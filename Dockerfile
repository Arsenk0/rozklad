# Use the full Python image instead of the slim variant to ensure all dependencies are available
FROM python:3.11

# Prevent Python from buffering stdout and stderr (useful for logging)
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for Python packages that need to be compiled
# You can add more dependencies if your packages require them
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean

# Copy requirements.txt before other files to leverage Docker caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Specify the command to run the application
CMD ["python", "your_script.py"]
