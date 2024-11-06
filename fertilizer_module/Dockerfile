FROM python:3.11-alpine


WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask API
EXPOSE 5000

# Run the application
CMD ["python", "FlaskApp.py"]
