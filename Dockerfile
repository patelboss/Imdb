# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create a symbolic link named "session" that points to the long string session
RUN ln -s /path/to/long/string/session session

# Run the Telegram client with the short name of the symbolic link
CMD python bot.py
