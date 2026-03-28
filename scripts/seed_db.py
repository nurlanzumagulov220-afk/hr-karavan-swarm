import psycopg2
import os

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

# Здесь можно добавить тестовые данные, если нужно
# Например, создать несколько тестовых целей
cur.execute("""
    INSERT INTO goals (employee_id, title, description, quarter, year, status, smart_index, strategic_alignment)
    VALUES 
        (1, 'Увеличить продажи', 'Увеличить продажи на 15%', 'Q1', 2026, 'approved', 0.7, true),
        (2, 'Улучшить обслуживание', 'Снизить время ответа с 24ч до 4ч', 'Q1', 2026, 'approved', 0.9, true)
    ON CONFLICT DO NOTHING;
""")
conn.commit()
print("База данных инициализирована")