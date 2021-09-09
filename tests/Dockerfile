FROM racket/racket:8.2
RUN mkdir app
WORKDIR /app
RUN apt-get update || : && apt-get install python3 python3-pip -y
COPY . .
RUN pip3 install -r requirements.txt
CMD [ "python3", "main.py" ]