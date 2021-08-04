from sqlalchemy.orm import Session

import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).get(user_id)


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    new_user = models.User(email=user.email, password=user.password, name=user.name, gender=user.gender)
    db.add(new_user)
    db.commit()
    return new_user

def update_user(db: Session, db_user: schemas.User, user: schemas.UserUpdate):
    db_user.name = user.name
    db_user.gender = user.gender
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user: schemas.User):
    db.delete(user)
    db.commit()


def get_article(db: Session, article_id: int):
    return db.query(models.Article).get(article_id)


def get_articles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Article).offset(skip).limit(limit).all()


def create_article(db: Session, article: schemas.ArticleBase):
    new_article = models.Article(title=article.title, content=article.content, owner_id=article.owner_id)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


def update_article(db: Session, db_article: schemas.Article, article: schemas.ArticleUpdate):
    db_article.title = article.title
    db_article.content = article.content
    db.commit()
    db.enable_relationship_loading(db_article)
    return db_article


def delete_article(db: Session, article: schemas.Article):
    db.delete(article)
    db.commit()
