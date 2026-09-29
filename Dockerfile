FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Nuclear API code
COPY . .

# Expose the port
EXPOSE 8000

# Run the API in Ghost Mode
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
