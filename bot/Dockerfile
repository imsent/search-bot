FROM python:3.12

COPY . /bot

COPY requirements.txt requirements.txt

WORKDIR /bot

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT python start.py