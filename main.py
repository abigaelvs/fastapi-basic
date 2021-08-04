from fastapi import FastAPI, Depends, HTTPException, Query

from typing import List, Optional

from sqlalchemy.orm import Session


import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/{email}/", response_model=schemas.User)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="Email not found!")
    return user


@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")
    return crud.update_user(db=db, db_user=db_user, user=user)


@app.delete("/users/{item_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user:
        crud.delete_user(db=db, user=user)
        raise HTTPException(status_code=200, detail="User Deleted!")
    raise HTTPException(status_code=404, detail="User not found!")


@app.get("/articles/", response_model=List[schemas.Article])
def get_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    articles = crud.get_articles(db, skip=skip, limit=limit)
    return articles


@app.get("/article/{article_id}", response_model=schemas.Article)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = crud.get_article(db=db, article_id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@app.post("/article", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    new_article = crud.create_article(db=db, article=article)
    return new_article

@app.put("/article/{article_id}", response_model=schemas.Article)
def update_article(article_id: int ,article: schemas.ArticleUpdate, db: Session = Depends(get_db)):
    db_article = crud.get_article(db=db, article_id=article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found!")
    return crud.update_article(db=db, db_article=db_article, article=article)


@app.delete("/article/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = crud.get_article(db=db, article_id=article_id)
    if article:
        crud.delete_article(db=db, article=article)
        raise HTTPException(status_code=200, detail="Article has been deleted!")
    raise HTTPException(status_code=404, detail="Article not found!")