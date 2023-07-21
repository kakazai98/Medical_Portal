Install VS code latest version
Download and install python 3.10

Open the project foler into VS code.
 
Open a new terminal and run the following commands

    pip install whitenoise
    pip install django-cors-headers  
    pip install django
    pip install django-tempus-dominus
    pip install matplotlib

after these are installed successfully.

Make sure your terminal is in the directory of the project where manage.py is.
Use the following command to check.

    ls

Most likey you will be in the main folder so just use the following command.

    cd project

Run the following commands

    python manage.py makemigrations website 
    python manage.py sqlmigrate website 0001
    python manage.py migrate

This will create the app for you. Now add data using these commands. This is some sample data.

    python manage.py shell

This will open a command prompt. using the following command there.

    exec(open('sample_data.py').read())
    exit()

Now you have sample data to work with. You have 3 patients you can login as.

username = johndoe@example.com
password = 123

username = alicejohnson@example.com
password = 123

username = davidsmith@example.com
password = 123

you can also login as administration

username = admin
password = admin

now run the server using

    python manage.py runserver

Open this link on any browser (preferably Chrome)

http://127.0.0.1:8000/