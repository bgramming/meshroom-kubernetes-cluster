# Base Meshroom Docker image with AMD ROCm support
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV MESHROOM_VERSION=2023.2.0
ENV ALICEVISION_VERSION=2.4.0

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    curl \
    python3 \
    python3-pip \
    python3-dev \
    libboost-all-dev \
    libopencv-dev \
    libeigen3-dev \
    libceres-dev \
    libsuitesparse-dev \
    libgflags-dev \
    libgoogle-glog-dev \
    libhdf5-dev \
    libtiff-dev \
    libjpeg-dev \
    libpng-dev \
    libgdal-dev \
    libproj-dev \
    libgeotiff-dev \
    libcgal-dev \
    libcgal-qt5-dev \
    qtbase5-dev \
    qttools5-dev \
    libqt5opengl5-dev \
    libqt5svg5-dev \
    qtbase5-dev-tools \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install \
    numpy \
    scipy \
    matplotlib \
    pillow \
    opencv-python \
    pyyaml \
    requests \
    tqdm

# Install AMD ROCm (if available)
RUN wget -qO - https://repo.radeon.com/rocm/rocm.gpg.key | gpg --dearmor -o /etc/apt/trusted.gpg.d/rocm.gpg && \
    echo 'deb [arch=amd64] https://repo.radeon.com/rocm/apt/5.7 ubuntu main' > /etc/apt/sources.list.d/rocm.list && \
    apt-get update && \
    apt-get install -y rocm-opencl-dev rocm-opencl-runtime || echo "ROCm installation failed, continuing without GPU acceleration" && \
    rm -rf /var/lib/apt/lists/*

# Clone and build AliceVision
WORKDIR /opt
RUN git clone --recursive https://github.com/alicevision/AliceVision.git && \
    cd AliceVision && \
    git checkout v${ALICEVISION_VERSION} && \
    mkdir build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DALICEVISION_USE_OPENCL=ON && \
    make -j$(nproc) && \
    make install

# Clone and build Meshroom
RUN git clone --recursive https://github.com/alicevision/meshroom.git && \
    cd meshroom && \
    git checkout v${MESHROOM_VERSION} && \
    mkdir build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release && \
    make -j$(nproc) && \
    make install

# Set environment variables
ENV PATH="/opt/meshroom/bin:${PATH}"
ENV LD_LIBRARY_PATH="/opt/AliceVision/lib:/usr/local/lib"
ENV PYTHONPATH="/opt/meshroom/python"

# Create working directory
WORKDIR /data

# Create entrypoint script
RUN echo '#!/bin/bash\n\
if [ "$1" = "meshroom" ]; then\n\
    shift\n\
    exec /opt/meshroom/bin/meshroom_photogrammetry "$@"\n\
elif [ "$1" = "alicevision" ]; then\n\
    shift\n\
    exec /opt/AliceVision/bin/aliceVision "$@"\n\
else\n\
    exec "$@"\n\
fi' > /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["meshroom"] 