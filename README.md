SportArena is a sports event management web application built using Django. It allows users to register, log in, create events, join events, manage profiles, and interact with other sports enthusiasts. The system ensures event capacity control, real-time participant tracking, and a
dashboard for both players and organizers.

Features:
User registration and login
Unique username & email for registration
Create, view, edit, and delete events (organizer & admin controlled)
Search for events by name or city
Join events with form input (name, email, contact)
Event organizer dashboard (view join information)
Event creation form with sport-specific inputs
Secure & validated forms
About us section on homepage
Featured events section for highlights
Proper user authentication (only logged-in users can join/add events)

Technologies Used:
Django (Python framework)
SQLite (Default development database)
HTML and CSS for Frontend 
Git & GitHub (Version control and repository)

How to Set Up & Run This Project Locally
1. Install Python
Make sure you have Python installed.
Recommended version: Python 3.10+

2. Clone the Repository
Run this command to clone the project to your local machine:
git clone https://github.com/your-username/your-repo-name.git
Then, navigate into the project directory:
cd your-repo-name

3. Create Virtual Environment
Create a virtual environment to isolate dependencies:
python -m venv env
Activate the virtual environment: On Windows:
env\Scripts\activate
On Linux / MacOS:
source env/bin/activate

4. Install Dependencies
Install required Python packages from the requirements.txt file:
pip install -r requirements.txt

5. Apply Database Migrations
Run Django migrations to set up the database:
python manage.py migrate

6. Create a Superuser (Optional)
Create an admin user to access Django Admin Panel:
python manage.py createsuperuser
Follow the prompts to set username, email, and password.

7. Run the Development Server
Start the Django development server:
python manage.py runserver

8. Open your browser and go to:
http://127.0.0.1:8000/

Images:
<img width="1892" height="897" alt="image" src="https://github.com/user-attachments/assets/4c137857-faad-4e0e-a4aa-ed1d4e323ae1" />
<img width="1891" height="862" alt="image" src="https://github.com/user-attachments/assets/a84e0a88-b5f3-4a15-a2d4-42a9e529c3b2" />

