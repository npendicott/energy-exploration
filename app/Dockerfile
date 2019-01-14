FROM python:3.6-slim

WORKDIR /webserver

COPY . /webserver

RUN pip install -r requirements.txt

# I feel like I should not have to change directories
#WORKDIR /webserver/ts_decomposition

# Also fell like I should run one blanket "test", instead of for each module
RUN  python -m unittest -v test/test_series_sample.py

# Reset
#WORKDIR /webserver

EXPOSE 8789

ENV NAME Energy Exploration

CMD ["python", "app.py"]