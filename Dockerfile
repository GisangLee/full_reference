FROM python3.9

FROM python:3.9

ENV PYTHONUNBUFFERED 1
RUN apt-get -y update && apt-get clean

RUN mkdir /usr/src/Documents
RUN mkdir /usr/src/Documents/dev
RUN mkdir /usr/src/Documents/dev/full_ref_backend

WORKDIR /usr/src/Documents/dev/full_ref_backend

ADD . .

RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
RUN pip freeze > ./requirements.txt

EXPOSE 8000