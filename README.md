# ToDo API

## Setup Instructions

1. **Clone the repository**


2. **Install dependencies**
   ```
   pip install fastapi uvicorn sqlalchemy pydantic
   ```

3. **Run the application**
   ```
   uvicorn main:app --reload
   ```

4. **Database**
   - The SQLite database file (`todo.db`) will be created automatically in the project directory.

## API Endpoints

### Users
- `GET /users` - List all users
- `POST /users` - Create a new user

### Todos
- `GET /todos` - List all todos
- `POST /todos` - Create a new todo (requires valid user_id)
- `DELETE /todos/{id}` - Delete a todo by id

## Notes
- User `name` must be unique and not empty.
- Todo `name` must not be empty.
- All timestamps are in UTC.
