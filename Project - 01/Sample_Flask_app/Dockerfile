FROM python:3.11-slim

#Se the working directory to /app
WORKDIR /app

# copy the requirements file into the container
COPY requirements.txt requirements.txt

#install the python packages inside the container
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

# Set the port on which this app should run
# (informational; you still need -p to publish the port)
EXPOSE 5000

#Command to run the application
CMD ["python", "app.py"]