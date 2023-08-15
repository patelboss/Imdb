
# Use official Python an runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip  # Upgrade pip to the latest version
# Fixing the typo in requirements.txt
RUN sed -i 's/string-sessions/string-session/' requirements.txt
RUN pip install -r requirements.txt  # Install the required packages

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run bot.py when the container launches
CMD ["python", "bot.py"]
