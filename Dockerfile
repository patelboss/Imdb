# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
# Fixing the typo in the file name, changing "requirements.txt" to "/requirements.txt"
COPY requirements.txt /requirements.txt

# Change the directory to root directory
RUN cd /

# Upgrade pip and install the required packages specified in requirements.txt
# Adding "&&" to combine two commands into one, and removing the "-U" flag as it is unnecessary
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Install any needed packages specified in requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run bot.py when the container launches
CMD ["python", "bot.py"]
