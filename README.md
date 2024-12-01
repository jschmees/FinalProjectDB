

## Overview
This project is a Django web application designed to manage restaurant menus efficiently. The application offers a user-friendly GUI for interacting with the system, as well as providing a full suite of management features for menu creation, updates, and more.

## Prerequisites
Ensure that the following software is installed before proceeding:

- Python (>=3.8)
- Git
- Virtualenv
- Django

## Installation Guide

Follow these steps to set up the project locally:

### Step 1: Clone the Repository
Clone the project from the remote repository:

```bash
$ git clone <repository-url>
$ cd <project-directory>
```

### Step 2: Set Up a Virtual Environment
Create a virtual environment to keep dependencies isolated:

```bash
$ python -m venv venv
$ source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 3: Install Requirements
Install the required packages using `pip`:

```bash
$ pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Copy the example environment file and fill it in with your specific details:

```bash
$ cp .env.example .env
```

Open `.env` and fill in the required details, such as your database credentials and API keys.

### Step 5: Run Migrations and Create Superuser
Run the Django database migrations and create a superuser for accessing the Django admin panel:

```bash
$ python manage.py migrate
$ python manage.py createsuperuser
```

### Step 6: Start the Application and GUI
Finally, start the Django server and GUI by running the `gui.py` script:

```bash
$ python gui.py
```

## Additional Information

### Running the Server
To run the server separately (without the GUI), you can use the following command:

```bash
$ python manage.py runserver
```

### Testing
To run the unit tests, use:

```bash
$ python manage.py test
```

### Environment Variables
Some critical environment variables you may need to add in the `.env` file include:

- `SECRET_KEY`: A secret key for the Django application.
- `DATABASE_URL`: The URL for your database connection.
- `DEBUG`: Set to `True` for development environments and `False` for production.

### Admin Interface
After creating a superuser, access the Django admin interface at:

```
http://127.0.0.1:8000/admin/
```

### GUI Overview
The `gui.py` script starts a graphical user interface that allows easier interaction with the application. Ensure all environment settings are configured before starting it.

### Common Issues
- **Virtual Environment Activation**: If you cannot activate your virtual environment, check your shell settings or use the full path as indicated.
- **Missing Dependencies**: Make sure you have installed all packages from `requirements.txt`. Run `$ pip install -r requirements.txt` again if necessary.



