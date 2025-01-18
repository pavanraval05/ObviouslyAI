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
