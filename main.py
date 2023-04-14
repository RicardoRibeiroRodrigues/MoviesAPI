from typing import Annotated
from models import *
from fastapi import FastAPI, Path, HTTPException, Response, status, Body

app = FastAPI()

movies: dict[int, MovieDB] = {}
last_movie_id = 0
last_review_id = 0


def add_movie_db(movie: MovieDB) -> int:
    global last_movie_id
    movie_id = last_movie_id
    movies[movie_id] = movie
    last_movie_id += 1
    return movie_id


def remove_movie_db(movie_id: int) -> MovieDB:
    return movies.pop(movie_id)


def add_review_db(movie_id: int, review: movieReviewDB) -> int:
    global last_review_id
    review_id = last_review_id
    movies[movie_id].reviews[review_id] = review
    last_review_id += 1
    return review_id


def remove_review_db(movie_id: int, review_id: int) -> movieReviewDB:
    return movies[movie_id].reviews.pop(review_id)


# This is used to document the 404 response for all endpoints that can raise it.
RESPONSES_NOT_FOUND = {
    404: {
        "description": "Item not found in the database",
    }
}


@app.get("/")
async def root():
    return "Hello World, please check the /docs for info on using this API."


@app.get("/movies/", tags=["movies"])
def get_movies():
    """
    Get the list of the all **movies** in the database.
    """
    return list(movies.values())


@app.post("/movies/", tags=["movies"], status_code=201)
def create_movie(
    movie: Annotated[Movie, Body(description="Movie JSON to add to the database")],
    response: Response,
) -> MovieDB:
    """
    Receive a **Movie** object as json and add it to the database, returns the created movie id on database.
    """
    movie_to_add = MovieDB(**movie.dict(), movie_id=last_movie_id)
    movie_id = add_movie_db(movie_to_add)
    response.status_code = status.HTTP_201_CREATED
    response.headers["Location"] = f"/movies/{movie_id}"
    return movie_to_add


@app.get("/movies/{movie_id}", tags=["movies"], responses=RESPONSES_NOT_FOUND)
def get_movie(
    movie_id: Annotated[
        int, Path(description="The ID of the movie to get", ge=0, example=0)
    ]
) -> MovieDB:
    """
    Get a **Movie** object from the database, given its id.
    """
    if movie_id not in movies:
        raise HTTPException(
            status_code=404,
            detail=f"The movie with id {movie_id} doesnt exist in the DataBase.",
        )
    return movies[movie_id]


@app.delete("/movies/{movie_id}", tags=["movies"], responses=RESPONSES_NOT_FOUND)
def delete_movie(
    movie_id: Annotated[
        int, Path(description="The ID of the movie to delete", ge=0, example=0)
    ]
) -> MovieDB:
    """
    Delete a **Movie** object from the database, given its id.
    """
    if movie_id not in movies:
        raise HTTPException(
            status_code=404,
            detail=f"The movie with id {movie_id} doesnt exist in the DataBase.",
        )
    return remove_movie_db(movie_id)


@app.put("/movies/{movie_id}", tags=["movies"], responses=RESPONSES_NOT_FOUND)
def update_movie(
    movie_id: Annotated[
        int, Path(description="The ID of the movie to update", ge=0, example=0)
    ],
    movie: Annotated[Movie, Body(description="Movie JSON to update the database")],
) -> MovieDB:
    """
    Update a **Movie** object from the database, given its id.
    """
    if movie_id not in movies:
        raise HTTPException(
            status_code=404,
            detail=f"The movie with id {movie_id} doesnt exist in the DataBase.",
        )
    movies[movie_id] = MovieDB(**movie.dict(), movie_id=movie_id)
    return movies[movie_id]


@app.get("/movies/{movie_id}/reviews", tags=["reviews"], responses=RESPONSES_NOT_FOUND)
def get_movie_reviews(
    movie_id: Annotated[
        int,
        Path(
            description="The ID of the movie to get the all the reviews",
            ge=0,
            example=0,
        ),
    ]
) -> list[movieReview]:
    """
    Get the list of **reviews** for a given movie.
    """
    if movie_id not in movies:
        raise HTTPException(
            status_code=404,
            detail=f"The movie with id {movie_id} doesnt exist in the DataBase.",
        )
    return list(movies[movie_id].reviews.values())


@app.post(
    "/movies/{movie_id}/reviews",
    tags=["reviews"],
    status_code=201,
    responses=RESPONSES_NOT_FOUND,
)
def create_review(
    movie_id: Annotated[
        int,
        Path(description="The ID of the movie to post the review.", ge=0, example=0),
    ],
    review: movieReview,
    response: Response,
) -> movieReview:
    """
    Add a **review** to a given movie.
    """
    if movie_id not in movies:
        raise HTTPException(
            status_code=404,
            detail=f"The movie with id {movie_id} doesnt exist in the DataBase.",
        )
    movie_id = add_review_db(
        movie_id, movieReviewDB(**review.dict(), review_id=last_review_id)
    )
    response.status_code = status.HTTP_201_CREATED
    response.headers["Location"] = f"/reviews/{movie_id}"
    return review


@app.put(
    "/movies/{movie_id}/reviews/{review_id}",
    tags=["reviews"],
    responses=RESPONSES_NOT_FOUND,
)
def update_review(
    movie_id: Annotated[
        int,
        Path(description="The id of the movie to update the review.", ge=0, example=0),
    ],
    review_id: Annotated[
        int, Path(description="The id of the review to update.", ge=0, example=0)
    ],
    review: movieReview,
) -> movieReview:
    """
    Update a **review** from its id and the **movie id**.
    """
    if movie_id not in movies:
        raise HTTPException(
            status_code=404,
            detail=f"The movie with id {movie_id} doesnt exist in the DataBase.",
        )
    if review_id not in movies[movie_id].reviews:
        raise HTTPException(
            status_code=404,
            detail=f"The review with id {review_id} doesnt exist in the DataBase.",
        )
    movies[movie_id].reviews[review_id] = movieReviewDB(
        **review.dict(), review_id=review_id
    )
    return review


@app.delete(
    "/movies/{movie_id}/reviews/{review_id}",
    tags=["reviews"],
    responses=RESPONSES_NOT_FOUND,
)
def delete_review(
    movie_id: Annotated[
        int,
        Path(description="The ID of the movie to delete the review.", ge=0, example=0),
    ],
    review_id: Annotated[
        int, Path(description="The ID of the review to delete.", ge=0, example=0)
    ],
) -> movieReview:
    """
    Delete a **review** from a given movie.
    """
    if movie_id not in movies:
        raise HTTPException(
            status_code=404,
            detail=f"The movie with id {movie_id} doesnt exist in the DataBase.",
        )
    if review_id not in movies[movie_id].reviews:
        raise HTTPException(
            status_code=404,
            detail=f"The review with id {review_id} doesnt exist in the DataBase.",
        )
    return remove_review_db(movie_id, review_id)
