FROM python:3.9-alpine

WORKDIR /app

RUN apk add iproute2

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir tests
RUN mkdir tests/project

COPY tests tests
COPY project tests/project

RUN touch .env
RUN rm -rf .env

CMD [ "pytest" ]