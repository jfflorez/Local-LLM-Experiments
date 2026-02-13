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
