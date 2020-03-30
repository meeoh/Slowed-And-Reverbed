FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN mkdir downloads
RUN apt update -y
RUN apt install -y ffmpeg sox
RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

CMD [ "python", "./main.py" ]
