#!/bin/bash

# Define the script functions

format_code() {
    echo "Formatting code..."
    black .
}

display_structure() {
    echo "Displaying directory structure..."
    tree -I 'venv'
}

freeze_requirements() {
    echo "Freezing current environment packages..."
    pip freeze > requirements.txt
}

create_django_app() {
    if [ -z "$1" ]
    then
        echo "Please provide the name of the Django app to create."
    else
        echo "Creating Django app: $1 ..."
        python manage.py startapp $1
    fi
}

# Call the function based on the first script argument

case $1 in
    format_code) format_code ;;
    display_structure) display_structure ;;
    freeze_requirements) freeze_requirements ;;
    create_django_app) create_django_app $2 ;;
    *) echo "Invalid command" ;;
esac
