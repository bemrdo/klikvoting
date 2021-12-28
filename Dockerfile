FROM surnet/alpine-python-wkhtmltopdf:3.8.5-0.12.6-full

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD [ "python","app.py" ]
