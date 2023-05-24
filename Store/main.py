import databases
import sqlalchemy

from fastapi import FastAPI, Request
from decouple import config

# install decouple - pip install python-decouple/ create in main folder regular file '.env' and add there the DB details
DATABASE_URL = f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@{config('DB_PORT')}/{config('DB_NAME')}"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


# Creating the first model
books = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("author", sqlalchemy.String),
    sqlalchemy.Column("pages", sqlalchemy.Integer),
)

# creating second model
readers = sqlalchemy.Table(
    "readers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
)

# creating a junction table for many-to-many relationships
readers_books = sqlalchemy.Table(
    "readers_books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("book_id", sqlalchemy.ForeignKey("books.id"), nullable=False),
    sqlalchemy.Column("reader_id", sqlalchemy.ForeignKey("readers.id"), nullable=False),
)

# save the DB state. install alembic and use it for migrations with these commands:
# 1) alembic revision --autogenerate -m "Initial"  -> "Initial" for first migrations
# 2) alembic upgrade head

### Not using this!!!
# engine = sqlalchemy.create_engine(DATABASE_URL)
# # This creates all tables (in our case just one above "books"
# metadata.create_all(engine)

app = FastAPI()

# adding middlewares/events for when starting the application and closing
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# returning all records from DB
@app.get("/books/")
async def get_all_books():
    query = books.select()
    return await database.fetch_all(query) #returns a list of dictionaries -> in JSON format

# create a record (new book)
@app.post("/books/")
async def create_book(request: Request):
    data = await request.json() #getting the data
    query = books.insert().values(**data) #unpacking the dictionary
    last_record_id = await database.execute(query) #insert the new book values here
    return {"id": last_record_id}

@app.post("/readers/")
async def create_reader(request: Request):
    data = await request.json() #getting the data
    query = readers.insert().values(**data) #unpacking the dictionary
    last_record_id = await database.execute(query) #insert the new book values here
    return {"id": last_record_id}

@app.post("/read/")
async def read_book(request: Request):
    data = await request.json() #getting the data
    query = readers_books.insert().values(**data) #unpacking the dictionary
    last_record_id = await database.execute(query) #insert the new book values here
    return {"id": last_record_id}