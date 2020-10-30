FROM python:3.6.10-slim


WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip3 install \
        six \
        bs4 \
        redis \
        django==3.0.5 \
        sqlparse==0.2.4 \
        djongo==1.3.3 \
        pytest \
        ipcalc \
        demjson \
        requests \
        botocore \
        virtualenv \
        mongoengine \
        coloredlogs