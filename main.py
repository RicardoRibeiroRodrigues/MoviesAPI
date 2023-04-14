from typing import Annotated
from models import *
from fastapi import FastAPI, Path, HTTPException, Response, status, Body

app = FastAPI()

movies: dict[int, MovieDB] = {}
last_id = 0


def add_movie(movie: MovieDB) -> int:
    global last_id
    movie_id = last_id
    movies[movie_id] = movie
    last_id += 1
    return movie_id


def remove_movie(movie_id: int) -> MovieDB:
    return movies.pop(movie_id)


@app.get("/")
async def root():
    return "Hello World, please check the /docs for info on using this API."


@app.get("/movies/", tags=["movies"])
def get_movies():
    """
    Get the list of the **movies** in the database.
    """
    return list(movies.values())


# TODO: Descricao dos argumentos usando Body ou Field, colocar summary e description no .post()
@app.post("/movies/", tags=["movies"])
def create_movie(
    movie: Annotated[Movie, Body(description="Movie JSON to add to the database")],
    response: Response,
) -> MovieDB:
    """
    Receive a **Movie** object as json and add it to the database, returns the created movie id on database.
    """
    movie_to_add = MovieDB(**movie.dict(), movie_id=last_id)
    movie_id = add_movie(movie_to_add)
    response.status_code = status.HTTP_201_CREATED
    response.headers["Location"] = f"/movies/{movie_id}"
    return movie_to_add


@app.get("/movies/{movie_id}", tags=["movies"])
def get_movie(
    movie_id: Annotated[int, Path(title="The ID of the movie to get", ge=0)]
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


@app.get("/reviews/{movie_id}", tags=["reviews"])
def get_reviews(
    movie_id: Annotated[
        int, Path(title="The ID of the movie to get the all the reviews", ge=0)
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
    return movies[movie_id].reviews


@app.post("/reviews/{movie_id}", tags=["reviews"])
def add_review(
    movie_id: Annotated[
        int, Path(title="The ID of the movie to post the review.", ge=0)
    ],
    review: movieReview,
    response: Response,
) -> movieReview:
    """
    Add a **review** to a given movie.
    """
    if movie_id >= len(movies):
        raise HTTPException(
            status_code=404,
            detail=f"The movie with id {movie_id} doesnt exist in the DataBase.",
        )
    movies[movie_id].reviews.append(review)
    response.status_code = status.HTTP_201_CREATED
    response.headers["Location"] = f"/reviews/{movie_id}"
    return review
