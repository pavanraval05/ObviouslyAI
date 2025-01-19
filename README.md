# FastAPI Book Management Application

This is a FastAPI application for managing a collection of books. It provides endpoints for creating, reading, updating, and deleting book records. The application also includes user authentication using JWT tokens.

## Demo

[ObviouslyAI - Demo](https://obviouslyai-7e45a676f5a1.herokuapp.com/docs)

## Features

- **User Authentication**: Secure access using OAuth2 with JWT tokens.
- **CRUD Operations**: Create, read, update, and delete book records.
- **Pagination**: Supports pagination for listing books.
- **Validation**: Input validation using Pydantic models.
- **Error Handling**: Custom error handling for validation errors.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **SQLite Cloud**: SQLite databases in cloud environments.
- **SQLite**: A lightweight, disk-based database.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **JWT**: JSON Web Tokens for secure user authentication.
- **Passlib**: A password hashing library for Python.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/fastapi-book-management.git
   cd fastapi-book-management
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   uvicorn app:app --reload
   ```

## API Endpoints

### Authentication

- **POST /token**: Obtain a JWT token by providing a username and password.

### Books

- **GET /read**: Retrieve a paginated list of books.
- **POST /create**: Create a new book record.
- **PUT /update/{book_id}**: Update an existing book record.
- **DELETE /delete/{book_id}**: Delete a book record.

## Environment Variables

- `DATABASE_URL`: The URL for the SQLite database.
- `SECRET_KEY`: The secret key used for encoding JWT tokens.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: The expiration time for access tokens in minutes.

## Usage

1. **Authentication**: Use the `/token` endpoint to obtain a JWT token. Include this token in the `Authorization` header as a Bearer token for accessing other endpoints.

2. **CRUD Operations**: Use the provided endpoints to manage book records. Ensure you are authenticated to perform these operations.

## Error Handling

- **Validation Errors**: Returns a 422 status code with details about the invalid input.
- **Authentication Errors**: Returns a 401 status code if credentials are invalid.
- **Not Found Errors**: Returns a 404 status code if a book is not found.
- **Server Errors**: Returns a 500 status code for unexpected server errors.





# To Test Book Management API

## 1. Create a Book (POST /create)

To create a new book, the JSON body should contain the `title`, `author`, `published_date`, `summary`, and `genre`:

```json
{
  "title": "To Kill a Mockingbird",
  "author": "Harper Lee",
  "published_date": "1960-07-11",
  "summary": "A novel about the serious issues of rape and racial inequality.",
  "genre": "Fiction"
}
```

## 2. Update a Book (PUT /update/{book_id})

To update a book, the JSON body should contain an `updates` object with the fields you want to update. For example, to update the `title` and `summary`:

```json
{
  "updates": {
    "title": "To Kill a Mockingbird - Updated Edition",
    "summary": "A gripping novel about the serious issues of racial inequality and justice."
  }
}
```

## 3. Delete a Book (DELETE /delete/{book_id})

To delete a book, you don't need to send a body. You only need to specify the `book_id` in the URL. For example, to delete the book with ID `123`:

```bash
DELETE /delete/123
```

No JSON body is required for this request.

## 4. Read Books (List of Books) (GET /read)

To retrieve a list of books, the query parameters `page` and `per_page` can be used to control pagination. Example URL with query parameters:

```bash
GET /read?page=1&per_page=10
```

This will return a paginated list of books with the following structure:

```json
{
  "total_books": 100,
  "total_pages": 10,
  "current_page": 1,
  "books": [
    {
      "id": 1,
      "title": "To Kill a Mockingbird",
      "author": "Harper Lee",
      "published_date": "1960-07-11",
      "summary": "A novel about the serious issues of rape and racial inequality.",
      "genre": "Fiction"
    },
    {
      "id": 2,
      "title": "1984",
      "author": "George Orwell",
      "published_date": "1949-06-08",
      "summary": "A dystopian novel about totalitarianism and surveillance.",
      "genre": "Dystopian"
    }
  ]
}
```

