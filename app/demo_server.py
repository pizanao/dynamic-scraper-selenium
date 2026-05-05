from flask import Flask, jsonify, request, redirect, make_response


def items():
    cats = ["HR", "Operations", "Analytics", "Security"]
    return [
        {"id": f"ITEM-{i:03d}", "title": f"Workforce Signal {i:03d}", "category": cats[i % 4],
         "price": round(19.9 + i * 1.37, 2), "rating": round(3.5 + (i % 15) / 10, 1), "url": f"/items/ITEM-{i:03d}"}
        for i in range(1, 49)
    ]


def create_app():
    app = Flask(__name__)
    data = items()

    @app.get('/')
    def root():
        return redirect('/login')

    @app.get('/login')
    def login():
        return '''<html><body><h1>Dynamic Demo Portal</h1><form method="post" action="/login"><input id="username" name="username" placeholder="username" value="demo"/><input id="password" name="password" placeholder="password" type="password" value="demo"/><button id="login-button">Login</button></form></body></html>'''

    @app.post('/login')
    def do_login():
        r = make_response(redirect('/feed'))
        r.set_cookie('session', 'ok')
        return r

    @app.get('/feed')
    def feed():
        return '''<html><head><title>Dynamic Feed</title><style>body{font-family:system-ui;margin:40px;background:#0f172a;color:#e2e8f0}.product-card{background:#111827;border:1px solid #334155;border-radius:16px;padding:16px;margin:12px 0}.title{font-size:18px;font-weight:700;color:#93c5fd}</style></head><body><h1>Dynamic Product Feed</h1><p id="status">Loading...</p><main id="feed"></main><script>let page=1,loading=false;async function loadMore(){if(loading)return;loading=true;const r=await fetch(`/api/feed?page=${page}&page_size=8`);const p=await r.json();const f=document.querySelector('#feed');p.items.forEach(item=>{const c=document.createElement('article');c.className='product-card';c.setAttribute('data-role','product-card');c.setAttribute('data-id',item.id);c.innerHTML=`<a class="title" data-field="title" href="${item.url}">${item.title}</a><div class="category" data-field="category">${item.category}</div><div class="price" data-field="price">$${item.price}</div><div class="rating" data-field="rating">${item.rating}</div>`;f.appendChild(c)});document.querySelector('#status').textContent=`Loaded ${document.querySelectorAll('.product-card').length} records`;page++;loading=false;}window.addEventListener('scroll',()=>{if(window.innerHeight+window.scrollY>=document.body.offsetHeight-100)loadMore()});loadMore();</script></body></html>'''

    @app.get('/api/feed')
    def api():
        page = int(request.args.get('page', 1))
        size = int(request.args.get('page_size', 8))
        start = (page - 1) * size
        end = start + size
        return jsonify({"items": data[start:end], "page": page, "has_next": end < len(data)})

    return app


def run(host='127.0.0.1', port=5000):
    create_app().run(host=host, port=port, debug=False)
