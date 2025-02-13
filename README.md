# Dynamic Pricing API

This project implements a dynamic pricing API for a ride-hailing application using Django and Django REST Framework (DRF).

## Setup Instructions

1.  **Clone the repository:**

    ```bash
    git clone <repository_link>
    cd <repository_name>
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (optional, for accessing the Django admin panel):**

    ```bash
    python manage.py createsuperuser
    ```

## Running the Application

1.  **Start the development server:**

    ```bash
    python manage.py runserver
    ```

    The API will be accessible at `http://localhost:8000/`.

## Running Tests

1.  **Run the tests:**

    ```bash
    python manage.py test
    ```

    This will run all the unit and integration tests defined in the `pricing/tests.py` file.

## API Endpoints

### `GET /api/calculate-fare/`

Accepts the following query parameters:

*   `distance`: The distance of the ride in kilometers (required, numeric).
*   `traffic_level`: The traffic level (`low`, `normal`, `high`). Defaults to `normal`.
*   `demand_level`: The demand level (`low`, `normal`, `peak`). Defaults to `normal`.

Returns the ride fare details as a JSON response.

**Sample Request:**