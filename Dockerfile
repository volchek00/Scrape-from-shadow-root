FROM python:3.11.3

WORKDIR /app

COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Start server
CMD ["python", "server.py"]








# FROM python:3.11.3

# WORKDIR /app

# COPY templates/index.html /app/templates/index.html
# COPY server.py /app/server.py
# COPY scrape.py /app/scrape.py
# COPY requirements.txt /app/requirements.txt

# # Install dependencies
# RUN pip install -r /app/requirements.txt

# # Set environment variables
# ENV PYTHONUNBUFFERED=1

# # Expose port
# EXPOSE 8080

# # Start server
# CMD ["python", "server.py"]
