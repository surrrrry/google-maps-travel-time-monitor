FROM python:3.12-bullseye
RUN apt update
RUN apt-get update
RUN apt-get -y install python3-pip git vim
RUN python3 -m pip install --upgrade pip

ARG SECRETS_FILE_PATH

COPY ./app /app
COPY $SECRETS_FILE_PATH /app/secrets/secrets.json
RUN pip3 install -r ./app/requirements.txt
RUN cd app && sh install.sh

ARG GIT_PAT
RUN pip3 install git+https://$GIT_PAT@github.com/surrrrry/peaklib@v0.2.9

CMD tenmplateservice -c /app/configs/prod.json