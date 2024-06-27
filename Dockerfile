
FROM ubuntu:22.04

Install dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    curl \
    htop \
    vim \
    screen \
    && apt-get clean

WORKDIR /app
# pre-copy requirementsm so that rebuilding could start
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED TRUE

# export port
EXPOSE 5000
# Run the server
CMD ["/app/run_server.sh"]
