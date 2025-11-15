# Meshroom Worker Node - extends base image with worker-specific tools
FROM meshroom-base:latest

# Install additional worker dependencies
RUN apt-get update && apt-get install -y \
    htop \
    iotop \
    nmon \
    parallel \
    rsync \
    && rm -rf /var/lib/apt/lists/*

# Install Python worker libraries
RUN pip3 install \
    kubernetes \
    redis \
    celery \
    psutil \
    prometheus_client

# Create worker directories
RUN mkdir -p /data/input /data/work /data/output /data/temp

# Copy worker scripts
COPY worker-scripts/ /opt/worker-scripts/
RUN chmod +x /opt/worker-scripts/*.py

# Set worker environment
ENV WORKER_TYPE=photogrammetry
ENV MAX_WORKERS=4
ENV MEMORY_LIMIT=8G

# Create worker entrypoint
RUN echo '#!/bin/bash\n\
echo "Starting Meshroom Worker Node..."\n\
echo "Worker Type: $WORKER_TYPE"\n\
echo "Max Workers: $MAX_WORKERS"\n\
echo "Memory Limit: $MEMORY_LIMIT"\n\
\n\
# Start worker process\n\
exec python3 /opt/worker-scripts/worker.py "$@"' > /worker-entrypoint.sh && \
    chmod +x /worker-entrypoint.sh

ENTRYPOINT ["/worker-entrypoint.sh"]
CMD ["--help"] 