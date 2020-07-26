FROM python:3
ADD * app/
ADD templates /add
RUN pip3 install --upgrade pip
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip3 install psycopg2~=2.6
RUN apt-get autoremove -y gcc
RUN pip3 install -r app/requirements.txt
CMD ["python", "/app/main.py"]