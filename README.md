**Table of Contents**

This is the code for the example used in the Django Media Explorer [documentation](https://github.com/oxfamamerica/django-media-explorer). 

#Installation

This was tested on Django 1.8.8


```
virtualenv dme
cd dme
source bin/activate
pip install django-media-explorer
git clone https://github.com/oxfamamerica/media_explorer_example.git
./bin/python media_explorer_example/manage.py makemigrations
./bin/python media_explorer_example/manage.py migrate
#Create a superuser so you can add data in the admin section
./bin/python media_explorer_example/manage.py createsuperuser
./bin/python media_explorer_example/manage.py runserver
```

