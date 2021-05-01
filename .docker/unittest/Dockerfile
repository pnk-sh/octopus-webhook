FROM python:3.9-alpine

WORKDIR /app

RUN apk update && apk upgrade
RUN apk add \
    iproute2

RUN apk add --no-cache --virtual .build-deps gcc musl-dev
RUN pip install cython
RUN apk del .build-deps gcc musl-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir tests
RUN mkdir tests/project

COPY tests tests
COPY project tests/project

RUN touch .env
RUN rm -rf .env

CMD [ "pytest" ]