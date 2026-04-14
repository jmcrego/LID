# FastAPI LID Service

A FastAPI microservice for language identification using FastText and the `lid.176.bin` model.

## Features

- Load `resources/lid.176.bin` at startup
- `GET /health`: Service status and model load status
- `GET /lid`: Return top-5 language candidates and scores
- Default local server target: `127.0.0.1:8004`

## Endpoints

### `GET /health`

Returns service health and model availability.

### `POST /lid`

Detects language from a `text` query parameter and returns the k-best candidates.

**Query parameter:**
- `text` (string, required)
- `k` (int, optional)

## Setup

### 1) Place the FastText model

The server expects:

`resources/lid.176.bin`

Download it with:

```bash
mkdir -p resources
curl -L https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin -o resources/lid.176.bin
```

### 2) Create and prepare the virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Running the Server

```bash
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8004 --reload
```

## Example Requests

### Health check

```bash
curl "http://127.0.0.1:8004/health"
```

Example response:

```json
{
  "status": "ok",
  "model_loaded": true,
  "model_path": "/path/to/LID/resources/lid.176.bin",
  "runtime_ms": 0.0014584511518478394
}
```

### LID detection (top-5)

```bash
curl -X POST "http://localhost:8004/lid"   -H "Content-Type: application/json"   -d '{"text": "This is my sentence", "k": 5}' 
```

Example response:

```json
{
  "candidates": [
    {"lang": "en", "score": 0.99},
    {"lang": "nl", "score": 0.001},
    {"lang": "de", "score": 0.001},
    {"lang": "fr", "score": 0.001},
    {"lang": "it", "score": 0.001}
  ]
  "runtime_ms": 0.12083259359002113
}
```

## Directory Structure

- `app/main.py` - FastAPI app and routes
- `app/lid.py` - LID endpoint logic and response models
- `app/health.py` - Health endpoint logic and response model
- `app/shared.py` - Shared model state and model path
- `requirements.txt` - Python dependencies
- `resources/` - FastText model directory (`lid.176.bin`)

