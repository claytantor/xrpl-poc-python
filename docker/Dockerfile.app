# Build image
FROM python:3.7 as builder

# Setup virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install build deps use --no-cache to avoid using cached packages

# RUN apt-get install -y --no-install-recommends build-essential python3-tk tk-dev 
ARG DEBIAN_FRONTEND=noninteractive
ARG TZ=America/Los_Angeles
RUN apt-get update -y && apt-get install -yq --no-install-recommends apt-utils build-essential tk-dev python3-tk && rm -r /var/lib/apt/lists/*

# Install runtime deps
COPY requirements.txt /tmp/requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

# Production image
FROM python:3.7-slim as rapaygo

# Run as non-root
USER 1000:1000

# Copy over virtualenv
ENV VIRTUAL_ENV="/opt/venv"
COPY --from=builder --chown=1000:1000 $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


# Copy in app source
WORKDIR /app
COPY --chown=1000:1000 api /app/api
COPY --chown=1000:1000 migrations /app/migrations
ENV PYTHONPATH "${PYTHONPATH}:/app/api"

EXPOSE 5200

ENTRYPOINT [ "flask" ]

CMD [ "run","-h","0.0.0.0","-p","5000" ]
