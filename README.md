# Python backend test
This project is a FastAPI-based RESTful API that manages profiles and their friendships. The API allows you to create, read, update, delete profiles, get their friends, and find the shortest connection between two profiles.

To storage the data, the project uses SQLite. The database is created automatically when the application is started.

## Features
- Create, Read, Update, Delete (CRUD) operations for profiles.
- List all profiles.
- Given a profile, list all its friends.
- Find the shortest connection between two profiles based on their friendships.

## Installation
1. Clone the repository:

```bash
git clone https://github.com/antoniowd/python-backend-test.git
cd python-backend-test
```

2. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```
**Note**: python3.11 is required to run the project.

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Initialize the application:

```bash
fastapi dev app/main.py
```
The application will be available at `http://localhost:8000`.

## API Documentation
 API documentation is available at `http://localhost:8000/docs`.

## Testing
To run the tests, execute the following command:

```bash
pytest
```
