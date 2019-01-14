FROM python:3.6-slim

WORKDIR /webserver

COPY . /webserver

RUN pip install -r requirements.txt
# TODO: break here into a seperate container to save build time?

# Do I need to keep this?
# I feel like I should not have to change directories
#WORKDIR /webserver/ts_decomposition

# Also fell like I should run one blanket "test", instead of for each module
# RUN  python -m unittest -v test/test_series_sample.py
RUN python -m unittest discover -v

# Reset
#WORKDIR /webserver

EXPOSE 8789

ENV NAME 'Energy Exploration'

# Should overwrite local envs in .env file
ENV ENERGY_DB_HOST 'influx'

CMD ["python", "app.py"]