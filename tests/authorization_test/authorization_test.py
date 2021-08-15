import os
import requests
import time

time.sleep(2)

# définition de l'adresse de l'API
api_address = 'fastapi'

# port de l'API
api_port = 8000

# requête
usernames = 'alice', 'bob'
passwords = 'wonderland', 'builder'
sentence = "I love it, it's fantastic !"
endpoints = '/v1/sentiment', '/v2/sentiment'
expected_results = 200, 200, 200, 403

count=0
for endpoint in endpoints:
    for user, passwd in zip(usernames, passwords):
        expected_result = expected_results[count]
        count+=1
        r = requests.get(
                url='http://{address}:{port}{end}'.format(address=api_address, port=api_port, end=endpoint),
                params= {
                    'username': user,
                    'password': passwd,
                    'sentence': sentence
                    }
                )

       # statut de la requête
        status_code = r.status_code

        # affichage des résultats
        if status_code == expected_result:
            test_status = 'SUCCESS'
        else:
            test_status = 'FAILURE'
            
        output = '''
        ============================
            Authentication test
        ============================

        request done at {endpoint}
        | username = {user}
        | password = {passwd}
        expected result = {expected_result}
        actual restult = {status_code}

        ==>  {test_status}

        '''

        print(output.format(endpoint=endpoint, user=user, passwd=passwd, expected_result=expected_result, status_code=status_code, test_status=test_status))

        # impression dans un fichier
        if os.environ.get('LOG') == 1:
            with open('api_test.log', 'a') as file:
                file.write(output)

