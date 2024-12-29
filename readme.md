# IMDb Content Upload and Review System

## Objective

The objective of this project is to build a feature that allows the content team to upload movie-related data using a CSV file, and to provide the necessary APIs to consume and manage this data. This project is part of IMDb, the world's most popular and authoritative source for movie, TV, and celebrity content.

### Features
- **CSV Upload**: Users can upload movie-related data in CSV format.
- **Movie Data View**: Users can view the list of all movies/shows available in the system with pagination and filtering by:
  - Year of release
  - Language
- **Sorting**: The data can be sorted by release date and ratings.

---

## Tech Stack

- **Backend**: Django (with Django REST Framework)
- **Database**: MySQL
- **CSV Processing**: Python's `csv` module or similar for CSV file parsing
- **Environment Management**: `.env` for storing configuration variables

---

## Setup Instructions

### 1. Install Dependencies

Clone the repository and navigate to the project directory.

```bash
git clone <repository_url>
cd <project_directory>
```

### 2. Create a virtual environment and install the required packages.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. . Set Up Environment Variables
Create a dev.env file in the root of the project directory with the following content:

```bash
DJANGO_SECRET_KEY='xxxdfds'

# MySQL Main
MYSQL_HOST='localhost'
MYSQL_NAME='imdb_content_db'
MYSQL_USER='root'
MYSQL_PASSWORD=''
MYSQL_PORT=3306
```

### 4. Apply Database Migrations
After setting up the environment, run the following command to apply database migrations:

```bash
python manage.py migrate
```

### 5. Start the Development Server
```bash
python manage.py runserver
```
Your API will be available at http://127.0.0.1:8000/

### 5. To Run the Tests for all the APIs
```bash
python manage.py test movies
```


## API Endpoints

### 1. CSV Upload API
- **URL**: `/v1/upload-csv/`
- **Method**: `POST`
- **Description**: Allows users to upload a CSV file containing movie data.
- **Request Body**: A CSV file (Max size: 100 MB)
- **Response**:
  - **Success**:
    ```json
    {
      "status": "success",
      "message": "CSV file uploaded and processed successfully."
    }
    ```
  - **Failure**:
    ```json
    {
      "status": "failure",
      "message": "File size exceeds the maximum allowed limit of 100 MB."
    }
    ```

---

### 2. Movie List API
- **URL**: `/v1/movies/`
- **Method**: `GET`
- **Description**: View the list of all uploaded movies/shows with pagination, filtering, and sorting options.
- **Query Parameters**:
  - `page`: The page number for pagination.
  - `year`: Filter movies by the year of release.
  - `language`: Filter movies by language.
  - `sort_by`: Sort movies by release date or ratings.

#### Example Request:
```bash
GET /v1/movies/?page=1&year=2020&language=en&sort_by=release_date

