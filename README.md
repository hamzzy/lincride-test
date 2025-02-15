
# Dynamic Pricing API

This project implements a dynamic pricing API for a ride-hailing application using Django, Django REST Framework (DRF), Redis for caching, and integrates asynchronous processing.

## Table of Contents

- [Dynamic Pricing API](#dynamic-pricing-api)
  - [Table of Contents](#table-of-contents)
  - [Setup Instructions](#setup-instructions)
  - [Running the Application](#running-the-application)
  - [Running Tests](#running-tests)
  - [API Endpoints](#api-endpoints)
    - [`GET /api/calculate-fare/`](#get-apicalculate-fare)

## Setup Instructions

1.  **Clone the repository:**

    ```bash
    git clone <repository_link>
    cd <repository_name>
    ```

2.  **Install Docker and Docker Compose:**

    *   Make sure you have Docker and Docker Compose installed on your system. You can download them from the official Docker website:  [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

3.  **Build and Run the Application:**

    ```bash
    docker-compose up --build
    ```

    This command will build the Docker image, create the necessary containers (web, redis, db), and start the application.  Docker Compose will automatically handle the dependencies between the services.

4.  **Apply Migrations:**

   If you're starting with a new database, you'll need to apply the Django migrations:

    ```bash
    docker-compose exec web python manage.py migrate
    ```

    This command runs the `migrate` command inside the `web` container.

5.  **Create a Superuser (Optional):**

    If you want to access the Django admin panel, you can create a superuser:

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

6.  **Access the Application:**

    The API will be accessible at `http://localhost:8000/`.

## Running the Application

Once the Docker containers are running, the application will be available at the specified port (usually 8000).

## Running Tests

To run the tests:

1.  **Ensure the application is running:**
    Make sure that the application and its dependencies (Redis, database) are running using `docker-compose up`.

2.  **Run tests inside the web container:**

    ```bash
    docker-compose exec web python manage.py test
    ```

    This command will execute the Django tests within the `web` container.
   If a pytest or pytest-asyncio package is installed, remember to follow those rules on the test cases, such as marking async, or setting the proper model.

## API Endpoints

### `GET /api/calculate-fare/`

Accepts the following query parameters:

*   `distance`: The distance of the ride in kilometers (required, numeric).
*   `traffic_level`: The traffic level (`low`, `normal`, `high`). Defaults to `normal`.
*   `demand_level`: The demand level (`normal`, `high`,`peak`). Defaults to `normal`.
*   `current_time`: The time of the request (format HH:MM). If not provided, the current server time will be used.
*   `location`: The geographical location of the request. Used to isolate real-time demand (String). Defaults to "default".

Returns the ride fare details as a JSON response.

**Sample Request:**
content_copy
download
Use code with caution.
Markdown

GET /api/calculate-fare/?distance=10&traffic_level=high&demand_level=peak&current_time=10:00&location=Downtown

**Sample Response:**

```json
{
    "base_fare": 2.5,
    "distance_fare": 10.0,
    "traffic_multiplier": 2.0,
    "demand_multiplier": 1.0,
    "time_multiplier": 1.3,
    "total_fare": 39.0
}
