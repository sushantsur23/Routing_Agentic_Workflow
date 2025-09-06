FROM python:3.11-slim

# Set working directory to /app
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Add the current directory to Python path
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run the application
CMD ["streamlit", "run", "app/mainapp.py", "--server.port=8000", "--server.address=0.0.0.0"]