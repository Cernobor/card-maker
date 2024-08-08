FROM python:3.12

RUN apt-get update && apt-get install -y net-tools netcat-traditional

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

CMD ["/wait-for-it.sh", "cardmaker_db:3306", "--", "python", "app.py"]
