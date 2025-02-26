# Use an official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy everything from your project folder to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your Python app (replace 'app.py' with your main file)
CMD ["python", "Gif maker.py"]
