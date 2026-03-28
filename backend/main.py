from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import (
    GoalEvaluationRequest, SmartEvaluationResponse,
    GoalGenerationRequest, GoalGenerationResponse,
    BatchEvaluationRequest, DashboardResponse
)
from smart_evaluator import evaluate_smart
from rag_generator import generate_goals
from validators import validate_goals_batch, validate_goal_set
from aggregator import get_department_dashboard
import uvicorn

app = FastAPI(title="HR-Karavan Swarm API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/evaluate", response_model=SmartEvaluationResponse)
async def evaluate_goal(req: GoalEvaluationRequest):
    try:
        result = evaluate_smart(req.goal_text, req.role)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate", response_model=GoalGenerationResponse)
async def generate_goals_endpoint(req: GoalGenerationRequest):
    try:
        goals = generate_goals(req.employee_role, req.department, req.top_k)
        return {"goals": goals}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch_evaluate")
async def batch_evaluate(req: BatchEvaluationRequest):
    results = []
    for g in req.goals:
        res = evaluate_smart(g.goal_text, g.role)
        results.append(res)
    validation = validate_goals_batch([g.goal_text for g in req.goals])
    return {"evaluations": results, "validation": validation}

@app.get("/dashboard/{department_id}")
async def dashboard(department_id: str):
    data = get_department_dashboard(department_id)
    return data

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)