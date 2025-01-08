FROM python:latest

LABEL Maintainer="roushan.me17"

WORKDIR /usr/app/src

RUN pip install requests

COPY script.py ./

CMD [ "python", "./script.py"]