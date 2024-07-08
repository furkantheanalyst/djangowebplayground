# Pull base image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED 1

RUN mkdir /wdtestdocker

# Set work directory
WORKDIR /wdtestdocker

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY ./app ./app

WORKDIR /wdtestdocker/app