import random
from typing import Dict

# Мок-данные для демо
MOCK_EMPLOYEES = [
    {"id": 1, "name": "Айнура Сатпаева", "department_id": "IT", "goals": [
        {"goal_text": "Внедрить CI/CD пайплайн", "smart_index": 0.85, "strategic_alignment": True},
        {"goal_text": "Оптимизировать время сборки", "smart_index": 0.72, "strategic_alignment": True},
        {"goal_text": "Написать документацию", "smart_index": 0.58, "strategic_alignment": False}
    ]},
    {"id": 2, "name": "Бауыржан Омаров", "department_id": "IT", "goals": [
        {"goal_text": "Снизить количество багов на 30%", "smart_index": 0.91, "strategic_alignment": True},
        {"goal_text": "Провести код-ревью", "smart_index": 0.45, "strategic_alignment": False}
    ]},
    {"id": 3, "name": "Гульмира Абдиева", "department_id": "HR", "goals": [
        {"goal_text": "Снизить текучесть кадров до 10%", "smart_index": 0.88, "strategic_alignment": True},
        {"goal_text": "Внедрить программу наставничества", "smart_index": 0.76, "strategic_alignment": True},
        {"goal_text": "Провести 3 тренинга", "smart_index": 0.62, "strategic_alignment": False},
        {"goal_text": "Улучшить онбординг", "smart_index": 0.71, "strategic_alignment": True}
    ]},
    {"id": 4, "name": "Дамир Нурланов", "department_id": "Finance", "goals": [
        {"goal_text": "Сократить операционные расходы на 15%", "smart_index": 0.94, "strategic_alignment": True},
        {"goal_text": "Автоматизировать отчетность", "smart_index": 0.83, "strategic_alignment": True}
    ]}
]

def get_department_dashboard(dept_id: str) -> Dict:
    # Фильтруем сотрудников по департаменту
    dept_employees = [emp for emp in MOCK_EMPLOYEES if emp["department_id"] == dept_id]
    
    if not dept_employees:
        dept_employees = [emp for emp in MOCK_EMPLOYEES if emp["department_id"] == "IT"]
        dept_id = "IT (демо-данные)"
    
    all_goals = []
    smart_indices = []
    strategic_count = 0
    
    for emp in dept_employees:
        for goal in emp["goals"]:
            all_goals.append(goal)
            smart_indices.append(goal["smart_index"])
            if goal["strategic_alignment"]:
                strategic_count += 1
    
    total_goals = len(all_goals)
    avg_smart = sum(smart_indices) / len(smart_indices) if smart_indices else 0
    strategic_rate = strategic_count / total_goals if total_goals else 0
    
    top_issues = []
    if avg_smart < 0.7:
        top_issues.append("Низкий общий SMART-индекс команды")
    
    low_quality_goals = [g for g in all_goals if g["smart_index"] < 0.6]
    if low_quality_goals:
        top_issues.append(f"{len(low_quality_goals)} целей требуют улучшения (индекс < 0.6)")
    
    activity_goals = [g for g in all_goals if "написать" in g["goal_text"].lower() or "провести" in g["goal_text"].lower()]
    if activity_goals:
        top_issues.append(f"{len(activity_goals)} activity-целей, рекомендуется переформулировать")
    
    if not top_issues:
        top_issues = ["Все показатели в норме"]
    
    employees_list = []
    for emp in dept_employees:
        emp_smart = sum(g["smart_index"] for g in emp["goals"]) / len(emp["goals"]) if emp["goals"] else 0
        emp_strategic = sum(1 for g in emp["goals"] if g["strategic_alignment"])
        
        employees_list.append({
            "id": emp["id"],
            "name": emp["name"],
            "goal_count": len(emp["goals"]),
            "avg_smart_index": round(emp_smart, 2),
            "strategic_goals_count": emp_strategic,
            "needs_attention": emp_smart < 0.6
        })
    
    return {
        "department_id": dept_id,
        "avg_smart_index": round(avg_smart, 2),
        "strategic_alignment_rate": round(strategic_rate, 2),
        "total_goals": total_goals,
        "top_issues": top_issues,
        "employees": employees_list
    }