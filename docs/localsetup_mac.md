
# Resources for Building llama.cpp From Source (llama-server) on Mac
**LLAMA CPP Server features**

https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md


**References**

**Official documentation:**

https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md#metal-build

**Additional resources by the community**

- https://www.youtube.com/watch?v=7IDhNLZVfq0
- https://el337.com/posts/build-llama-cpp-from-source/

# Build from Source
Install basic dependencies:
```
brew install cmake ninja git
````
Clone the repository:
```
git clone https://github.com/ggml-org/llama.cpp                
cd llama.cpp


```
**Build with Metal Support**

```
cmake -B llama.cpp/build -DBUILD_SHARED_LIBS=OFF -DGGML_METAL=ON
cmake --build llama.cpp/build --config Release -j 8 --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split
```

`-j 8` will run 8 jobs in parallel

*Accelerated computation*
On MacOs, by default DGGML_METAL is enabled, which makes computation run on GPU, but it can be disabled with `--n-gpu-layers 0`.


# Start the Server
```
mkdir models
curl -L -o models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
```
Set environment variable with model name:
```
MODEL_NAME="Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
```
For access from other devices on your LAN:
```
build/bin/llama-server --host 0.0.0.0 --model models/$MODEL_NAME -c 2048
build/bin/llama-server --host 0.0.0.0 --model models/$MODEL_NAME -c 2048 --n-gpu-layers 0
```


**Build with Docker**

TODO: Review .devops/cpu.Dockerfile for MacOS. It doesnt run properly for some reason.
TODO: Explor on a Docker Sandbox environment for secure server deployments.
```
docker build \                                                               
  -f .devops/cpu.Dockerfile \
  --target server \
  -t official-llama-server:latest .
```
```
docker run --name llama-server \
  -p 8080:8080 \
  -v ./models:/models \
  official-llama-server \
  --host 0.0.0.0 \
  --model /models/$MODEL_NAME \
  -c 2048 \
  --n-gpu-layers 0
```

# Networking

`--host` controls which network interfaces can reach the server:
- 127.0.0.1 -> only this Mac
- 0.0.0.0 -> all network interfaces, including your LAN

For security, prefer 127.0.0.1 unless you actually need remote access.

`--port` determines where the server listens. 8080 is the common default, but you can choose another port if it conflicts with an existing service.

To find your Mac's LAN IP:
```
ifconfig | grep "inet " | grep -v 127.0.0.1
```
You can then connect from another device using:
```
http://<MAC-IP>:8080
```
**Important**: `0.0.0.0` does not mean the server is automatically exposed to the internet. It means llama-server listens on all local interfaces. Your firewall/router still determines external accessibility.

