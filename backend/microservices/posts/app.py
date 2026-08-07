from fastapi import FastAPI

app = FastAPI(title="Posts Service")

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.get('/posts')
def list_posts():
    return [{'id': 1, 'title': 'Hello'}]

@app.post('/posts')
def create_post():
    return {'id': 2, 'title': 'New post'}
