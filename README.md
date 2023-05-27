# Django Portfolio

This repository contains a Django Portfolio application that has been deployed on Google Cloud Run. The app includes functionalities like creating and connecting to a Cloud SQL database, using Secret Manager secret values, hosting static files on Cloud Storage, and using Cloud Build for automated deployment.

The project uses Django 4 and Python 3.8+ is required.

## Project Structure

Here is a high-level overview of the project structure:

```text
.
├── accounts                   # User account related files
├── blogs                      # Blog application files
├── cloudmigrate.yaml          # Cloud migration configuration
├── db.sqlite3                 # SQLite database
├── django_portfolio           # Main Django project configuration
├── Dockerfile                 # Docker configuration file for building the application
├── e2e_test_cleanup.yaml      # End-to-end test cleanup configuration
├── e2e_test.py                # End-to-end test script
├── e2e_test_setup.yaml        # End-to-end test setup configuration
├── home                       # Home application files
├── image_gen                  # Image-generation application files
├── manage.py                  # Django management script
├── media                      # Media files for the application
├── noxfile_config.py          # Noxfile configuration script
├── photos                     # Photo application files
├── polls                      # Polls application files
├── project_commands.sh        # Project command scripts
├── __pycache__                # Python cache files
├── README.md                  # The file you are reading now
├── requirements-test.txt      # Test requirements
├── requirements.txt           # Project requirements
├── retry.sh                   # Retry script
├── static                     # Static files for the application
├── templates                  # Django templates
└── venv                       # Python virtual environment
```