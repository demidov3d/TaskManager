import json
from datetime import datetime

with open('AI_Core_Tasks.json', encoding='utf-8') as f:
    data = json.load(f)

tasks = [e for e in data['entities'] if e['type'] == 'task']
stats = {
    'total': len(tasks),
    'crit': len([t for t in tasks if t['props'].get('priority') == 'critical']),
    'high': len([t for t in tasks if t['props'].get('priority') == 'high']),
    'todo': len([t for t in tasks if t['props'].get('status') == 'todo']),
    'prog': len([t for t in tasks if t['props'].get('status') == 'in_progress']),
    'done': len([t for t in tasks if t['props'].get('status') == 'done']),
}

items = []
for t in tasks:
    items.append({
        'title': t.get('title', 'N/A'),
        'priority': t['props'].get('priority', 'normal'),
        'status': t['props'].get('status', 'todo'),
        'due': t['props'].get('due', '—'),
        'hours': t['props'].get('est_hours', 0),
        'module': t['props'].get('module', '—'),
    })

import json as j
data_js = j.dumps(items, ensure_ascii=False)

html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Tasks</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:system-ui;background:#f5f5f5;padding:20px}}
.box{{max-width:1200px;margin:0 auto;background:white;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}}
.top{{background:#667eea;color:white;padding:30px;text-align:center}}
.top h1{{font-size:2em;margin-bottom:10px}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:15px;padding:30px;background:#f9f9f9}}
.s{{background:white;padding:20px;border-radius:8px;border-left:4px solid #667eea;text-align:center}}
.s.red{{border-left-color:#ff6b6b}}
.s.orange{{border-left-color:#ffa94d}}
.num{{font-size:2em;font-weight:bold;color:#667eea}}
.s.red .num{{color:#ff6b6b}}
.s.orange .num{{color:#ffa94d}}
.label{{color:#666;font-size:0.9em;margin-top:8px}}
.ctrl{{padding:20px 30px;display:flex;gap:15px;flex-wrap:wrap;border-bottom:1px solid #eee}}
.cg{{display:flex;gap:8px;align-items:center}}
.cg label{{font-weight:600}}
select,input{{padding:8px 12px;border:1px solid #ddd;border-radius:4px}}
button{{padding:8px 16px;background:#667eea;color:white;border:none;border-radius:4px;cursor:pointer}}
button:hover{{background:#5568d3}}
.tbl{{padding:30px;overflow-x:auto}}
table{{width:100%;border-collapse:collapse}}
th{{background:#f9f9f9;padding:12px;text-align:left;font-weight:600;border-bottom:2px solid #ddd;cursor:pointer}}
th:hover{{background:#f0f0f0}}
td{{padding:12px;border-bottom:1px solid #eee}}
tr:hover{{background:#f9f9f9}}
.bd{{display:inline-block;padding:4px 12px;border-radius:12px;font-size:0.85em;font-weight:600}}
.bd.critical{{background:#ffe0e0;color:#c00}}
.bd.high{{background:#fff3cd;color:#856404}}
.bd.normal{{background:#e7f3ff;color:#004085}}
.st{{display:inline-block;padding:4px 12px;border-radius:12px;font-size:0.85em;font-weight:600}}
.st.todo{{background:#f1f3f5;color:#495057}}
.st.in_progress{{background:#cfe9ff;color:#0066cc}}
.st.done{{background:#d3f9d8;color:#2b8a3e}}
.hide{{display:none}}
.nr{{text-align:center;padding:40px;color:#999}}
.bot{{padding:20px;background:#f9f9f9;text-align:center;color:#666;font-size:0.9em}}
</style>
</head>
<body>
<div class="box">
<div class="top">
<h1>📊 Tasks</h1>
<p>{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</p>
</div>
<div class="stats">
<div class="s"><div class="num">{stats['total']}</div><div class="label">Total</div></div>
<div class="s red"><div class="num">{stats['crit']}</div><div class="label">Critical</div></div>
<div class="s orange"><div class="num">{stats['high']}</div><div class="label">High</div></div>
<div class="s"><div class="num">{stats['prog']}</div><div class="label">In Progress</div></div>
<div class="s"><div class="num">{stats['todo']}</div><div class="label">Todo</div></div>
<div class="s"><div class="num">{stats['done']}</div><div class="label">Done</div></div>
</div>
<div class="ctrl">
<div class="cg"><label>Priority:</label><select id="p" onchange="f()"><option value="">All</option><option value="critical">Critical</option><option value="high">High</option><option value="normal">Normal</option></select></div>
<div class="cg"><label>Status:</label><select id="s" onchange="f()"><option value="">All</option><option value="todo">Todo</option><option value="in_progress">In Progress</option><option value="done">Done</option></select></div>
<div class="cg"><label>Search:</label><input type="text" id="q" placeholder="Title..." onkeyup="f()"></div>
<button onclick="r()">Reset</button>
</div>
<div class="tbl">
<table id="t">
<thead><tr><th>Title</th><th>Priority</th><th>Status</th><th>Due</th><th>Hours</th><th>Module</th></tr></thead>
<tbody id="b"></tbody>
</table>
<div id="n" class="nr hide">No tasks</div>
</div>
<div class="bot">Task Manager</div>
</div>
<script>
const d={data_js};
function f(){{
let p=document.getElementById('p').value;
let s=document.getElementById('s').value;
let q=document.getElementById('q').value.toLowerCase();
let x=d.filter(t=>(p===''||t.priority===p)&&(s===''||t.status===s)&&(q===''||t.title.toLowerCase().includes(q)));
let h='';
if(x.length===0){{document.getElementById('t').classList.add('hide');document.getElementById('n').classList.remove('hide')}}else{{document.getElementById('t').classList.remove('hide');document.getElementById('n').classList.add('hide');x.forEach(t=>{{h+=`<tr><td>${{t.title}}</td><td><span class="bd ${{t.priority}}">${{t.priority}}</span></td><td><span class="st ${{t.status}}">${{t.status}}</span></td><td>${{t.due}}</td><td>${{t.hours}}h</td><td>${{t.module}}</td></tr>`}})}}
document.getElementById('b').innerHTML=h;
}}
function r(){{document.getElementById('p').value='';document.getElementById('s').value='';document.getElementById('q').value='';f()}}
f();
</script>
</body>
</html>
'''

with open('out.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("OK")
