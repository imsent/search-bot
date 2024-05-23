FROM python:3.12

COPY . /background/

COPY requirements.txt requirements.txt

WORKDIR /background

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT python start.py