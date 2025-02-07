# Booking System Project

## Project Setup

### Prerequisites

Ensure you have the following installed on your machine:

- Docker
- Docker Compose

### Docker

This project uses Docker for containerization. Make sure you have Docker installed and running on your machine.

### Docker Compose

The project uses Docker Compose to manage multiple services, including the PostgreSQL database and Django application.

### Environment Variables

The project uses a `.env` file to manage environment variables. Here is the structure of the `.env` file:

```env
DEBUG=True
SECRET_KEY='your-secret-key'
DATABASE_NAME='reservation'
DATABASE_USER='postgres'
DATABASE_PASSWORD='your-db-password'
DATABASE_HOST='db'
DATABASE_PORT='5432'

DJANGO_SUPERUSER_USERNAME='admin'
DJANGO_SUPERUSER_EMAIL='admin@example.com'
DJANGO_SUPERUSER_PASSWORD='adminpassword'
```



## Setting Up the Database
The PostgreSQL database is set up in a separate Docker container. The configuration for the database container is defined in the docker-compose.yml file.  
Setting Up the Django Project

### Clone the repository:  
```bash
git clone https://github.com/SoroushZol/2FJB7-45309.git
cd bookingSystem
```

### Create a .env file:  
Create a .env file in the root directory of the project and add the environment variables as shown above.  

### Running the Project with Python
To run the project with Python, follow these steps:

### Install the project dependencies:  
```bash 
pip install -r requirements.txt
```

### Apply the Django migrations:  
```bash
python manage.py migrate
```

### Create a superuser:  
```bash
python manage.py createsuperuser
```

### Start the Django development server:  
```bash
python manage.py runserver
``` 

This will start the Django development server and make the application accessible at http://localhost:8000.


### Build and run the Docker containers:  
```
docker-compose up --build
```
This command will build the Docker images and start the containers. It will also run the Django migrations and create a default superuser using the environment variables defined in the .env file.

## Running the Project with Docker
To run the project with Docker, follow these steps:  
- Ensure the PostgreSQL container is running:  `docker-compose up db`
- Start the Django application container:  `docker-compose up web`

This will start the Django application and make it accessible at http://localhost:8000.  

### Access the Django admin panel:  
Open your browser and go to http://localhost:8000/admin. Use the superuser credentials defined in the .env file to log in.

### Additional Commands
- Rebuild the Docker containers:  `docker-compose up --build`
- Stop the Docker containers:  `docker-compose down`
- View running containers:   `docker ps`