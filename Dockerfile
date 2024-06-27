
FROM ubuntu:22.04

ENV http_proxy $HTTPS_PROXY
ENV https_proxy $HTTPS_PROXY

# avoid geographical questions from apt-get
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
    software-properties-common && add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get install -y \
    python3.8 \
    python3-pip \
    curl \
    htop \
    vim \
    screen \
    && apt-get clean

# Install dependencies
# RUN apt-get update && apt-get install -y \
#     python3.10 \
#     python3-pip \
#     curl \
#     htop \
#     vim \
#     screen \
#     && apt-get clean


## Enable Python3.8 on Ubuntu 22.04:
# # Install dependencies
# RUN apt-get update && apt-get install -y \
#     software-properties-common

# # # Add deadsnakes PPA for Python 3.8
# RUN add-apt-repository ppa:deadsnakes/ppa && \
#     apt-get update && \
#     apt-get install -y \
#     python3.8 \
#     python3.8-venv \
#     python3.8-dev \
#     python3-pip \
# #     htop \
# #     vim \
# #     screen \
#     && apt-get clean


WORKDIR /app
# pre-copy requirementsm so that rebuilding could start
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Set environment variables
# ENV PYTHONUNBUFFERED TRUE

# export port
EXPOSE 5000
# Run the server
CMD ["/app/run_server.sh"]
