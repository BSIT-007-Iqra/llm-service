# llm-service

A small FastAPI service with a swappable LLM backend, built to run on limited hardware.

## What it does
- `GET /health` returns service status and the active backend
- `POST /ask` takes `{"question": "..."}` and returns an answer
- `BACKEND=mock` returns a fake answer, `BACKEND=ollama` calls a local Ollama model

## Run it
```bash
docker build --format docker -t llm-service:0.1 .
docker run -d --name llm-service -p 8000:8000 --memory=256m --cpus=0.5 llm-service:0.1
curl http://localhost:8000/health
```

## Resource usage (measured)
| Metric | Value |
|---|---|
| Image size | [X MB] |
| Idle memory | [Y MB] |
| Limits | 256 MB RAM, 0.5 CPU |

## Problems I hit
- Model download failed with "no space left on device" on a 20 GB disk
- A VM with 923 MB of RAM could not run any model
- Old process on port 8000 answered my test instead of the new container

## Design decisions
- Mock backend so the service can be built and deployed without a GPU
- Non-root container user and a healthcheck
- Settings come from environment variables, not code

## Next
Kubernetes manifests with requests and limits, then image scanning in CI.
