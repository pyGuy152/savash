import strawberry
from typing import List, Optional

# Define your GraphQL types
@strawberry.type
class User:
    id: strawberry.ID
    name: str
    age: int
    email: Optional[str] = None

@strawberry.type
class Book:
    title: str
    author: str
    pages: int

# In-memory "database" for demonstration
users_db = [
    User(id=strawberry.ID("1"), name="Alice", age=30, email="alice@example.com"),
    User(id=strawberry.ID("2"), name="Bob", age=25),
]

books_db = [
    Book(title="The Great Gatsby", author="F. Scott Fitzgerald", pages=180),
    Book(title="1984", author="George Orwell", pages=328),
]

# Define your Query type (how clients can fetch data)
@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"

    @strawberry.field
    def user(self, id: strawberry.ID) -> Optional[User]:
        for user in users_db:
            if user.id == id:
                return user
        return None

    @strawberry.field
    def users(self) -> List[User]:
        return users_db
    
    @strawberry.field
    def books(self) -> List[Book]:
        return books_db

# Define your Mutation type (how clients can modify data)
@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_user(self, name: str, age: int, email: Optional[str] = None) -> User:
        new_id = str(len(users_db) + 1)
        new_user = User(id=strawberry.ID(new_id), name=name, age=age, email=email)
        users_db.append(new_user)
        return new_user

    @strawberry.mutation
    def add_book(self, title: str, author: str, pages: int) -> Book:
        new_book = Book(title=title, author=author, pages=pages)
        books_db.append(new_book)
        return new_book

# Create the Strawberry Schema
schema = strawberry.Schema(query=Query, mutation=Mutation)