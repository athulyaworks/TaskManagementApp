# Task Management App
A simple Django web application designed to provide efficient task management, enabling users to create, update, delete tasks, and organize them by categories, due dates, and priority levels.

## Features
- User registration and login
- Ability to create, update, and delete tasks
- Categorization of tasks by type or project
- Assignment of due dates and priority levels

## Technologies Used
- Python
- Django
- HTML, CSS (Bootstrap)
- JavaScript
- SQLite

## How to Run
1. Clone the repository:  
   `git clone https://github.com/athulyaworks/TaskManagementApp.git`
2. Navigate to the project directory:  
   `cd myproject`
3. Set up a virtual environment (recommended):  
   `python -m venv myenv`
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
5. Install the required dependencies:  
   `pip install -r requirements.txt`
6. Apply database migrations:  
   `python manage.py migrate`
7. Create a superuser account to access the admin panel:  
   `python manage.py createsuperuser`
8. Start the development server:  
   `python manage.py runserver`
9. Open your browser and go to `http://127.0.0.1:8000/` to view the app.

## Notes
- Ensure Python is installed on your system for the project to run properly.

## Author
Athulya Jolly
