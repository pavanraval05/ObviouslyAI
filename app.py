from fastapi import FastAPI, HTTPException, Depends, Query, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, ValidationError
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from math import ceil
from jose import jwt, JWTError
from passlib.context import CryptContext

# Initialize the app
app = FastAPI()

# Database setup
DATABASE_URL = "sqlitecloud://cmn6x4qvhz.g6.sqlite.cloud:8860/books.db?apikey=0fbMBtLzIYN4l62Bdsw6zE9AYlpNn87V5Pc8ySHbmOQ"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Secret key to encode the JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy user data
fake_users_db = {
    "pavan": {
        "username": "pavan",
        "full_name": "Pavan Raval",
        "email": "raval.pa@northeastern.edu",
        "hashed_password": pwd_context.hash("ObviouslyAI"),
        "disabled": False,
    }
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return user_dict

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# SQLAlchemy model for the books table
class BookDB(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    published_date = Column(Date)
    summary = Column(String)
    genre = Column(String)

# Pydantic model for request and response
class Token(BaseModel):
    access_token: str
    token_type: str

class Book(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=100)
    published_date: date
    summary: str = Field(..., min_length=1, max_length=500)
    genre: str = Field(..., min_length=1, max_length=50)

    class Config:
        orm_mode = True
        from_attributes = True

class BookUpdate(BaseModel):
    updates: Dict[str, str]

class PaginatedBooks(BaseModel):
    total_books: int
    total_pages: int
    current_page: int
    books: List[Book]

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username)
    if user is None:
        raise credentials_exception
    return user

# Route to get a list of books
@app.get("/read", response_model=PaginatedBooks)
def get_books(page: int = Query(1, ge=1), per_page: int = Query(10, ge=1, le=100), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        total_books = db.query(BookDB).count()
        total_pages = ceil(total_books / per_page)
        offset = (page - 1) * per_page
        books_db = db.query(BookDB).offset(offset).limit(per_page).all()
        books = [Book.from_orm(book) for book in books_db]
        return PaginatedBooks(
            total_books=total_books,
            total_pages=total_pages,
            current_page=page,
            books=books
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    custom_errors = [
        {"detail": f"Invalid input given for {error['loc'][1]}"}
        for error in errors
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"errors": custom_errors},
    )

@app.post("/create", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book: Book, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        new_book = BookDB(
            title=book.title,
            author=book.author,
            published_date=book.published_date,
            summary=book.summary,
            genre=book.genre
        )
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/update/{book_id}", response_model=Book)
def update_book(book_id: int, update_data: BookUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        book = db.query(BookDB).filter(BookDB.id == book_id).first()
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        
        for field, value in update_data.updates.items():
            if hasattr(book, field):
                setattr(book, field, value)
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid field name: {field}")
        
        db.commit()
        db.refresh(book)
        return book
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.delete("/delete/{book_id}", response_model=dict)
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        book = db.query(BookDB).filter(BookDB.id == book_id).first()
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        
        db.delete(book)
        db.commit()
        return {"detail": "Book deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Run the app (for development purposes)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)