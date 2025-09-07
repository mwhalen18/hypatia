FROM python:3.12-bookworm
RUN apt update

COPY ./requirements.txt ./requirements.txt

RUN python3 -m pip install -U pip
RUN python3 -m pip install -r ./requirements.txt

RUN mkdir /app/

COPY ./data/ /app/data/
COPY ./hypatia /app/hypatia/
COPY ./main.py /app/main.py
COPY ./data/ /app/data/
# COPY ./plex.py /app/plex.py

WORKDIR /app
ENTRYPOINT [ "python3" ]
