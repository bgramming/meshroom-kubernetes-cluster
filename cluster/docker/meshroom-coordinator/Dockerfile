# Meshroom Coordinator - manages workflows and job distribution
FROM meshroom-base:latest

# Install coordinator dependencies
RUN apt-get update && apt-get install -y \
    python3-flask \
    python3-redis \
    python3-celery \
    python3-psutil \
    && rm -rf /var/lib/apt/lists/*

# Install Python coordinator libraries
RUN pip3 install \
    flask \
    redis \
    celery \
    psutil \
    prometheus_client \
    kubernetes \
    argo-workflows

# Create coordinator directories
RUN mkdir -p /opt/coordinator /data/input /data/work /data/output

# Copy coordinator scripts
COPY coordinator-scripts/ /opt/coordinator/
RUN chmod +x /opt/coordinator/*.py

# Set coordinator environment
ENV COORDINATOR_PORT=8080
ENV METRICS_PORT=9090
ENV REDIS_URL=redis://localhost:6379
ENV MAX_WORKERS=8

# Expose ports
EXPOSE 8080 9090

# Create coordinator entrypoint
RUN echo '#!/bin/bash\n\
echo "Starting Meshroom Coordinator..."\n\
echo "Port: $COORDINATOR_PORT"\n\
echo "Metrics Port: $METRICS_PORT"\n\
echo "Max Workers: $MAX_WORKERS"\n\
\n\
# Start coordinator process\n\
exec python3 /opt/coordinator/coordinator.py "$@"' > /coordinator-entrypoint.sh && \
    chmod +x /coordinator-entrypoint.sh

ENTRYPOINT ["/coordinator-entrypoint.sh"]
CMD ["--help"] 