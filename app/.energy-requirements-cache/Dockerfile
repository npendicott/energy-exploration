FROM python:3.6-slim

WORKDIR /req

COPY ./requirements.txt /req

RUN pip install -r requirements.txt

CMD ["python", "-V"]
