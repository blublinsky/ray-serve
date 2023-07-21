FROM docker.io/rayproject/ray:2.5.1-py310
RUN pip3 install -U "ray[serve]"==2.5.1
COPY fruit.py fruit.py
COPY hello.py hello.py
COPY fruit_url.py fruit_url.py
COPY hello_url.py hello_url.py
