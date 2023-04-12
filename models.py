from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int
    username: str
    full_name: str | None = None


class movieReview(BaseModel):
    n_stars: float = Field(
        gte=0.0, le=10.0, description="The number of stars this movie got"
    )
    review: str
    user: User


class Movie(BaseModel):
    title: str
    description: str | None = None
    year: int


class MovieDB(Movie):
    movie_id: int
    reviews: list[movieReview] | list = []
