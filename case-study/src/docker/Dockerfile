FROM python:3.8

WORKDIR /app

COPY app.py /app
COPY requirements.txt /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["app.py"]
 