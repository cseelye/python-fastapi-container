# Default port for the service to listen on - this can be overridden at runtime by passing --env UVICORN_PORT=<portnumber>
ARG SERVICE_PORT=12345

FROM ghcr.io/cseelye/ubuntu-base as builder
COPY requirements.txt /tmp/requirements.txt
RUN apt-get update && \
    apt-get install --yes python3-pip && \
    pip install --upgrade pip && \
    pip install --user --upgrade --requirement /tmp/requirements.txt


# Service container target
FROM ghcr.io/cseelye/ubuntu-base as service-container

# Copy python packages from builder stage
COPY --from=builder /root/.local/ /root/.local/
ENV PATH=/root/.local/bin:$PATH

# Copy service code
COPY app/ /service/app/
WORKDIR /service
COPY RELEASE_TAG /version

ARG SERVICE_PORT
ENV UVICORN_PORT=$SERVICE_PORT
ENTRYPOINT ["uvicorn","app.main:app","--host","0.0.0.0"]
CMD ["--log-config", "/app/logconfig.json", "--app-dir", "/service"]


# Development container target
# Add extras to production container to use as dev environment
FROM service-container as dev-container

# Remove the static code from the service container so there is less confusion
RUN rm -rf /service

RUN apt-get update && \
    apt-get install --yes \
        ack \
        curl \
        git \
        jq \
        make \
        python3-pip \
    && apt-get autoremove --yes && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install \
        autopep8 \
        bandit \
        black \
        flake8 \
        mypy \
        pycodestyle \
        pydocstyle \
        pylint \
        pytest \
        yapf

# Install VS Code  Live Share prerequisites
RUN curl -ssfLo ~/vsls-reqs https://aka.ms/vsls-linux-prereq-script && chmod +x ~/vsls-reqs && ~/vsls-reqs

ENTRYPOINT []
CMD ["/bin/bash"]
