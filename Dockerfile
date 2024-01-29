# Getting base image using Python
FROM python:3.8

# Creates a working directory in the container
WORKDIR /app

# Copies the requirements file in the working directory
COPY requirements.txt /app/

# Installs the necessary libraries for requirements
RUN pip install -r requirements.txt

# Copies the remaining files from host system to a container
COPY . /app

# Exposing this port from the container
EXPOSE 8501

# Runs the streamlit app after building a container
CMD ["streamlit", "run", "app.py"]