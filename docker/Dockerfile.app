# Build image
FROM python:3.9 as builder

# Setup virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install build deps use --no-cache to avoid using cached packages
ARG DEBIAN_FRONTEND=noninteractive
ARG TZ=America/Los_Angeles
RUN apt-get update -y && apt-get install -yq --no-install-recommends apt-utils build-essential tk-dev python3-tk && rm -r /var/lib/apt/lists/*

# Install runtime deps
COPY requirements.txt /tmp/requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

# Production image
FROM python:3.9 as xurlpay-api

# Run as non-root
USER 1000:1000

# Copy over virtualenv
ENV VIRTUAL_ENV="/opt/venv"
COPY --from=builder --chown=1000:1000 $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

#ARGS
ARG BUILD_TS
ARG BUILD_BRANCH
ARG BUILD_SHA
# required
ARG APP_CONFIG 

# Copy in app source
WORKDIR /app
COPY --chown=1000:1000 api /app/api
COPY --chown=1000:1000 migrations /app/migrations
ENV PYTHONPATH "${PYTHONPATH}:/app/api"

# export API_TIMESTAMP=$(date +%s)
# export API_GIT_BRANCH=${CIRCLE_BRANCH:-$(git branch | grep \* | cut -d ' ' -f2)}
# export API_GIT_SHA=$(git rev-parse --verify HEAD)

ENV API_TIMESTAMP $BUILD_TS
ENV API_GIT_BRANCH $BUILD_BRANCH
ENV API_GIT_SHA $BUILD_SHA
ENV APP_CONFIG $APP_CONFIG

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "-m","api" ]
