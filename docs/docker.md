
### Build LLama.cpp Docker image
While inside the folder repo `Local-LLM-Experiments/`, run the following command:

```Powershell 
docker build --file llmengines/llama.cpp/.devops/cpu.Dockerfile --tag llama.cpp-server llmengines/llama.cpp

```

### Run LLM inference engine on a Docker container
Excute the following command on a terminal with access to docker. On Windows, first install Docker Desktop, the Windows Subsystem for Linux WSL, and then use a WindowsPowerShell terminal.

**Windows**
```Powershell
$env:MODEL_NAME="Mistral-7B-Instruct-v0.3-Q4_K_M.gguf"
```
```Powershell
docker compose -f llmengines/docker-compose.yaml up
```

## My Docker Worflow (Stop container gracefully)
On the WindowsPowerShell terminal, running the container. 
1. Press `Ctrl + C` to stop the container.
2. Run `docker ps -n <some number>` to discover the CONTAINER ID 
3. Run `docker rm <CONTAINER ID (a SHA like string)> `

## Restart Container with a New Model
One the WindowsPowerShell,
1. Run `ls models/` to check the available models in GGUF format. In my case, I get something like this
    ```PowerShell 
    Mode                 LastWriteTime         Length Name
    ----                 -------------         ------ ----
    -a----         2/14/2026  12:35 PM     4920739232 Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
    -a----         2/15/2026   5:08 PM     4368439584 mistral-7b-instruct-v0.2.Q4_K_M.gguf
    -a----         2/14/2026  12:17 PM     4372812000 Mistral-7B-Instruct-v0.3-Q4_K_M.gguf
    ``` 
2. Set an environment variable and restart the container as follows:

    ```PowerShell
    $env:MODEL_NAME="Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
    docker compose --file llmengines/docker-compose.yaml up -d --force-recreate
    ```
Note that llmengines/myclient.py defines an api class to do this using python code. 