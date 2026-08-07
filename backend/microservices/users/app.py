from fastapi import FastAPI

app = FastAPI(title="Users Service")

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.get('/users')
def list_users():
    return [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
