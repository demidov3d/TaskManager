import json
from datetime import datetime
from pathlib import Path

print("🚀 Starting script...")

try:
    # Создаём папку
    Path('reports').mkdir(exist_ok=True)
    print("✅ Created reports folder")
    
    # Читаем JSON
    print("📖 Reading AI_Core_Tasks.json...")
    with open('AI_Core_Tasks.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("✅ JSON loaded")
    
    # Получаем задачи
    tasks = [e for e in data['entities'] if e['type'] == 'task']
    print(f"✅ Found {len(tasks)} tasks")
    
    # Создаём простой HTML
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Test Report</title>
    <style>
        body {{ font-family: Arial; padding: 20px; }}
        h1 {{ color: #667eea; }}
        .stat {{ background: #f0f0f0; padding: 10px; margin: 10px 0; }}
    </style>
</head>
<body>
    <h1>📊 Test Report</h1>
    <div class="stat">
        <p><strong>Total tasks:</strong> {len(tasks)}</p>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    <h2>Tasks:</h2>
    <ul>
"""
    
    # Добавляем задачи
    for t in tasks[:10]:  # Первые 10
        title = t.get('title', 'No title')
        html_content += f"        <li>{title}</li>\n"
    
    html_content += """    </ul>
</body>
</html>
"""
    
    # Сохраняем
    output_file = 'reports/index.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML saved to {output_file}")
    print(f"📏 File size: {Path(output_file).stat().st_size} bytes")
    
except Exception as e:
    print(f"❌ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    
    # Сохраняем ошибку
    with open('reports/error.txt', 'w') as f:
        f.write(f"Error: {e}\n")
        f.write(traceback.format_exc())

print("✅ Script finished!")
