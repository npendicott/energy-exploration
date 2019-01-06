FROM resin/raspberry-pi-python:latest

# Enable systemd
ENV INITSYSTEM on

WORKDIR /webserver

COPY ./app /webserver

RUN ls

# TODO: make sure to set dns on Ansible 
# REF: https://docs.docker.com/get-started/part2/#build-the-app
RUN pip install -r requirements.txt

EXPOSE 8789

ENV NAME Energy Exploration

CMD ["python", "app.py"]
