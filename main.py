from typing import Annotated
from schemas import *
from fastapi import FastAPI, Path, HTTPException, Response, status, Body, Depends
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# This is used to document the 404 response for all endpoints that can raise it.
RESPONSES_NOT_FOUND = {
    404: {
        "description": "Item not found in the database",
    }
}


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return "Hello World, please check the /docs for info on using this API."


@app.post("/users/", tags=["users"], status_code=201)
def create_user(
    user: Annotated[UserCreate, Body(description="User JSON to add to the database")],
    response: Response,
    db: Session = Depends(get_db),
) -> schemas.User:
    """
    Receive a **User** object as json and add it to the database, returns the created user id on database.
    """
    user = crud.create_user(db, user)
    response.status_code = status.HTTP_201_CREATED
    response.headers["Location"] = f"/users/{user.user_id}"
    return user


@app.get("/movies/", tags=["movies"])
def get_movies(db: Session = Depends(get_db)) -> list[schemas.Movie]:
    """
    Get the list of the all **movies** in the database.
    """
    return crud.get_movies(db)


@app.post("/movies/", tags=["movies"], status_code=201)
def create_movie(
    movie: Annotated[
        MovieCreate, Body(description="Movie JSON to add to the database")
    ],
    response: Response,
    db: Session = Depends(get_db),
) -> schemas.Movie:
    """
    Receive a **Movie** object as json and add it to the database, returns the created movie id on database.
    """
    movie = crud.create_movie(db, movie)
    response.status_code = status.HTTP_201_CREATED
    response.headers["Location"] = f"/movies/{movie.movie_id}"
    return movie


@app.get("/movies/{movie_id}", tags=["movies"], responses=RESPONSES_NOT_FOUND)
def get_movie(
    movie_id: Annotated[
        int, Path(description="The ID of the movie to get", ge=0, example=1)
    ],
    db: Session = Depends(get_db),
) -> schemas.Movie:
    """
    Get a **Movie** object from the database, given its id.
    """
    movie = crud.get_movie(db, movie_id)
    if not movie:
        raise HTTPException(
            status_code=404,
            detail=f"The movie with id {movie_id} doesnt exist in the DataBase.",
        )
    return movie


@app.delete("/movies/{movie_id}", tags=["movies"], responses=RESPONSES_NOT_FOUND)
def delete_movie(
    movie_id: Annotated[
        int, Path(description="The ID of the movie to delete", ge=0, example=1)
    ],
    db: Session = Depends(get_db),
) -> schemas.Movie:
    """
    Delete a **Movie** object from the database, given its id.
    """
    movie = crud.delete_movie(db, movie_id)
    if not movie:
        raise HTTPException(
            status_code=404,
            detail=f"The movie with id {movie_id} doesnt exist in the DataBase.",
        )
    return movie


@app.put("/movies/{movie_id}", tags=["movies"], responses=RESPONSES_NOT_FOUND)
def update_movie(
    movie_id: Annotated[
        int, Path(description="The ID of the movie to update", ge=0, example=1)
    ],
    movie: Annotated[
        schemas.MovieCreate, Body(description="Movie JSON to update the database")
    ],
    db: Session = Depends(get_db),
) -> schemas.Movie:
    """
    Update a **Movie** object from the database, given its id.
    """
    movie_updated = crud.update_movie(db, movie_id, movie)
    if not movie_updated:
        raise HTTPException(
            status_code=404,
            detail=f"The movie with id {movie_id} doesnt exist in the DataBase.",
        )
    return movie_updated


@app.get("/reviews/{movie_id}", tags=["reviews"], responses=RESPONSES_NOT_FOUND)
def get_movie_reviews(
    movie_id: Annotated[
        int,
        Path(
            description="The id of the movie to get the all the reviews",
            ge=0,
            example=1,
        ),
    ],
    db: Session = Depends(get_db),
) -> list[schemas.MovieReview]:
    """
    Get the list of **reviews** for a given movie.
    """
    movie_reviews = crud.get_movie_reviews(db, movie_id)
    if not movie_reviews:
        raise HTTPException(
            status_code=404,
            detail=f"The movie with id {movie_id} doesnt exist in the DataBase.",
        )
    return movie_reviews


@app.post(
    "/reviews/",
    tags=["reviews"],
    status_code=201,
    responses=RESPONSES_NOT_FOUND,
)
def create_review(
    review: schemas.MovieReviewCreate,
    response: Response,
    db: Session = Depends(get_db),
) -> schemas.MovieReview:
    """
    Add a **review** to a given movie.
    """
    if not crud.get_movie(db, review.movie_id):
        raise HTTPException(
            status_code=404,
            detail=f"The movie with id {review.movie_id} doesnt exist in the DataBase.",
        )
    elif not crud.get_user(db, review.user_id):
        raise HTTPException(
            status_code=404,
            detail=f"The user with id {review.user_id} doesnt exist in the DataBase.",
        )

    moview_review = crud.create_movie_review(
        db, review, review.user_id, review.movie_id
    )
    if not moview_review:
        raise HTTPException(
            status_code=404,
            detail=f"The movie with id {review.movie_id} doesnt exist in the DataBase.",
        )
    response.status_code = status.HTTP_201_CREATED
    response.headers["Location"] = f"/reviews/{moview_review.review_id}"
    return moview_review


@app.put(
    "/reviews/{review_id}",
    tags=["reviews"],
    responses=RESPONSES_NOT_FOUND,
)
def update_review(
    review_id: Annotated[
        int, Path(description="The id of the review to update.", ge=0, example=1)
    ],
    review: schemas.MovieReviewCreate,
    db: Session = Depends(get_db),
) -> schemas.MovieReview:
    """
    Update a **review** from its id and the **movie id**.
    """
    if not crud.get_movie(db, review.movie_id):
        raise HTTPException(
            status_code=404,
            detail=f"The movie with id {review.movie_id} doesnt exist in the DataBase.",
        )
    review_updated = crud.update_movie_review(db, review_id, review)
    if not review_updated:
        raise HTTPException(
            status_code=404,
            detail=f"The review with id {review_id} doesnt exist in the DataBase.",
        )
    return review_updated


@app.delete(
    "/reviews/{review_id}",
    tags=["reviews"],
    responses=RESPONSES_NOT_FOUND,
)
def delete_review(
    review_id: Annotated[
        int, Path(description="The ID of the review to delete.", ge=0, example=0)
    ],
    db: Session = Depends(get_db),
) -> schemas.MovieReview:
    """
    Delete a **review** from a given movie.
    """
    deleted_review = crud.delete_movie_review(db, review_id)
    if not deleted_review:
        raise HTTPException(
            status_code=404,
            detail=f"The review with id {review_id} doesnt exist in the DataBase.",
        )
    return deleted_review
