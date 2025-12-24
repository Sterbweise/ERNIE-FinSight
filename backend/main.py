import os
import uuid
import logging
import asyncio
from pathlib import Path
from typing import Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from models.schemas import (
    UploadResponse,
    TaskStatusResponse,
    TaskResultResponse,
    TaskStatus,
    AnalysisResult
)
from services.pdf_processor import PDFProcessor
from services.ernie_analyzer import ERNIEAnalyzer

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
NOVITA_API_KEY = os.getenv("NOVITA_API_KEY")
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "./uploads"))

# Ensure upload directory exists
UPLOAD_DIR.mkdir(exist_ok=True)

# In-memory task storage (for demo purposes)
tasks: Dict[str, Dict[str, Any]] = {}

# Initialize services
pdf_processor = PDFProcessor()
ernie_analyzer = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global ernie_analyzer
    
    # Startup
    if not NOVITA_API_KEY:
        logger.error("NOVITA_API_KEY not found in environment variables!")
    else:
        ernie_analyzer = ERNIEAnalyzer(NOVITA_API_KEY)
        logger.info("ERNIE Analyzer initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Application shutting down")


# Initialize FastAPI app
app = FastAPI(
    title="ERNIE FinSight API",
    description="Crypto whitepaper analyzer using ERNIE AI",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ernie-fin-sight.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ERNIE FinSight API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ernie_configured": ernie_analyzer is not None
    }


@app.post("/api/upload", response_model=UploadResponse)
async def upload_whitepaper(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Upload a PDF whitepaper for analysis
    
    Args:
        file: PDF file upload
        
    Returns:
        UploadResponse with task_id for tracking
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    
    # Generate unique task ID
    task_id = str(uuid.uuid4())
    
    # Save uploaded file
    file_path = UPLOAD_DIR / f"{task_id}_{file.filename}"
    
    try:
        # Save file to disk
        content = await file.read()
        
        # Check file size
        size_mb = len(content) / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            raise HTTPException(
                status_code=400,
                detail=f"File size ({size_mb:.2f}MB) exceeds maximum allowed size ({MAX_FILE_SIZE_MB}MB)"
            )
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        logger.info(f"File uploaded: {file.filename} (Task ID: {task_id})")
        
        # Initialize task status
        tasks[task_id] = {
            "status": TaskStatus.PENDING,
            "filename": file.filename,
            "file_path": str(file_path),
            "progress": 0,
            "result": None,
            "error": None
        }
        
        # Start background processing
        background_tasks.add_task(process_whitepaper, task_id)
        
        return UploadResponse(
            task_id=task_id,
            filename=file.filename,
            message="File uploaded successfully. Processing started."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        # Clean up file if exists
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


async def process_whitepaper(task_id: str):
    """
    Background task to process whitepaper
    
    Args:
        task_id: Unique task identifier
    """
    try:
        task = tasks[task_id]
        file_path = task["file_path"]
        
        # Update status to processing
        task["status"] = TaskStatus.PROCESSING
        task["progress"] = 10
        logger.info(f"Processing task {task_id}")
        
        # Step 1: Validate PDF
        is_valid, error_msg = pdf_processor.validate_pdf(file_path, MAX_FILE_SIZE_MB)
        if not is_valid:
            raise ValueError(error_msg)
        
        task["progress"] = 20
        
        # Step 2: Extract text from PDF
        logger.info(f"Extracting text from PDF: {file_path}")
        text = pdf_processor.extract_text(file_path)
        task["progress"] = 40
        
        # Step 3: Analyze with ERNIE
        if not ernie_analyzer:
            raise ValueError("ERNIE Analyzer not initialized. Check NOVITA_API_KEY.")
        
        logger.info(f"Analyzing whitepaper with ERNIE...")
        task["progress"] = 50
        
        result = ernie_analyzer.analyze_whitepaper(text)
        task["progress"] = 90
        
        # Update task with result
        task["status"] = TaskStatus.COMPLETED
        task["progress"] = 100
        task["result"] = result.model_dump()
        
        logger.info(f"Task {task_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Task {task_id} failed: {str(e)}")
        tasks[task_id]["status"] = TaskStatus.FAILED
        tasks[task_id]["error"] = str(e)
        tasks[task_id]["progress"] = 0
    
    finally:
        # Clean up uploaded file
        try:
            file_path = Path(tasks[task_id]["file_path"])
            if file_path.exists():
                file_path.unlink()
                logger.info(f"Cleaned up file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to clean up file: {str(e)}")


@app.post("/api/analyze/{task_id}")
async def trigger_analysis(task_id: str, background_tasks: BackgroundTasks):
    """
    Manually trigger analysis for an uploaded file (alternative endpoint)
    
    Args:
        task_id: Task identifier from upload
        
    Returns:
        Status message
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks[task_id]
    
    if task["status"] != TaskStatus.PENDING:
        raise HTTPException(
            status_code=400,
            detail=f"Task is already {task['status']}"
        )
    
    # Start processing
    background_tasks.add_task(process_whitepaper, task_id)
    
    return {"message": "Analysis started", "task_id": task_id}


@app.get("/api/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """
    Get the status of a processing task
    
    Args:
        task_id: Task identifier
        
    Returns:
        TaskStatusResponse with current status and progress
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks[task_id]
    
    return TaskStatusResponse(
        task_id=task_id,
        status=task["status"],
        message=task.get("error") if task["status"] == TaskStatus.FAILED else None,
        progress=task["progress"]
    )


@app.get("/api/result/{task_id}", response_model=TaskResultResponse)
async def get_task_result(task_id: str):
    """
    Get the analysis result for a completed task
    
    Args:
        task_id: Task identifier
        
    Returns:
        TaskResultResponse with analysis results
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks[task_id]
    
    if task["status"] == TaskStatus.PENDING or task["status"] == TaskStatus.PROCESSING:
        raise HTTPException(
            status_code=400,
            detail="Task is still processing. Check status endpoint for progress."
        )
    
    result = None
    if task["status"] == TaskStatus.COMPLETED and task["result"]:
        result = AnalysisResult(**task["result"])
    
    return TaskResultResponse(
        task_id=task_id,
        status=task["status"],
        result=result,
        error=task.get("error")
    )


@app.delete("/api/task/{task_id}")
async def delete_task(task_id: str):
    """
    Delete a task and its data
    
    Args:
        task_id: Task identifier
        
    Returns:
        Deletion confirmation
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    del tasks[task_id]
    
    return {"message": "Task deleted successfully", "task_id": task_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

