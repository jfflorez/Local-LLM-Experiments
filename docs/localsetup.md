## Get Started

- Build llama.cpp
- Download models
- Run experiments

### 1. Clone the repository with submodules
```bash
git clone --recurse-submodules https://github.com/jfflorez/Local-LLM-Insights.git
cd Local-LLM-Insights
```
### Run LLM inference engine on a Docker container
Excute the following command on a terminal with access to docker. On Windows, first install Docker Desktop, the Windows Subsystem for Linux WSL, and then use a WindowsPowerShell terminal.

```
docker compose -f llmengines/docker-compose.yaml up
```

## My Docker Worflow (Stop container gracefully)
On the WindowsPowerShell terminal, running the container. 
1. Press `Ctrl + C` to stop the container.
2. Run `docker ps -n <some number>` to discover the CONTAINER ID 
3. Run `docker rm <CONTAINER ID (a SHA like string)> `

