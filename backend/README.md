# ERNIE FinSight Backend

Backend API for crypto whitepaper analyzer using ERNIE AI via Novita AI.

## Setup

1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

2. **Configure Environment**
   Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your Novita AI API key:

```
NOVITA_API_KEY=your_actual_api_key_here
MAX_FILE_SIZE_MB=10
UPLOAD_DIR=./uploads
```

3. **Run the Server**

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### `POST /api/upload`

Upload a PDF whitepaper for analysis.

**Request:**

- Content-Type: `multipart/form-data`
- Body: `file` (PDF file, max 10MB)

**Response:**

```json
{
  "task_id": "uuid-string",
  "filename": "whitepaper.pdf",
  "message": "File uploaded successfully. Processing started."
}
```

### `GET /api/status/{task_id}`

Check the processing status of a task.

**Response:**

```json
{
  "task_id": "uuid-string",
  "status": "processing",
  "progress": 50,
  "message": null
}
```

Status values: `pending`, `processing`, `completed`, `failed`

### `GET /api/result/{task_id}`

Retrieve the analysis results for a completed task.

**Response:**

```json
{
  "task_id": "uuid-string",
  "status": "completed",
  "result": {
    "project_name": "Example Token",
    "executive_summary": "...",
    "key_value_propositions": [...],
    "technology_stack": {...},
    "tokenomics": {...},
    "roadmap": [...],
    "team_and_partnerships": {...},
    "risk_factors": [...],
    "competitive_advantages": [...],
    "target_audience": [...],
    "use_cases": [...],
    "overall_assessment": "..."
  },
  "error": null
}
```

### `GET /api/health`

Health check endpoint.

## Testing

Test the API with curl:

```bash
# Upload a PDF
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@path/to/whitepaper.pdf"

# Check status
curl "http://localhost:8000/api/status/{task_id}"

# Get results
curl "http://localhost:8000/api/result/{task_id}"
```

## Architecture

- **FastAPI**: Modern async web framework
- **Novita AI**: API provider for ERNIE models
- **ERNIE 4.5**: Baidu's multimodal AI model for analysis
- **PyPDF2/pdfplumber**: PDF text extraction
- **Background Tasks**: Async processing for long-running analysis

## Notes

- Files are automatically deleted after processing
- Task data is stored in-memory (not persistent)
- Suitable for hackathon demo purposes
