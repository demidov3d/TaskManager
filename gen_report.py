import json
from datetime import datetime

# Read JSON
with open('AI_Core_Tasks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get tasks
tasks = [e for e in data['entities'] if e['type'] == 'task']

# Stats
stats = {
    'total': len(tasks),
    'critical': len([t for t in tasks if t['props'].get('priority') == 'critical']),
    'high': len([t for t in tasks if t['props'].get('priority') == 'high']),
    'todo': len([t for t in tasks if t['props'].get('status') == 'todo']),
    'progress': len([t for t in tasks if t['props'].get('status') == 'in_progress']),
    'done': len([t for t in tasks if t['props'].get('status') == 'done']),
}

# Task data for JS
tasks_json = []
for t in tasks:
    tasks_json.append({
        'title': t.get('title', 'N/A'),
        'priority': t['props'].get('priority', 'normal'),
        'status': t['props'].get('status', 'todo'),
        'due': t['props'].get('due', '—'),
        'hours': t['props'].get('est_hours', 0),
        'module': t['props'].get('module', '—'),
    })

import json as json_lib
tasks_str = json_lib.dumps(tasks_json, ensure_ascii=False)

# HTML
html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>📊 Tasks Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); overflow: hidden; }}
        .header {{ background: #667eea; color: white; padding: 30px; text-align: center; }}
        .header h1 {{ font-size: 2em; margin-bottom: 10px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; padding: 30px; background: #f9f9f9; }}
        .stat {{ background: white; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; text-align: center; }}
        .stat.critical {{ border-left-color: #ff6b6b; }}
        .stat.high {{ border-left-color: #ffa94d; }}
        .stat-num {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        .stat.critical .stat-num {{ color: #ff6b6b; }}
        .stat.high .stat-num {{ color: #ffa94d; }}
        .stat-label {{ color: #666; font-size: 0.9em; margin-top: 8px; }}
        .controls {{ padding: 20px 30px; display: flex; gap: 15px; flex-wrap: wrap; align-items: center; border-bottom: 1px solid #eee; }}
        .control-group {{ display: flex; gap: 8px; align-items: center; }}
        .control-group label {{ font-weight: 600; }}
        select, input {{ padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; }}
        button {{ padding: 8px 16px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; }}
        button:hover {{ background: #5568d3; }}
        .table-wrapper {{ padding: 30px; overflow-x: auto; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ background: #f9f9f9; padding: 12px; text-align: left; font-weight: 600; border-bottom: 2px solid #ddd; cursor: pointer; }}
        th:hover {{ background: #f0f0f0; }}
        td {{ padding: 12px; border-bottom: 1px solid #eee; }}
        tr:hover {{ background: #f9f9f9; }}
        .badge {{ display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 0.85em; font-weight: 600; }}
        .badge.critical {{ background: #ffe0e0; color: #c00; }}
        .badge.high {{ background: #fff3cd; color: #856404; }}
        .badge.normal {{ background: #e7f3ff; color: #004085; }}
        .status {{ display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 0.85em; font-weight: 600; }}
        .status.todo {{ background: #f1f3f5; color: #495057; }}
        .status.in_progress {{ background: #cfe9ff; color: #0066cc; }}
        .status.done {{ background: #d3f9d8; color: #2b8a3e; }}
        .hidden {{ display: none; }}
        .no-results {{ text-align: center; padding: 40px; color: #999; }}
        .footer {{ padding: 20px; background: #f9f9f9; text-align: center; color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Отчёт по задачам</h1>
            <p>{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</p>
        </div>

        <div class="stats">
            <div class="stat"><div class="stat-num">{stats['total']}</div><div class="stat-label">Всего</div></div>
            <div class="stat critical"><div class="stat-num">{stats['critical']}</div><div class="stat-label">🔴 Критичные</div></div>
            <div class="stat high"><div class="stat-num">{stats['high']}</div><div class="stat-label">⚠️ Высокий</div></div>
            <div class="stat"><div class="stat-num">{stats['progress']}</div><div class="stat-label">🔵 В работе</div></div>
            <div class="stat"><div class="stat-num">{stats['todo']}</div><div class="stat-label">📋 К выполнению</div></div>
            <div class="stat"><div class="stat-num">{stats['done']}</div><div class="stat-label">✅ Завершено</div></div>
        </div>

        <div class="controls">
            <div class="control-group">
                <label>Приоритет:</label>
                <select id="p" onchange="filter()"><option value="">Все</option><option value="critical">Критичные</option><option value="high">Высокий</option><option value="normal">Обычный</option></select>
            </div>
            <div class="control-group">
                <label>Статус:</label>
                <select id="s" onchange="filter()"><option value="">Все</option><option value="todo">К выполнению</option><option value="in_progress">В работе</option><option value="done">Завершено</option></select>
            </div>
            <div class="control-group">
                <label>Поиск:</label>
                <input type="text" id="q" placeholder="Название..." onkeyup="filter()">
            </div>
            <button onclick="reset()">Сбросить</button>
        </div>

        <div class="table-wrapper">
            <table id="t">
                <thead><tr><th onclick="sort(0)">Название</th><th onclick="sort(1)">Приоритет</th><th onclick="sort(2)">Статус</th><th onclick="sort(3)">Срок</th><th onclick="sort(4)">Часы</th><th onclick="sort(5)">Модуль</th></tr></thead>
                <tbody id="b"></tbody>
            </table>
            <div id="nr" class="no-results hidden">😕 Нет задач</div>
        </div>

        <div class="footer">AI Core Task Manager • {datetime.now().strftime('%Y-%m-%d')}</div>
    </div>

    <script>
        const data = {tasks_str};
        let sortBy = null, sortDir = 'asc';

        function render() {{
            let p = document.getElementById('p').value;
            let s = document.getElementById('s').value;
            let q = document.getElementById('q').value.toLowerCase();

            let filtered = data.filter(x => 
                (!p || x.priority === p) &&
                (!s || x.status === s) &&
                (!q || x.title.toLowerCase().includes(q))
            );

            if (sortBy !== null) {{
                const keys = ['title', 'priority', 'status', 'due', 'hours', 'module'];
                const key = keys[sortBy];
                filtered.sort((a, b) => {{
                    let av = a[key], bv = b[key];
                    if (typeof av === 'number') return sortDir === 'asc' ? av - bv : bv - av;
                    av = String(av).toLowerCase();
                    bv = String(bv).toLowerCase();
                    let cmp = av.localeCompare(bv);
                    return sortDir === 'asc' ? cmp : -cmp;
                }});
            }}

            let html = '';
            filtered.forEach(x => {{
                html += `<tr><td>${{x.title}}</td><td><span class="badge ${{x.priority}}">${{x.priority}}</span></td><td><span class="status ${{x.status}}">${{x.status}}</span></td><td>${{x.due}}</td><td>${{x.hours}}h</td><td><code>${{x.module}}</code></td></tr>`;
            }});

            if (filtered.length === 0) {{
                document.getElementById('t').classList.add('hidden');
                document.getElementById('nr').classList.remove('hidden');
            }} else {{
                document.getElementById('t').classList.remove('hidden');
                document.getElementById('nr').classList.add('hidden');
            }}

            document.getElementById('b').innerHTML = html;
        }}

        function filter() {{ render(); }}
        function sort(i) {{ sortBy = (sortBy === i) ? null : i; sortDir = sortBy === i && sortDir === 'asc' ? 'desc' : 'asc'; render(); }}
        function reset() {{ document.getElementById('p').value = ''; document.getElementById('s').value = ''; document.getElementById('q').value = ''; sortBy = null; render(); }}

        render();
    </script>
</body>
</html>
"""

# Save
with open('tasks_report.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Report generated: tasks_report.html")
