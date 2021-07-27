FROM racket/racket:8.2
RUN mkdir app
COPY . .
RUN apt-get update || : && apt-get install python3 python3-pip -y
RUN pip3 install pyinputplus colorama
CMD [ "python3", "main.py" ]