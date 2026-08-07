from fastapi import FastAPI

app = FastAPI(title="Comments Service")

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.get('/comments')
def list_comments():
    return [{'id': 1, 'post_id': 1, 'text': 'Nice post!'}]

@app.post('/comments')
def create_comment():
    return {'id': 2, 'post_id': 1, 'text': 'Great read!'}
