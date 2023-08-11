FROM ubuntu:latest
WORKDIR /web_app

RUN  apt update && apt install -y python3 python3-pip python-is-python3 && \
     pip3 install --upgrade pip && \
     pip3 install poetry

COPY . /web_app
RUN poetry export -f requirements.txt --output requirements.txt
RUN pip3 install -r requirements.txt



CMD ["gunicorn", "-w", "4", "card_maker:web:routes:app"]