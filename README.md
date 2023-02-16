Project manager app
# step 1
Create virtualenv using python3
    'python -m venv c:\path\to\myenv'

# step 2
install requirements.txt by running this command
    'pip install -r requirements.txt'

# step 3
make migrations and migrate command to migrate all tables
    'python manage.py makemigrations'
    'python manage.py migrate'

# step 4
run the server
    'python manage.py runserver'