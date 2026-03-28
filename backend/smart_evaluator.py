import json
import random

def evaluate_smart(goal_text: str, role_context: str = "") -> dict:
    """
    Мок-версия SMART-оценки без OpenAI.
    Возвращает правдоподобные данные для демо.
    """
    
    # Анализируем текст цели для более реалистичных оценок
    goal_lower = goal_text.lower()
    
    # S - Конкретность
    if any(word in goal_lower for word in ["увеличить", "снизить", "разработать", "внедрить", "создать"]):
        specific_score = 0.9
        specific_reason = "Цель содержит конкретное действие"
    elif len(goal_text.split()) < 5:
        specific_score = 0.3
        specific_reason = "Цель слишком короткая, не хватает конкретики"
    else:
        specific_score = 0.6
        specific_reason = "Цель сформулирована, но можно уточнить предмет"
    
    # M - Измеримость
    if any(char.isdigit() for char in goal_text) or any(word in goal_lower for word in ["%", "процент", "раз", "часов", "дней"]):
        measurable_score = 0.85
        measurable_reason = "Цель содержит числовой показатель"
    else:
        measurable_score = 0.4
        measurable_reason = "Отсутствует числовой KPI или измеримый результат"
    
    # A - Достижимость
    if any(word in goal_lower for word in ["на 100%", "все", "полностью"]):
        achievable_score = 0.5
        achievable_reason = "Цель может быть слишком амбициозной"
    else:
        achievable_score = 0.8
        achievable_reason = "Цель выглядит реалистичной для данной роли"
    
    # R - Релевантность
    if any(word in goal_lower for word in ["стратегия", "kpi", "бизнес", "клиент", "эффективность"]):
        relevant_score = 0.85
        relevant_reason = "Цель связана со стратегическими приоритетами"
    else:
        relevant_score = 0.5
        relevant_reason = "Связь со стратегией компании не очевидна"
    
    # T - Ограниченность во времени
    if any(word in goal_lower for word in ["до", "квартал", "год", "месяц", "2026", "2025"]):
        time_score = 0.9
        time_reason = "Указан конкретный срок"
    else:
        time_score = 0.4
        time_reason = "Не указан срок выполнения"
    
    criteria = {
        "specific": {"score": specific_score, "reason": specific_reason},
        "measurable": {"score": measurable_score, "reason": measurable_reason},
        "achievable": {"score": achievable_score, "reason": achievable_reason},
        "relevant": {"score": relevant_score, "reason": relevant_reason},
        "time_bound": {"score": time_score, "reason": time_reason}
    }
    
    smart_index = sum(v["score"] for v in criteria.values()) / len(criteria)
    
    # Генерация рекомендации на основе слабых мест
    weak_criteria = [k for k, v in criteria.items() if v["score"] < 0.6]
    if weak_criteria:
        feedback = f"Улучшите критерии: {', '.join(weak_criteria)}. " + recommendations[weak_criteria[0] if weak_criteria else "default"]
    else:
        feedback = "Хорошая цель, соответствует SMART критериям."
    
    # Улучшенная формулировка
    if smart_index < 0.7:
        if "улучшить" in goal_lower:
            reformulation = goal_text + " на 20% до конца квартала"
        elif "сделать" in goal_lower or "провести" in goal_lower:
            reformulation = goal_text.replace("сделать", "разработать и внедрить") + " с измеримым результатом до конца Q2 2026"
        else:
            reformulation = goal_text + " (с указанием срока и метрики)"
    else:
        reformulation = goal_text
    
    return {
        "smart_index": round(smart_index, 2),
        "criteria": criteria,
        "feedback": feedback,
        "reformulation": reformulation
    }

# Словарь рекомендаций
recommendations = {
    "specific": "Уточните, что именно нужно сделать и с каким объектом.",
    "measurable": "Добавьте числовой показатель или способ измерения результата.",
    "achievable": "Сделайте цель более реалистичной или разбейте на этапы.",
    "relevant": "Свяжите цель с бизнес-показателями или стратегией компании.",
    "time_bound": "Укажите конкретный срок выполнения цели.",
    "default": "Сформулируйте цель по SMART методологии."
}