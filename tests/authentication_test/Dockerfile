FROM python
RUN pip install requests
ADD ./authentication_test.py ./authentication_test.py
#WORKDIR /tests/
WORKDIR .
CMD python3 authentication_test.py

