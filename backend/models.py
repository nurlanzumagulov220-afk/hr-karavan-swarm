from pydantic import BaseModel
from typing import List, Optional

class GoalEvaluationRequest(BaseModel):
    goal_text: str
    role: str = ""
    department: str = ""

class GoalGenerationRequest(BaseModel):
    employee_role: str
    department: str
    top_k: int = 5

class BatchEvaluationRequest(BaseModel):
    goals: List[GoalEvaluationRequest]

class CriteriaScore(BaseModel):
    score: float
    reason: str

class SmartEvaluationResponse(BaseModel):
    smart_index: float
    criteria: dict[str, CriteriaScore]
    feedback: str
    reformulation: str

class GeneratedGoal(BaseModel):
    goal_text: str
    source_title: str
    source_fragment: str

class GoalGenerationResponse(BaseModel):
    goals: List[GeneratedGoal]

class DashboardResponse(BaseModel):
    department_id: str
    avg_smart_index: float
    strategic_alignment_rate: float
    top_issues: List[str]
    employees: List[dict]