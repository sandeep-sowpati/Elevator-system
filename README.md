# Elevator-system

## Elevator System Problem

In a real world we can see a Builing having multiple elevators and each elevator have different properties.

## Properties:
Can take user requests and based on that elevator moves up and down. and I have used a constraints that the destination floor can t be greater than the max_floor of the building and along with that it can't go beyond Zero , we can change it in future i.e. we make it dynamic in the future for each building by adding a new property called bottom_floor(default=0) and currently we are using two Elevator status modes (operational / non operaational ) and with door properties(open /closed). and for API Endpoints Documentation I am using Django Spectactular (Swagger UI) for easier access.


## Installation:

Using a venv is highly recommended and you can Activate a venv  using python module
```
python -m venev env_name
env_name\Scripts\activate.bat #windows
source venv_name/bin/activate #unix including macOS
```

Once the venv is activated please clone the github repo using
```
git clone https://github.com/sandeep-sowpati/Elevator-system.git
```

Once the cloning is completed please install the requirements
```
cd Elevator-system
pip install -r requirements.txt
```

#### Running Server

```
python manage.py runserver
```


## Additional Notes:

1. using Django ORM for querying so it can perfectly work with any other SQL Databses(postgres, MYSQl, MSSQL)

if you want to update the database please change the databases code
```
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': ‘<database_name>’,
       'USER': '<database_username>',
       'PASSWORD': '<password>',
       'HOST': '<database_hostname_or_ip>',
       'PORT': '<database_port>',
   }
}
```

2. Requests are implemented/fullfilled immediately without any delay threads will takke care of it If we want to put some time we can make it wait.

3. API documentation is mentioned unde /api/docs
