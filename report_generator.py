#!/usr/bin/env python3
import json
from datetime import datetime

print("[INFO] Starting report generator...")

# Читаем JSON
with open('AI_Core_Tasks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("[INFO] JSON loaded successfully")

# Фильтруем задачи
tasks = [e for e in data['entities'] if e['type'] == 'task']
print(f"[INFO] Found {len(tasks)} tasks")

# Считаем статистику
stats = {
    'total': len(tasks),
    'critical': len([t for t in tasks if t['props'].get('priority') == 'critical']),
    'high': len([t for t in tasks if t['props'].get('priority') == 'high']),
    'todo': len([t for t in tasks if t['props'].get('status') == 'todo']),
    'in_progress': len([t for t in tasks if t['props'].get('status') == 'in_progress']),
    'done': len([t for t in tasks if t['props'].get('status') == 'done']),
}

print(f"[INFO] Statistics: {stats}")

# Преобразуем в JSON для JS
import json as json_lib
tasks_json = []
for t in tasks:
    tasks_json.append({
        'title': t.get('title', 'Без названия'),
        'priority': t['props'].get('priority', 'normal'),
        'status': t['props'].get('status', 'todo'),
        'due': t['props'].get('due', '—'),
        'hours': t['props'].get('est_hours', 0),
        'module': t['props'].get('module', '—'),
    })

tasks_data_json = json_lib.dumps(tasks_json, ensure_ascii=False, indent=2)

# Создаём HTML
html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 Отчёт задач</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}

        .stat {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}

        .stat.critical {{ border-left-color: #ff6b6b; }}
        .stat.high {{ border-left-color: #ffa94d; }}

        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}

        .stat.critical .stat-number {{ color: #ff6b6b; }}
        .stat.high .stat-number {{ color: #ffa94d; }}

        .stat-label {{
            color: #666;
            font-size: 0.9em;
            margin-top: 8px;
        }}

        .controls {{
            padding: 20px 30px;
            background: white;
            border-bottom: 1px solid #eee;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}

        .control-group {{
            display: flex;
            gap: 8px;
            align-items: center;
        }}

        .control-group label {{
            font-weight: 600;
            color: #333;
            font-size: 0.95em;
        }}

        select, input {{
            padding: 8px 12px;
            border: 2px solid #ddd;
            border-radius: 6px;
            font-size: 0.95em;
            transition: border-color 0.3s;
        }}

        select:focus, input:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}

        button {{
            background: #667eea;
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.3s;
        }}

        button:hover {{
            background: #764ba2;
        }}

        button.secondary {{
            background: #999;
        }}

        button.secondary:hover {{
            background: #777;
        }}

        .table-container {{
            padding: 30px;
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95em;
        }}

        th {{
            background: #f8f9fa;
            padding: 12px 15px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #ddd;
            cursor: pointer;
            user-select: none;
        }}

        th:hover {{
            background: #e9ecef;
        }}

        th.sort-asc::after {{
            content: ' ↑';
            color: #667eea;
        }}

        th.sort-desc::after {{
            content: ' ↓';
            color: #667eea;
        }}

        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}

        tr:hover {{
            background: #f8f9fa;
        }}

        tr.hidden {{
            display: none;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85em;
        }}

        .badge.critical {{
            background: #ffe0e0;
            color: #c00;
        }}

        .badge.high {{
            background: #fff3cd;
            color: #856404;
        }}

        .badge.normal {{
            background: #e7f3ff;
            color: #004085;
        }}

        .status {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85em;
        }}

        .status.todo {{
            background: #f1f3f5;
            color: #495057;
        }}

        .status.in_progress {{
            background: #cfe9ff;
            color: #0066cc;
        }}

        .status.done {{
            background: #d3f9d8;
            color: #2b8a3e;
        }}

        .no-results {{
            text-align: center;
            padding: 40px;
            color: #999;
            font-size: 1.1em;
        }}

        .footer {{
            padding: 20px 30px;
            background: #f8f9fa;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}

        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.8em; }}
            .stats {{ grid-template-columns: repeat(2, 1fr); }}
            .controls {{ flex-direction: column; align-items: stretch; }}
            .control-group {{ flex-direction: column; }}
            .control-group label {{ display: block; margin-bottom: 5px; }}
            select, input, button {{ width: 100%; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Отчёт по задачам</h1>
            <p>Сгенерировано: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</p>
        </div>

        <div class="stats">
            <div class="stat">
                <div class="stat-number">{stats['total']}</div>
                <div class="stat-label">Всего задач</div>
            </div>
            <div class="stat critical">
                <div class="stat-number">{stats['critical']}</div>
                <div class="stat-label">🔴 Критичные</div>
            </div>
            <div class="stat high">
                <div class="stat-number">{stats['high']}</div>
                <div class="stat-label">⚠️ Высокий приоритет</div>
            </div>
            <div class="stat">
                <div class="stat-number">{stats['in_progress']}</div>
                <div class="stat-label">🔵 В работе</div>
            </div>
            <div class="stat">
                <div class="stat-number">{stats['todo']}</div>
                <div class="stat-label">📋 К выполнению</div>
            </div>
            <div class="stat">
                <div class="stat-number">{stats['done']}</div>
                <div class="stat-label">✅ Завершено</div>
            </div>
        </div>

        <div class="controls">
            <div class="control-group">
                <label>Приоритет:</label>
                <select onchange="filterTable()">
                    <option value="">Все</option>
                    <option value="critical">🔴 Критичные</option>
                    <option value="high">⚠️ Высокий</option>
                    <option value="normal">ℹ️ Обычный</option>
                </select>
            </div>
            <div class="control-group">
                <label>Статус:</label>
                <select onchange="filterTable()">
                    <option value="">Все</option>
                    <option value="todo">📋 К ��ыполнению</option>
                    <option value="in_progress">🔵 В работе</option>
                    <option value="done">✅ Завершено</option>
                </select>
            </div>
            <div class="control-group">
                <label>Поиск:</label>
                <input type="text" id="search" placeholder="Название задачи..." onkeyup="filterTable()">
            </div>
            <button class="secondary" onclick="resetFilters()">Сбросить</button>
        </div>

        <div class="table-container">
            <table id="tasksTable">
                <thead>
                    <tr>
                        <th onclick="sortTable(0)">Название</th>
                        <th onclick="sortTable(1)">Приоритет</th>
                        <th onclick="sortTable(2)">Статус</th>
                        <th onclick="sortTable(3)">Срок</th>
                        <th onclick="sortTable(4)">Часы</th>
                        <th onclick="sortTable(5)">Модуль</th>
                    </tr>
                </thead>
                <tbody id="tasksBody">
                </tbody>
            </table>
            <div id="noResults" class="no-results" style="display:none;">
                😕 Задачи не найдены
            </div>
        </div>

        <div class="footer">
            <p>Интерактивный отчёт • AI Core Tasks Manager</p>
        </div>
    </div>

    <script>
        const tasksData = {tasks_data_json};
        let currentSort = {{ col: null, dir: 'asc' }};

        function renderTable() {{
            const tbody = document.getElementById('tasksBody');
            tbody.innerHTML = '';

            const filtered = getFilteredTasks();

            if (filtered.length === 0) {{
                document.getElementById('noResults').style.display = 'block';
                document.getElementById('tasksTable').style.display = 'none';
                return;
            }}

            document.getElementById('noResults').style.display = 'none';
            document.getElementById('tasksTable').style.display = 'table';

            filtered.forEach(task => {{
                const row = `
                    <tr>
                        <td>${{task.title}}</td>
                        <td><span class="badge ${{task.priority}}">${{task.priority}}</span></td>
                        <td><span class="status ${{task.status}}">${{task.status}}</span></td>
                        <td>${{task.due}}</td>
                        <td>${{task.hours}}ч</td>
                        <td><code>${{task.module}}</code></td>
                    </tr>
                `;
                tbody.innerHTML += row;
            }});
        }}

        function getFilteredTasks() {{
            const priority = document.querySelectorAll('select')[0].value;
            const status = document.querySelectorAll('select')[1].value;
            const search = document.getElementById('search').value.toLowerCase();

            let filtered = tasksData.filter(t => {{
                const matchP = !priority || t.priority === priority;
                const matchS = !status || t.status === status;
                const matchT = !search || t.title.toLowerCase().includes(search);
                return matchP && matchS && matchT;
            }});

            if (currentSort.col !== null) {{
                filtered.sort((a, b) => {{
                    const keys = ['title', 'priority', 'status', 'due', 'hours', 'module'];
                    const key = keys[currentSort.col];
                    let aVal = a[key];
                    let bVal = b[key];

                    if (typeof aVal === 'number') {{
                        return currentSort.dir === 'asc' ? aVal - bVal : bVal - aVal;
                    }}

                    aVal = String(aVal).toLowerCase();
                    bVal = String(bVal).toLowerCase();
                    const cmp = aVal.localeCompare(bVal);
                    return currentSort.dir === 'asc' ? cmp : -cmp;
                }});
            }}

            return filtered;
        }}

        function filterTable() {{
            renderTable();
        }}

        function sortTable(col) {{
            const headers = document.querySelectorAll('th');
            headers.forEach(h => h.classList.remove('sort-asc', 'sort-desc'));

            if (currentSort.col === col) {{
                currentSort.dir = currentSort.dir === 'asc' ? 'desc' : 'asc';
            }} else {{
                currentSort.col = col;
                currentSort.dir = 'asc';
            }}

            if (headers[col]) {{
                headers[col].classList.add(`sort-${{currentSort.dir}}`);
            }}

            renderTable();
        }}

        function resetFilters() {{
            document.querySelectorAll('select').forEach(s => s.value = '');
            document.getElementById('search').value = '';
            currentSort = {{ col: null, dir: 'asc' }};
            document.querySelectorAll('th').forEach(h => h.classList.remove('sort-asc', 'sort-desc'));
            renderTable();
        }}

        renderTable();
    </script>
</body>
</html>
"""

# Сохраняем
with open('report.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("[INFO] ✅ Report saved to report.html")
print("[INFO] Done!")
