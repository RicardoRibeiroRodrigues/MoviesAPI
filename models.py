from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, DECIMAL
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(80))
    user_reviews: Mapped[List["MovieReview"]] = relationship(
        "MovieReview", back_populates="user"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Movie(Base):
    __tablename__ = "movie"

    movie_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(80))
    studio: Mapped[str] = mapped_column(String(80))
    description: Mapped[Optional[str]] = mapped_column(String(400))
    year: Mapped[int] = mapped_column(Integer)

    reviews: Mapped[List["MovieReview"]] = relationship(
        "MovieReview", back_populates="movie"
    )


class MovieReview(Base):
    __tablename__ = "MovieReview"

    review_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    n_stars: Mapped[float] = mapped_column(DECIMAL(2, 1))
    review: Mapped[str] = mapped_column(String(500))

    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    user: Mapped["User"] = relationship(back_populates="user_reviews")

    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.movie_id"))
    movie: Mapped["Movie"] = relationship(back_populates="reviews")
