from typing import List, Dict
import re

def validate_goal_set(goals: List[Dict]) -> Dict:
    """Проверка набора целей без использования тяжелых библиотек"""
    count = len(goals)
    warnings = []
    
    # Проверка количества целей
    if count < 3:
        warnings.append(f"⚠️ Целей меньше 3 (сейчас {count}). Рекомендуется иметь 3-5 целей.")
    if count > 5:
        warnings.append(f"⚠️ Целей больше 5 (сейчас {count}). Рекомендуется иметь 3-5 целей.")
    
    # Проверка суммы весов (если есть)
    total_weight = sum(g.get("weight", 0) for g in goals)
    if goals and abs(total_weight - 100) > 0.01:
        warnings.append(f"⚠️ Сумма весов {total_weight}% (должна быть 100%)")
    
    # Простая проверка на дублирование (по тексту)
    texts = [g["goal_text"].lower() for g in goals]
    for i in range(len(texts)):
        for j in range(i+1, len(texts)):
            # Если тексты очень похожи
            if texts[i] == texts[j]:
                warnings.append(f"⚠️ Цели #{i+1} и #{j+1} идентичны")
            elif len(texts[i]) > 10 and len(texts[j]) > 10:
                # Простое сравнение слов
                words_i = set(texts[i].split())
                words_j = set(texts[j].split())
                if len(words_i & words_j) / len(words_i | words_j) > 0.8:
                    warnings.append(f"⚠️ Цели '#{i+1}' и '#{j+1}' очень похожи по смыслу")
    
    # Классификация типов целей
    types = []
    for g in goals:
        text = g["goal_text"].lower()
        # Activity-based (действие)
        if any(word in text for word in ["создам", "разработаю", "напишу", "проведу", "сделаю", "подготовлю"]):
            types.append("activity")
            warnings.append(f"📝 Цель '{g['goal_text'][:50]}...' является activity-целью. Рекомендуется переформулировать в результат-ориентированную.")
        # Output-based (результат)
        elif any(word in text for word in ["увеличу", "снижу", "достигну", "повысить", "сокращу"]):
            types.append("output")
        # Impact-based (влияние)
        else:
            types.append("impact")
    
    return {
        "warnings": warnings,
        "is_valid": len([w for w in warnings if not w.startswith("📝")]) == 0,
        "goal_types": types,
        "total_goals": count
    }

def validate_goals_batch(goals_texts: List[str]) -> Dict:
    """Пакетная проверка набора целей"""
    warnings = []
    count = len(goals_texts)
    
    if count < 3:
        warnings.append(f"⚠️ Мало целей: {count} (рекомендуется 3-5)")
    if count > 5:
        warnings.append(f"⚠️ Много целей: {count} (рекомендуется 3-5)")
    
    # Проверка на дублирование
    texts_lower = [t.lower() for t in goals_texts]
    for i in range(len(texts_lower)):
        for j in range(i+1, len(texts_lower)):
            if texts_lower[i] == texts_lower[j]:
                warnings.append(f"⚠️ Цель '{goals_texts[i][:50]}...' повторяется")
    
    return {
        "warnings": warnings,
        "is_valid": len(warnings) == 0,
        "total_goals": count
    }