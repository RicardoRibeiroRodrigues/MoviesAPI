from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int = Field(description="The ID of the user in the database.", example=1)
    username: str = Field(description="The username of the user.", example="user123")
    full_name: str | None = Field(
        default=None,
        description="The full name of the user.",
        example="User 123 da Silva",
    )


class movieReview(BaseModel):
    n_stars: float = Field(
        gte=0.0,
        le=5.0,
        description="The number of stars from 0.0 to 5.0 the user has given to the movie.",
        example=4.6,
    )
    review: str = Field(
        description="The texto of the review of the movie.", example="Great movie!"
    )
    user: User = Field(
        description="The user that has made the review.",
    )


class movieReviewDB(movieReview):
    review_id: int = Field(ge=0, description="The ID of the review in the database.")


class Movie(BaseModel):
    title: str = Field(description="The title of the movie.", example="The Matrix")
    studio: str = Field(
        description="The studio that produced the movie.", example="Warner Bros."
    )
    description: str | None = Field(
        default=None,
        description="The description of the movie.",
        example="A movie about a hacker.",
    )
    year: int = Field(description="The year the movie was released.", example=1999)


class MovieDB(Movie):
    movie_id: int = Field(ge=0, description="The ID of the movie in the database.")
    reviews: dict[int, movieReviewDB] | dict = Field(
        default={}, description="The dict of reviews for the movie."
    )
