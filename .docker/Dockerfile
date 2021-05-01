FROM python:3.9

EXPOSE 5000/tcp

WORKDIR /app

RUN apt-get install && apt-get dist-upgrade -y

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN touch .env
RUN rm -rf .env

CMD [ "python", "./app.py" ]