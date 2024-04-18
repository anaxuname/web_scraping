from pydantic import BaseModel, Field


class Amount(BaseModel):
    amount: int
    currency: str


class Price(BaseModel):
    actual: Amount
    regular: Amount


class Review(BaseModel):
    rating: float
    reviews_count: int = Field(alias="reviewsCount")


class Product(BaseModel):
    url: str
    name: str
    price: Price
    reviews: Review = Review(rating=0, reviewsCount=0)


class ProductInfo(BaseModel):
    description: str
    instructions: str
    country: str
