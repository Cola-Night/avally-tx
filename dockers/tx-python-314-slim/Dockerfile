# Use an official Python runtime as parent image
FROM python:3.14-slim

# Set the working directory to /workspace
WORKDIR /workspace

# Copy files into /workspace
COPY ./requirements .

# Install
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssl \
    libssl-dev \
    libmagic1 \
    glib2.0

# Install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install `opencv`
RUN pip install --no-cache-dir opencv-python-headless

# Clean up
RUN apt-get purge -y --auto-remove $BUILD_DEPS
RUN rm -rf /var/lib/apt/lists/*

# Run Web service
CMD ["python", "./server-http.py"]
