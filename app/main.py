from fastapi import FastAPI, Depends , HTTPException , BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from jose import JWTError, jwt
from .services.wiki import search_wikipedia
from .services.background import tag_article
from sqlalchemy.orm import joinedload
from fastapi.middleware.cors import CORSMiddleware


from .database import engine, SessionLocal
from . import models, schemas
from .auth import hash_password , verify_password, create_access_token
from .models import User
from fastapi.middleware.cors import CORSMiddleware


SECRET_KEY = "dev-secret"  
ALGORITHM = "HS256"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@app.get("/")
def home():
    return { "Personal Article Bookmark Tool "}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/auth/register", response_model=schemas.UserRead)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if len(user.password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password too long"
        )
    user.password =user.password[:72]
    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/auth/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


@app.post("/articles", response_model=schemas.ArticleRead)
def save_article(
    article: schemas.ArticleCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_article = models.Article(
        title=article.title,
        url=article.url,
        owner_id=current_user.id
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)

    background_tasks.add_task(
        tag_article,
        db_article.id
    )

    return db_article

@app.get("/articles", response_model=list[schemas.ArticleRead])
def get_articles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    articles = (
        db.query(models.Article)
        .options(joinedload(models.Article.tags))
        .filter(models.Article.owner_id == current_user.id)
        .all()
    )
    return articles

@app.get("/search")
async def search_articles(q: str, limit: int = 5):
    results = await search_wikipedia(q, limit)
    return {
        "query": q,
        "count": len(results),
        "results": results
    }

@app.put("/articles/{article_id}/tags")
def update_article_tags(
    article_id: int,
    tag_data: schemas.TagUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Fetch article
    article = (
        db.query(models.Article)
        .filter(
            models.Article.id == article_id,
            models.Article.owner_id == current_user.id
        )
        .first()
    )

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # 2. Clear existing tags
    article.tags.clear()

    # 3. Attach new tags
    for tag_name in tag_data.tags:
        tag = db.query(models.Tag).filter_by(name=tag_name).first()
        if not tag:
            tag = models.Tag(name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)

        article.tags.append(tag)

    db.commit()
    return {"message": "Tags updated successfully"}



