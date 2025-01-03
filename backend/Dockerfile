FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /code

RUN apk add --no-cache gcc musl-dev mariadb-connector-c-dev
COPY requirements.txt /code/
RUN --mount=type=cache,target=/root/.cache/pip pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV PYTHONPATH=/code

FROM builder AS dev-envs
RUN apk add --no-cache git

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
