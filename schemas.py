from pydantic import BaseModel, Field


class MovieReviewBase(BaseModel):
    n_stars: float = Field(
        gte=0.0,
        le=5.0,
        description="The number of stars from 0.0 to 5.0 the user has given to the movie.",
        example=4.6,
    )
    review: str = Field(
        description="The texto of the review of the movie.", example="Great movie!"
    )


class MovieReviewCreate(MovieReviewBase):
    movie_id: int = Field(
        ge=0, description="The id of the movie that the review is for.", example=1
    )
    user_id: int = Field(
        ge=0,
        description="The id of the user that made the review in the database.",
        example=1,
    )


class MovieReviewUpdate(MovieReviewBase):
    pass


class MovieReview(MovieReviewCreate):
    review_id: int = Field(
        ge=0, description="The ID of the review in the database.", example=1
    )

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str = Field(
        description="The username of the user.", example="joaozinho123"
    )
    fullname: str | None = Field(
        default=None,
        description="The full name of the user.",
        example="Joazinho da Silva",
    )


class UserCreate(UserBase):
    password: str = Field(description="The password of the user.", example="12345678")


class User(UserBase):
    user_id: int = Field(description="The ID of the user in the database.", example=1)
    user_reviews: list[MovieReview] = Field(description="The reviews made by the user.")

    class Config:
        orm_mode = True


class MovieBase(BaseModel):
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


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    movie_id: int = Field(
        ge=0, description="The ID of the movie in the database.", example=0
    )
    reviews: list[MovieReview] = Field(description="The reviews of the movie.")

    class Config:
        orm_mode = True
