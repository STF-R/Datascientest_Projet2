import os
import requests
import time

time.sleep(20)

# définition de l'adresse de l'API
api_address = 'flask'

# port de l'API
api_port = 5002

# requête
#alice : YWxpY2U6d29uZGVybGFuZA==
#bob : Ym9iOmJ1aWxkZXI= 
#clementine : Y2xlbWVudGluZTptYW5kYXJpbmU=
usernames = 'alice', 'bob', 'clementine'
base64encode = 'YWxpY2U6d29uZGVybGFuZA==', 'Ym9iOmJ1aWxkZXI=', 'Y2xlbWVudGluZTptYW5kYXJpbmU='
expected_results = 200, 200, 401
for user, encoding, expected_result in zip(usernames, base64encode, expected_results):
    r = requests.get(
            url='http://{address}:{port}/permissions'.format(code64=encoding, address=api_address, port=api_port),
            headers={"Authorization": "Basic %s" % encoding})
#            params = {
#                'header':"Authorization: Basic %s" % encoding
#                }
#            )

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

    request done at "/permissions"
    | username = {user}
    | auth_base64_code = {encoding}
    expected result = {expected_result}
    actual result = {status_code}

    ==>  {test_status}

    '''

    print(output.format(user=user, encoding=encoding, expected_result=expected_result, status_code=status_code, test_status=test_status))

    # impression dans un fichier
    if os.environ.get('LOG') == 1:
        with open('api_test.log', 'a') as file:
            file.write(output)
