# Local-LLM-Experiments
Collection of mini experiments and insights using local LLM inference engines like LLaMA.cpp

**Stack:** llama.cpp server (pinned build, Docker, CPU) · quantized 7–8B models (GGUF, Q4_K_M) · Python client for model switching · config-hashed, reproducible experiment runs.

## Getting Started

See [Local Setup](docs/localsetup.md) for detailed setup instructions.

## Experiment Index

| # | Question | Models | Report | 
|---|----------|--------|--------|
| 0 | How does sampling temperature shape the distribution of the first generated word? | Mistral-7B-Instruct-v0.3, Llama-3.1-8B-Instruct | [exp_0](experiments/exp_0/exp_0_report.md) | 
