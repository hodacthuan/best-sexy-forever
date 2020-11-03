FROM python:3.6.10-slim


WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY ./server/requirements.txt .

RUN pip3 install -r ./requirements.txt