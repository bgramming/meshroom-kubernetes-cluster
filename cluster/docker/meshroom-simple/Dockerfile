# Lightweight Meshroom container for testing
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install only essential packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install \
    numpy \
    pillow \
    pyyaml \
    requests

# Create working directory
WORKDIR /data

# Create directories
RUN mkdir -p /data/input /data/output /data/temp /data/logs

# Simple entrypoint for testing
RUN echo '#!/bin/bash\necho "Meshroom container ready"\necho "Input: /data/input"\necho "Output: /data/output"\ntail -f /dev/null' > /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
