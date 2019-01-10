FROM python:3.6-slim

WORKDIR /webserver

COPY . /webserver

RUN pip install -r requirements.txt

WORKDIR /webserver/ts_decomposition

# Crap
RUN  python -m unittest -v test/test_series_sample.py

# Crap
WORKDIR /webserver

EXPOSE 8789

ENV NAME Energy Exploration

CMD ["python", "app.py"]