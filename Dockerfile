FROM python:3.11-slim  # Start with a slim Python base image

WORKDIR /code  # Set the working directory inside the container 

COPY requirements.txt requirements.txt  # Copy your requirements file first
RUN pip install -r requirements.txt  # Install dependencies

COPY . .  # Copy the rest of your application code

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]  # Run Uvicorn server
