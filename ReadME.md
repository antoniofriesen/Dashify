# Dashify

## Overview
Dashify is a Django-based web application that allows users to register, log in, and access a dashboard with various features including a blog, to-do list, and data-plotting options using JSON or CSV files.

## Prerequisites
Ensure you have Python 3.12.2 installed. You can download Python from [here](https://www.python.org/downloads/).

## Installation

1. Clone the repository from GitHub:
    ```
    git clone https://github.com/username/dashify.git
    ```

2. Set up a virtual environment:

    **For Mac/Linux:**
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```

    **For Windows:**
    ```
    python -m venv .venv
    .\\.venv\\Scripts\\activate
    ```

3. Install the required dependencies:
    ```
    cd dashify
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```
    python manage.py migrate
    ```

5. Start the server:
    ```
    python manage.py runserver
    ```

6. Open your browser and navigate to `http://127.0.0.1:8000/` to access Dashify.

## License
This project is licensed under the MIT License.
