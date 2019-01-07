FROM python:3.6-slim-stretch

WORKDIR /webserver

COPY . /webserver

RUN ls

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
