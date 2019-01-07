FROM python:3.6-slim-stretch

WORKDIR /webserver

COPY . /webserver

RUN ls

# Some apt-get issues?
# Should porbbly be in a config
#RUN cat /etc/apt/sources.list
#RUN sed -Ei 's/^# stretch-src /stretch-src /' /etc/apt/sources.list
#RUN apt-get update

# Matplotlib
#RUN apt-get build-dep python-matplotlib

RUN apt-get install -y pkg-config

# TODO: make sure to set dns on Ansible 
# REF: https://docs.docker.com/get-started/part2/#build-the-app
RUN pip install -r requirements.txt

# TODO: public configs?
# https://jupyter-notebook.readthedocs.io/en/stable/public_server.html
RUN jupyter notebook --generate-config

COPY ./.configs/jupyter_notebook_config.py ~/.jupyter

EXPOSE 8789

ENV NAME Energy Exploration

# Notebook
# CMD ["jupyter-notebook"]
CMD ["jupyter-notebook", "--ip=0.0.0.0", "--port=8080", "--allow-root"]
