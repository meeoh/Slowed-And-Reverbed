FROM python:3

WORKDIR /usr/src/app

RUN mkdir downloads
RUN apt update -y
RUN apt install -y ffmpeg sox

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD [ "python", "./one_off.py" ]
CMD [ "python", "./main.py" ]
# CMD ["python2", "./test.py"]
