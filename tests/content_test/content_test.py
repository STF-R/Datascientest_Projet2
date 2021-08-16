import json
import os
import requests
import time

time.sleep(20)

# définition de l'adresse de l'API
api_address = 'flask'

# port de l'API
api_port = 5002

# requête
username = 'alice'
encoding = 'YWxpY2U6d29uZGVybGFuZA=='
sentences = "life is beautiful amazing and magic", "that sucks and this is expensive. It is the worst experience in my life, could not be worse"
endpoints = '/v1/sentiment', '/v2/sentiment'

for endpoint in endpoints:
    for i, sentence in enumerate(sentences):
        r = requests.get(
                url='http://{address}:{port}{end}'.format(address=api_address, port=api_port, end=endpoint),
                headers={"Authorization": "Basic %s" % encoding},
                params= {'sentence': sentence}
                )
        response = r.json()
        score = float(response['sentence_sentiment_score'])
    
        if i==0:
            expected_result = "superieur a 0"
            if score > 0:
                test_status = 'SUCCESS'
            else:
                test_status = 'FAILURE'
        elif i==1:
            expected_result = "inferieur a 0"
            if score < 0:
                test_status = 'SUCCESS'
            else:
                test_status = 'FAILURE' 

        output = '''
        ============================
                Content test
        ============================
    
        request done at {endpoint}
        | username = {username}
        | sentence = {sentence}
        expected result = {expected_result}
        actual result = {score}
    
        ==>  {test_status}

        '''

        print(output.format(endpoint=endpoint, username=username, sentence=sentence, expected_result=expected_result, score=score, test_status=test_status))

        # impression dans un fichier
        if os.environ.get('LOG') == 1:
            with open('/home/api_test.log', 'a') as file:
                file.write(output)

