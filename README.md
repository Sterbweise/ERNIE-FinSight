# ERNIE FinSight - Crypto Whitepaper Analyzer

**Transform complex crypto whitepapers into beautiful, easy-to-understand insights using ERNIE AI**

> Built for the **Baidu ERNIE AI Developer Challenge** - [DevPost](https://baiduernieai.devpost.com/)
>
> Qualifying for: **Best ERNIE Multimodel Application | Sponsored by Novita**

## 🚀 Live Demo

- **🌐 Website:** [https://ernie-fin-sight.vercel.app](https://ernie-fin-sight.vercel.app)
- **📹 Video Presentation:** [Watch on Vimeo](https://vimeo.com/1148937798?fl=pl&fe=sh)
- **🔧 Backend API:** [https://ernie-finsight.onrender.com](https://ernie-finsight.onrender.com)

Try it now! Upload any crypto whitepaper and get instant AI-powered insights.

## 📖 Overview

ERNIE FinSight is an intelligent crypto whitepaper analyzer that leverages Baidu's ERNIE 4.5 multimodal AI model (via Novita AI API) to extract, analyze, and present complex whitepaper information in a beautiful, accessible web interface.

### Key Features

- 📄 **PDF Upload & Processing** - Drag-and-drop interface with real-time progress
- 🧠 **ERNIE AI Analysis** - Comprehensive analysis using Baidu's ERNIE 4.5 VL model
- 💎 **Beautiful Dashboard** - Modern, financial-themed UI with smooth animations
- 📊 **Structured Insights** - Executive summary, tokenomics, roadmap, risks, and more
- ⚡ **Fast & Async** - Non-blocking background processing with status tracking

## Tech Stack

### Backend

- **FastAPI** - Modern Python web framework
- **Novita AI API** - Access to ERNIE 4.5 models
- **ERNIE 4.5 VL** - Baidu's multimodal AI model
- **PyPDF2 & pdfplumber** - PDF text extraction
- **Pydantic** - Data validation

### Frontend

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Fast build tool
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **React Router** - Navigation
- **Axios** - HTTP client

## Quick Start

> 💡 **Want to try it immediately?** Visit the [live demo](https://ernie-fin-sight.vercel.app) - no setup required!

### Local Development

#### Prerequisites

- Python 3.9+
- Node.js 18+
- Novita AI API key ([Get one here](https://novita.ai/))

### Backend Setup

1. **Navigate to backend directory**

```bash
cd backend
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment**

```bash
# Create .env file
NOVITA_API_KEY=your_novita_api_key_here
MAX_FILE_SIZE_MB=10
UPLOAD_DIR=./uploads
```

4. **Run the server**

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**

```bash
cd frontend
```

2. **Install dependencies**

```bash
npm install
```

3. **Run development server**

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## 📚 API Documentation

### Endpoints

#### `POST /api/upload`

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

#### `GET /api/status/{task_id}`

Check processing status.

**Response:**

```json
{
  "task_id": "uuid-string",
  "status": "processing",
  "progress": 50,
  "message": null
}
```

#### `GET /api/result/{task_id}`

Retrieve analysis results.

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
  }
}
```

### Features

- Glassmorphism cards
- Smooth animations with Framer Motion
- Responsive design
- Loading states and skeletons
- Error handling

## What Makes This Special

### For the Hackathon

1. **ERNIE Multimodal Capabilities** - Showcases ERNIE's advanced understanding of complex documents
2. **Novita AI Integration** - Uses Novita AI API for ERNIE access (qualifying for sponsored category)
3. **Practical Use Case** - Solves real problem for crypto investors and analysts
4. **Professional Quality** - Production-ready code with proper architecture
5. **Beautiful UX** - Modern, polished interface with attention to detail

### Technical Highlights

- **Async Processing** - Non-blocking analysis with real-time status updates
- **Structured Prompts** - Engineered prompts for consistent JSON output
- **Error Handling** - Graceful failures with helpful error messages
- **Type Safety** - Full TypeScript + Pydantic validation
- **Clean Architecture** - Separation of concerns, scalable design

## Use Cases

- **Crypto Investors** - Quickly understand new projects
- **Financial Analysts** - Comprehensive project evaluation
- **Due Diligence** - Risk assessment and comparison
- **Research** - Academic analysis of blockchain projects
- **Education** - Learning about crypto projects

## 🔧 Development

### Running Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

### Building for Production

```bash
# Backend
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run build
npm run preview
```

## 🌍 Deployment

The application is currently deployed and live:

- **Frontend:** Hosted on [Vercel](https://vercel.com) with automatic deployments from GitHub
  - URL: https://ernie-fin-sight.vercel.app
- **Backend:** Hosted on [Render](https://render.com) with automatic deployments from GitHub
  - API URL: https://ernie-finsight.onrender.com
  - Health check: https://ernie-finsight.onrender.com/api/health

For detailed deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)

## License

MIT License - Built for the Baidu ERNIE AI Developer Challenge

## 🙏 Acknowledgments

- **Baidu** - For the amazing ERNIE AI models
- **Novita AI** - For providing accessible ERNIE API
- **DevPost** - For hosting the hackathon

## 👥 Team

Built with ❤️ for the Baidu ERNIE AI Developer Challenge

---

**Note:** This is a hackathon demo project.
