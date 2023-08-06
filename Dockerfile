# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /requirements.txt

RUN cd /
RUN pip3 install -U pip && pip3 install -U -r requirements.txt

# Install any needed packages specified in requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run bot.py when the container launches
CMD ["python", "bot.py"]
