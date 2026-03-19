import json
from datetime import datetime
from pathlib import Path

# Создаём папку для отчётов
Path('reports').mkdir(exist_ok=True)

with open('AI_Core_Tasks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

tasks = [e for e in data['entities'] if e['type'] == 'task']

# Преобразуем в удобный формат
tasks_data = []
for t in tasks:
    due = t['props'].get('due', '')
    is_overdue = False
    if due:
        try:
            if datetime.fromisoformat(due) < datetime.now():
                is_overdue = True
        except:
            pass
    
    tasks_data.append({
        'title': t['title'],
        'status': t['props'].get('status', 'unknown'),
        'priority': t['props'].get('priority', 'normal'),
        'due': due or 'нет срока',
        'est_hours': t['props'].get('est_hours', 0),
        'module': t['props'].get('module', 'N/A'),
        'is_overdue': is_overdue,
        'description': t['props'].get('description', '')[:100] + '...' if t['props'].get('description') else ''
    })

# HTML шаблон
html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 Анализ задач</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
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
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .stat-card.critical {{
            border-left-color: #ff6b6b;
        }}
        
        .stat-card.warning {{
            border-left-color: #ffa94d;
        }}
        
        .stat-card.success {{
            border-left-color: #51cf66;
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-card.critical .stat-number {{
            color: #ff6b6b;
        }}
        
        .stat-card.warning .stat-number {{
            color: #ffa94d;
        }}
        
        .stat-card.success .stat-number {{
            color: #51cf66;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9em;
            margin-top: 8px;
        }}
        
        .controls {{
            padding: 30px;
            background: white;
            border-bottom: 1px solid #eee;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}
        
        .control-group {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}
        
        .control-group label {{
            font-weight: 600;
            color: #333;
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
        }}
        
        .filter-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.3s;
        }}
        
        .filter-btn:hover {{
            background: #764ba2;
        }}
        
        .filter-btn.reset {{
            background: #999;
        }}
        
        .filter-btn.reset:hover {{
            background: #777;
        }}
        
        .table-wrapper {{
            overflow-x: auto;
            padding: 30px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95em;
        }}
        
        th {{
            background: #f8f9fa;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #ddd;
            cursor: pointer;
            user-select: none;
            color: #333;
        }}
        
        th:hover {{
            background: #e9ecef;
        }}
        
        th.sortable::after {{
            content: ' ↕️';
            font-size: 0.8em;
            opacity: 0.5;
        }}
        
        th.sortable.asc::after {{
            content: ' ↑';
            opacity: 1;
        }}
        
        th.sortable.desc::after {{
            content: ' ↓';
            opacity: 1;
        }}
        
        td {{
            padding: 15px;
            border-bottom: 1px solid #eee;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        tr.hidden {{
            display: none;
        }}
        
        .priority {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85em;
        }}
        
        .priority.critical {{
            background: #ffe0e0;
            color: #c00;
        }}
        
        .priority.high {{
            background: #fff3cd;
            color: #856404;
        }}
        
        .priority.normal {{
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
        
        .overdue {{
            background: #ffe0e0 !important;
            font-weight: 600;
            color: #c00;
        }}
        
        .no-results {{
            text-align: center;
            padding: 40px;
            color: #999;
            font-size: 1.2em;
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
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .stats {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .controls {{
                flex-direction: column;
                align-items: stretch;
            }}
            
            .control-group {{
                flex-direction: column;
            }}
            
            .control-group label {{
                display: block;
                margin-bottom: 5px;
            }}
            
            select, input, .filter-btn {{
                width: 100%;
            }}
            
            table {{
                font-size: 0.8em;
            }}
            
            td, th {{
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Анализ задач проекта</h1>
            <p>Дата: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(tasks_data)}</div>
                <div class="stat-label">Всего задач</div>
            </div>
            <div class="stat-card critical">
                <div class="stat-number">{len([t for t in tasks_data if t['priority'] == 'critical'])}</div>
                <div class="stat-label">🔴 Критичные</div>
            </div>
            <div class="stat-card warning">
                <div class="stat-number">{len([t for t in tasks_data if t['priority'] == 'high'])}</div>
                <div class="stat-label">⚠️ Высокий приоритет</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len([t for t in tasks_data if t['status'] == 'in_progress'])}</div>
                <div class="stat-label">🔵 В работе</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len([t for t in tasks_data if t['status'] == 'todo'])}</div>
                <div class="stat-label">📋 К выполнению</div>
            </div>
            <div class="stat-card success">
                <div class="stat-number">{len([t for t in tasks_data if t['status'] == 'done'])}</div>
                <div class="stat-label">✅ Завершено</div>
            </div>
            <div class="stat-card warning">
                <div class="stat-number">{len([t for t in tasks_data if t['is_overdue']])}</div>
                <div class="stat-label">⏰ Просроченные</div>
            </div>
        </div>
        
        <div class="controls">
            <div class="control-group">
                <label>Приоритет:</label>
                <select id="priorityFilter">
                    <option value="">Все</option>
                    <option value="critical">🔴 Критичные</option>
                    <option value="high">⚠️ Высокий</option>
                    <option value="normal">ℹ️ Обычный</option>
                </select>
            </div>
            
            <div class="control-group">
                <label>Статус:</label>
                <select id="statusFilter">
                    <option value="">Все</option>
                    <option value="todo">📋 К выполнению</option>
                    <option value="in_progress">🔵 В работе</option>
                    <option value="done">✅ Завершено</option>
                </select>
            </div>
            
            <div class="control-group">
                <label>Модуль:</label>
                <select id="moduleFilter">
                    <option value="">Все</option>
                    {"".join([f'<option value="{m}">{m}</option>' for m in sorted(set(t["module"] for t in tasks_data))])}
                </select>
            </div>
            
            <div class="control-group">
                <label>Поиск:</label>
                <input type="text" id="searchInput" placeholder="Поиск по названию...">
            </div>
            
            <button class="filter-btn" onclick="resetFilters()">Сбросить фильтры</button>
        </div>
        
        <div class="table-wrapper">
            <table id="tasksTable">
                <thead>
                    <tr>
                        <th class="sortable" onclick="sortTable(0)">Название</th>
                        <th class="sortable" onclick="sortTable(1)">Приоритет</th>
                        <th class="sortable" onclick="sortTable(2)">Статус</th>
                        <th class="sortable" onclick="sortTable(3)">Срок</th>
                        <th class="sortable" onclick="sortTable(4)">Часы</th>
                        <th class="sortable" onclick="sortTable(5)">Модуль</th>
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
            Сгенерировано автоматически • Последнее обновление: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
        </div>
    </div>
    
    <script>
        const tasksData = {json.dumps(tasks_data)};
        let currentSort = {{ column: null, direction: 'asc' }};
        
        function renderTable() {{
            const tbody = document.getElementById('tasksBody');
            tbody.innerHTML = '';
            
            const filteredTasks = filterTasks();
            
            if (filteredTasks.length === 0) {{
                document.getElementById('noResults').style.display = 'block';
                document.getElementById('tasksTable').style.display = 'none';
                return;
            }}
            
            document.getElementById('noResults').style.display = 'none';
            document.getElementById('tasksTable').style.display = 'table';
            
            filteredTasks.forEach(task => {{
                const row = document.createElement('tr');
                if (task.is_overdue) row.classList.add('overdue');
                
                row.innerHTML = `
                    <td>${{task.title}}</td>
                    <td><span class="priority ${{task.priority}}">${{getPriorityEmoji(task.priority)}} ${{task.priority}}</span></td>
                    <td><span class="status ${{task.status}}">${{getStatusEmoji(task.status)}} ${{formatStatus(task.status)}}</span></td>
                    <td>${{task.due}} ${{task.is_overdue ? '⏰' : ''}}</td>
                    <td>${{task.est_hours}}ч</td>
                    <td><code>${{task.module}}</code></td>
                `;
                tbody.appendChild(row);
            }});
        }}
        
        function filterTasks() {{
            const priority = document.getElementById('priorityFilter').value;
            const status = document.getElementById('statusFilter').value;
            const module = document.getElementById('moduleFilter').value;
            const search = document.getElementById('searchInput').value.toLowerCase();
            
            let filtered = tasksData.filter(task => {{
                const matchPriority = !priority || task.priority === priority;
                const matchStatus = !status || task.status === status;
                const matchModule = !module || task.module === module;
                const matchSearch = !search || task.title.toLowerCase().includes(search);
                
                return matchPriority && matchStatus && matchModule && matchSearch;
            }});
            
            if (currentSort.column !== null) {{
                filtered.sort((a, b) => {{
                    const keys = ['title', 'priority', 'status', 'due', 'est_hours', 'module'];
                    const key = keys[currentSort.column];
                    
                    let aVal = a[key];
                    let bVal = b[key];
                    
                    if (typeof aVal === 'number') {{
                        return currentSort.direction === 'asc' ? aVal - bVal : bVal - aVal;
                    }}
                    
                    aVal = String(aVal).toLowerCase();
                    bVal = String(bVal).toLowerCase();
                    
                    if (currentSort.direction === 'asc') {{
                        return aVal.localeCompare(bVal);
                    }} else {{
                        return bVal.localeCompare(aVal);
                    }}
                }});
            }}
            
            return filtered;
        }}
        
        function sortTable(column) {{
            const headers = document.querySelectorAll('th');
            headers.forEach(h => h.classList.remove('asc', 'desc'));
            
            if (currentSort.column === column) {{
                currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
            }} else {{
                currentSort.column = column;
                currentSort.direction = 'asc';
            }}
            
            headers[column].classList.add(currentSort.direction);
            renderTable();
        }}
        
        function resetFilters() {{
            document.getElementById('priorityFilter').value = '';
            document.getElementById('statusFilter').value = '';
            document.getElementById('moduleFilter').value = '';
            document.getElementById('searchInput').value = '';
            currentSort = {{ column: null, direction: 'asc' }};
            document.querySelectorAll('th').forEach(h => h.classList.remove('asc', 'desc'));
            renderTable();
        }}
        
        function getPriorityEmoji(priority) {{
            const map = {{ critical: '🔴', high: '⚠️', normal: 'ℹ️' }};
            return map[priority] || '';
        }}
        
        function getStatusEmoji(status) {{
            const map = {{ todo: '📋', in_progress: '🔵', done: '✅' }};
            return map[status] || '';
        }}
        
        function formatStatus(status) {{
            const map = {{ todo: 'К выполнению', in_progress: 'В работе', done: 'Завершено' }};
            return map[status] || status;
        }}
        
        document.getElementById('priorityFilter').addEventListener('change', renderTable);
        document.getElementById('statusFilter').addEventListener('change', renderTable);
        document.getElementById('moduleFilter').addEventListener('change', renderTable);
        document.getElementById('searchInput').addEventListener('input', renderTable);
        
        renderTable();
    </script>
</body>
</html>
"""

# Сохраняем HTML
with open('reports/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ HTML-отчёт создан: reports/index.html")
