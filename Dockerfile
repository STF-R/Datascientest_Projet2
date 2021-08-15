FROM ubuntu:20.04

ADD ./requirements.txt ./api.py ./reviews.csv ./credentials.csv ./model1.pkl ./vectorizer.pkl ./model1_test_score.pkl ./

RUN apt update && apt install python3-pip libmysqlclient-dev -y && pip install -r requirements.txt

EXPOSE 8000

CMD python3 api.py
