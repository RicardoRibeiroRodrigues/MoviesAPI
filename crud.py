from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        username=user.username, password=fake_hashed_password, fullname=user.fullname
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_movies(db: Session):
    return db.query(models.Movie).all()


def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.movie_id == movie_id).first()


def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(
        title=movie.title,
        studio=movie.studio,
        description=movie.description,
        year=movie.year,
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def delete_movie(db: Session, movie_id: int):
    db_movie = db.query(models.Movie).filter(models.Movie.movie_id == movie_id).first()
    if not db_movie:
        return None
    db.delete(db_movie)
    db.commit()
    return db_movie


# TODO: Ver se aqui deveria ser MovieCreate ou Movie mesmo
def update_movie(db: Session, movie_id: int, updated: schemas.MovieCreate):
    db_movie = db.query(models.Movie).filter(models.Movie.movie_id == movie_id).first()
    if not db_movie:
        return None
    db_movie.title = updated.title
    db_movie.studio = updated.studio
    db_movie.description = updated.description
    db_movie.year = updated.year
    db.commit()
    db.refresh(db_movie)
    return db_movie


def create_movie_review(
    db: Session, review: schemas.MovieReviewCreate, user_id: int, movie_id: int
):
    db_review = models.MovieReview(
        n_stars=review.n_stars, review=review.review, user_id=user_id, movie_id=movie_id
    )
    if not db_review:
        return None
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_movie_reviews(db: Session, movie_id: int) -> list[schemas.MovieReview]:
    return (
        db.query(models.MovieReview)
        .filter(models.MovieReview.movie_id == movie_id)
        .all()
    )


def update_movie_review(
    db: Session, review_id: int, updated: schemas.MovieReviewCreate
):
    db_review = (
        db.query(models.MovieReview)
        .filter(models.MovieReview.review_id == review_id)
        .first()
    )
    if not db_review:
        return None
    db_review.n_stars = updated.n_stars
    db_review.review = updated.review
    db.commit()
    db.refresh(db_review)
    return db_review


def delete_movie_review(db: Session, review_id: int):
    db_review = (
        db.query(models.MovieReview)
        .filter(models.MovieReview.review_id == review_id)
        .first()
    )
    if not db_review:
        return None
    db.delete(db_review)
    db.commit()
    return db_review
