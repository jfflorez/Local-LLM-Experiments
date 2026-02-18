
import os, sys
project_dir = os.path.normpath(os.path.join(os.path.abspath(__file__),'..','..'))
if not project_dir in sys.path:
    sys.path.append(project_dir)

import subprocess
import requests
import time
from urllib.parse import urljoin

class myLlamacppClient():

    def __init__(self, base_url : str = "http://localhost:8080/"):
        self.base_url = base_url
        docker_compose_file = os.path.normpath(os.path.join(project_dir,'llmengines','docker-compose.yaml'))
        self.docker_compose_file = docker_compose_file.replace(os.sep,"/")
        self.load_container_id()

    def _get_container_id(self, service_name: str = "llama-server"):
        command = ["docker-compose", "--file", self.docker_compose_file, "ps", "-q", service_name]

        env = os.environ.copy() # needed for docker file interpolation
        env.setdefault("MODEL_NAME", "dummy")  # satisfies interpolation, not actually used
        result = subprocess.run(command, capture_output=True, text=True, env= env)
        return result.stdout.strip() or None

    def check_health_endpoint(self, endpoint : str = "health"):

        url = urljoin(self.base_url, endpoint)
        response = requests.get(url,timeout=5)

        if response.status_code == 200:
            self.status_code = 200
            print(f'LLM server is healthy : Reponse {response.json()}')

    def load_container_id(self):

        #command = ["docker", "ps", "--filter", f"id={CONTAINER_ID}", '-q']
        #response = subprocess.run(command, capture_output=True)
        #if not response.stdout.decode():
        #    print(f'Invalid container id : {CONTAINER_ID}. Choose one from the following')
        #    response = subprocess.run(["docker","ps","--all"])
        #    print(response.stdout.decode())
        self.container_id = self._get_container_id()

    def get_loaded_model(self):

        print(f"DEBUG container_id: {self.container_id}")
        command = ["docker", "exec", f"{self.container_id}", "printenv", "MODEL_NAME"]
        result = subprocess.run(command, capture_output=True)
        model_name = result.stdout.decode().strip()
        print(f"DEBUG model_name returned: '{model_name}'")
        return model_name


    def wait_for_healthy(self, health_endpoint : str = "health", timeout: int = 120, interval: int = 0.1):
        """
        Poll health endpoint until container is ready and status is ok.
        """
        
        #url = os.path.join(self.base_url, health_endpoint)        
        url = urljoin(self.base_url, health_endpoint)
        #max_retries = 3
        #retries = 0
        t_start = time.time()
        deadline =  t_start + timeout
        while time.time() < deadline:
            try:
                response = requests.get(url, timeout=3)

                if response.status_code == 200:
                    body = response.json()
                    if body.get("status") == "ok":

                        elapsed_time = time.time() - t_start
                        print(f"Container is healthy after {elapsed_time:0.2f} seconds.")
                        print(f"Response: {body}")
                        return

            except requests.RequestException:
                # Service not up yet
                pass

            #retries += 1
            #if retries >= max_retries:
            #    raise StopIteration(f"Container is not healthy after {retries}/{max_retries} health check attempts.") 
            #TimeoutError(f"Container is not healthy after {timeout}s")
                #break

            #print(f"Retrying health check... ({retries}/{max_retries})")
            time.sleep(interval)

        raise TimeoutError(f"Container is not healthy after {timeout}s")


    def switch_model(self, model_name: str,  health_endpoint : str = "health"):
        """
        Switch model by restarting docker-compose with new model name.
        Waits for container to be healthy before proceeding.

        model_name (str) : must be a valid string (e.g, *.GGUF) in project_path/models
        """
        models_dir = os.path.join(project_dir, "models")
        print(f"Expected models directory : {models_dir}")

        if model_name not in os.listdir(models_dir):
            print(f'Skipping model {model_name}. Choose one available in {models_dir}')
            return

        try:
            self.wait_for_healthy(health_endpoint, timeout=5)
            if self.get_loaded_model() == model_name:
                print(f"Model {model_name} already loaded, skipping restart.")
                return
        except TimeoutError:
            pass  # container not running, proceed with startup

        # 1. Set environment variable 
        env = os.environ.copy()
        env['MODEL_NAME'] = model_name

        # 2. Shut down existing container
        print(f"Stopping current container...")
        down = subprocess.run(
            ['docker-compose', '--file', self.docker_compose_file, 'down'],
            env=env,
            capture_output=True,
            text=True,
            check=True
        )
        print("Stopped:", down.stdout)

        # 3. Start new container with new model
        print(f"Starting container with model: {model_name}")
        up = subprocess.run(
            ['docker-compose', '--file', self.docker_compose_file, 'up', '-d'],
            env=env,
            capture_output=True,
            text=True,
            check=True
        )
        print("Started:", up.stdout)

        # 4. Wait for container to be healthy
        self.wait_for_healthy(health_endpoint, timeout=120)
        self.container_id = self._get_container_id()  # <- here
        print(f"Ready! Model {model_name} is live.")


                



                

        




