FROM python:3.12.3-alpine3.18
LABEL maintainer="roman.hlodann@gmail.com"

WORKDIR app/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN adduser \
    --disabled-password \
    --no-create-home \
    user

RUN mkdir -p /media/
RUN chown -R user /app/
RUN chown -R user /media/
RUN chown -R 755 /media/

USER user
