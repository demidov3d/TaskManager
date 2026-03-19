import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Создаём папку для отчётов
Path('reports').mkdir(exist_ok=True)

with open('AI_Core_Tasks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

tasks = [e for e in data['entities'] if e['type'] == 'task']

# Фильтрация
critical = [t for t in tasks if t['props'].get('priority') == 'critical']
high = [t for t in tasks if t['props'].get('priority') == 'high']
in_progress = [t for t in tasks if t['props'].get('status') == 'in_progress']
todo = [t for t in tasks if t['props'].get('status') == 'todo']

overdue = []
for t in tasks:
    due = t['props'].get('due', '')
    if due:
        try:
            if datetime.fromisoformat(due) < datetime.now():
                overdue.append(t)
        except:
            pass

# Консольный вывод
print("\n" + "="*70)
print("📊 АНАЛИЗ ЗАДАЧ AI Core Tasks")
print("="*70)
print(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

print("📌 ОБЩАЯ СТАТИСТИКА")
print(f"  • Всего задач: {len(tasks)}")
print(f"  • Критичные: {len(critical)}")
print(f"  • Высокий приоритет: {len(high)}")
print(f"  • В работе: {len(in_progress)}")
print(f"  • К выполнению: {len(todo)}")
print(f"  • Просроченные: {len(overdue)}\n")

if critical:
    print("🔴 КРИТИЧНЫЕ ЗАДАЧИ:")
    for t in critical:
        status = t['props'].get('status', 'unknown')
        due = t['props'].get('due', 'нет срока')
        est = t['props'].get('est_hours', 0)
        print(f"  • {t['title']}")
        print(f"    Статус: {status} | Срок: {due} | Эст: {est}ч\n")

if overdue:
    print("⚠️  ПРОСРОЧЕННЫЕ ЗАДАЧИ:")
    for t in overdue:
        due = t['props'].get('due', 'unknown')
        print(f"  • {t['title']}")
        print(f"    Срок был: {due}\n")

if in_progress:
    print("🔵 В РАБОТЕ:")
    for t in in_progress:
        est = t['props'].get('est_hours', 0)
        print(f"  • {t['title']} ({est}ч)\n")

print("="*70 + "\n")

# Генерируем Markdown отчёт
report = f"""# 📋 Отчёт по задачам

**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Статистика

- **Всего задач:** {len(tasks)}
- **Критичные:** {len(critical)}
- **Высокий приоритет:** {len(high)}
- **В работе:** {len(in_progress)}
- **К выполнению:** {len(todo)}
- **Просроченные:** {len(overdue)}

## 🔴 Критичные задачи ({len(critical)})

"""

for t in critical:
    status = t['props'].get('status', 'unknown')
    due = t['props'].get('due', 'нет срока')
    est = t['props'].get('est_hours', 0)
    report += f"- **{t['title']}**\n  - Статус: `{status}`\n  - Срок: {due}\n  - Эст: {est}ч\n\n"

report += f"\n## ⚠️ Просроченные ({len(overdue)})\n\n"
for t in overdue:
    due = t['props'].get('due', 'unknown')
    report += f"- **{t['title']}** (был срок: {due})\n"

# Сохраняем отчёт
with open('reports/tasks_report.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("✅ Отчёт сохранён в reports/tasks_report.md")
