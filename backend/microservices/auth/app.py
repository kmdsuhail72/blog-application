from fastapi import FastAPI

app = FastAPI(title="Auth Service")

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/login')
def login():
    return {'access_token': 'fake-token', 'token_type': 'bearer'}

@app.post('/refresh')
def refresh():
    return {'access_token': 'new-token', 'token_type': 'bearer'}
