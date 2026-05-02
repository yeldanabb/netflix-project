import pandas as pd
from app.database import SessionLocal, engine
from app import models
models.Base.metadata.create_all(bind=engine)

def load_csv_to_db(file_path: str):
    df = pd.read_csv(file_path)
    df['director'] = df['director'].fillna('')
    df['cast'] = df['cast'].fillna('')
    df['country'] = df['country'].fillna('')
    df['rating'] = df['rating'].fillna('')
    df['duration'] = df['duration'].fillna('')
    df['description'] = df['description'].fillna('')
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

    db = SessionLocal()
    ratings = set(df['rating'].dropna().unique())
    for rating_name in ratings:
        if not db.query(models.Rating).filter_by(name=rating_name).first():
            db.add(models.Rating(name=rating_name))
    db.commit()

    for _, row in df.iterrows():
        existing_movie = db.query(models.Movie).filter(
            models.Movie.show_id == str(row['show_id'])
        ).first()
        
        if existing_movie:
            continue 
        movie = models.Movie(
            show_id=row['show_id'],
            type=row['type'],
            title=row['title'],
            director=row['director'],
            cast=row['cast'],
            country=row['country'],
            date_added=row['date_added'].date() if pd.notnull(row['date_added']) else None,
            release_year=row['release_year'] if pd.notnull(row['release_year']) else None, 
            rating=row['rating'],
            duration=row['duration'],
            description=row['description']
        )
        db.add(movie)
        db.flush()
        categories = [c.strip() for c in row['listed_in'].split(',') if c.strip()]
        for category_name in categories:
            category = db.query(models.Category).filter_by(name=category_name).first()
            if not category:
                category = models.Category(name=category_name)
                db.add(category)
                db.flush()
            if category not in movie.categories:
                movie.categories.append(category)
    db.commit()
    db.close()