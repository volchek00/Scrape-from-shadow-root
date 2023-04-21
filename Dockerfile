FROM python:3.11.3

WORKDIR /app

COPY templates/index.html /app/index.html
COPY server.py /app/server.py
COPY scrape.py /app/scrape.py

COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Expose port
EXPOSE 8080

# Start server
CMD ["python", "server.py"]