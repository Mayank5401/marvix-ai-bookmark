from app.database import SessionLocal
from app import models
from .tagger import generate_tags
from .wiki_categories import get_wikipedia_categories

async def tag_article(article_id: int):
    db = SessionLocal()
    try:
        article = db.get(models.Article, article_id)
        if not article:
            return

        categories = await get_wikipedia_categories(article.title)

        for name in categories:
            tag = db.query(models.Tag).filter_by(name=name).first()
            if not tag:
                tag = models.Tag(name=name)
                db.add(tag)
                db.commit()
                db.refresh(tag)

            article.tags.append(tag)

        db.commit()
    finally:
        db.close()


