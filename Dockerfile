FROM registry.access.redhat.com/ubi8/python-38:1

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
