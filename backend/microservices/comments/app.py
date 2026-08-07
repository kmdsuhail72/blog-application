from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Path, Query

from schemas import Comment, CommentCreate, CommentUpdate

app = FastAPI(title="Comments Service")

comments: List[Comment] = []
next_comment_id = 1

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.get('/comments', response_model=List[Comment])
def list_comments(
    post_id: Optional[int] = Query(None, description='Filter comments by post ID'),
    author_id: Optional[int] = Query(None, description='Filter comments by author ID'),
):
    results = comments
    if post_id is not None:
        results = [comment for comment in results if comment.post_id == post_id]
    if author_id is not None:
        results = [comment for comment in results if comment.author_id == author_id]
    return results

@app.get('/comments/{comment_id}', response_model=Comment)
def get_comment(comment_id: int = Path(..., description='The ID of the comment to retrieve')):
    for comment in comments:
        if comment.id == comment_id:
            return comment
    raise HTTPException(status_code=404, detail='Comment not found')

@app.post('/comments', response_model=Comment, status_code=201)
def create_comment(payload: CommentCreate):
    global next_comment_id
    comment = Comment(
        id=next_comment_id,
        post_id=payload.post_id,
        author_id=payload.author_id,
        text=payload.text,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    comments.append(comment)
    next_comment_id += 1
    return comment

@app.put('/comments/{comment_id}', response_model=Comment)
def update_comment(
    payload: CommentUpdate,
    comment_id: int = Path(..., description='The ID of the comment to update'),
):
    for index, comment in enumerate(comments):
        if comment.id == comment_id:
            updated = comment.copy(update={
                'text': payload.text if payload.text is not None else comment.text,
                'updated_at': datetime.utcnow(),
            })
            comments[index] = updated
            return updated
    raise HTTPException(status_code=404, detail='Comment not found')

@app.delete('/comments/{comment_id}', status_code=204)
def delete_comment(comment_id: int = Path(..., description='The ID of the comment to delete')):
    for index, comment in enumerate(comments):
        if comment.id == comment_id:
            comments.pop(index)
            return
    raise HTTPException(status_code=404, detail='Comment not found')
