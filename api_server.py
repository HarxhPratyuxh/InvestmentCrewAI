import os
import time
from typing import Dict, Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.analysis_service import AnalysisService
from models.analysis import InvestmentRecommendation

# FastAPI app initialization
app = FastAPI(
    title="Financial Analysis API",
    description="A FastAPI server for running financial analysis using CrewAI agents",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response
class AnalysisRequest(BaseModel):
    stock: str
    execution_mode: str = "parallel"  # "parallel" or "sequential"


class AnalysisResponse(BaseModel):
    status: str
    execution_time: Optional[float] = None
    parallel_time: Optional[float] = None
    analysis_time: Optional[float] = None
    time_saved: Optional[float] = None
    task_id: Optional[str] = None


class TaskStatus(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict] = None
    execution_time: Optional[float] = None
    error: Optional[str] = None


# In-memory storage for task results
task_results = {}


async def run_analysis_background(task_id: str, stock: str, execution_mode: str):
    """Background task to run the analysis."""
    start_time = time.time()
    
    # Initialize Service
    service = AnalysisService()

    task_results[task_id] = {
        "status": "running",
        "start_time": start_time,
        "stock": stock,
    }

    try:
        # Run Analysis (The service handles parallel/sequential logic internally now)
        # We use the async wrapper provided by the service
        result = await service.run_analysis_async(stock, risk_profile="Moderate")
        
        end_time = time.time()
        execution_time = end_time - start_time

        # Serialize Pydantic model to dict
        result_data = result.model_dump() if hasattr(result, 'model_dump') else result.dict()

        task_results[task_id] = {
            "status": "completed",
            "execution_time": execution_time,
            "stock": stock,
            "results": result_data
        }
    except Exception as e:
        task_results[task_id] = {
            "status": "failed",
            "error": str(e),
            "stock": stock
        }


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Financial Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "POST /analyze": "Start financial analysis",
            "GET /status/{task_id}": "Get analysis status",
            "GET /health": "Health check",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": time.time()}


@app.post("/analyze", response_model=AnalysisResponse)
async def start_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """Start financial analysis for a given stock."""
    # Generate unique task ID
    task_id = f"{request.stock}_{int(time.time())}"

    # Start background task
    background_tasks.add_task(
        run_analysis_background, task_id, request.stock, request.execution_mode
    )

    return AnalysisResponse(
        status="started",
        task_id=task_id,
    )


@app.get("/status/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str):
    """Get the status of a running analysis task."""
    task_data = task_results[task_id]

    return TaskStatus(
        task_id=task_id,
        status=task_data["status"],
        result=task_data.get("results"),
        execution_time=task_data.get("execution_time"),
        error=task_data.get("error"),
    )


@app.get("/tasks")
async def list_tasks():
    """List all tasks and their statuses."""
    return {
        "tasks": [
            {
                "task_id": task_id,
                "status": data["status"],
                "stock": data.get("stock"),
                "execution_mode": data.get("execution_mode"),
                "execution_time": data.get("execution_time"),
            }
            for task_id, data in task_results.items()
        ]
    }


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a task from memory."""
    del task_results[task_id]
    return {"message": f"Task {task_id} deleted successfully"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
