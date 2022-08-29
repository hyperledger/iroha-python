FROM rust:1.64

RUN set -ex; \
    apt-get update -yq; \
    apt-get install -y --no-install-recommends python3-pip patchelf; \
    pip3 install --upgrade pip; \
    pip3 install maturin; \
    rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY . .
RUN maturin build
RUN pip3 install target/wheels/*

WORKDIR /test
