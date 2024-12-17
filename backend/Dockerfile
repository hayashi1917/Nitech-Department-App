# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /code

RUN apk add --no-cache gcc musl-dev mariadb-connector-c-dev

COPY requirements.txt /code
RUN --mount=type=cache,target=/root/.cache/pip pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

FROM builder AS dev-envs

RUN apk update && apk add --no-cache git
RUN addgroup -S docker && adduser -S --shell /bin/bash --ingroup docker vscode

CMD ["flask", "run"]
