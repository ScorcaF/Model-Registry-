import requests
import os
from base64 import b64decode
from base64 import b64encode
import time

#Add the MLP and CNN tflite models developed in LAB3-Ex1 to the Model Registry.

#need to put the ip of the rpi
url = 'http://192.168.178.34:8080/add'


#read in binary mode 
tflite_mlp = open('mlp.tflite', 'rb').read()
#encoding in b64 binary object
mlp_encoded = b64encode(tflite_mlp)
#creating b64 string
mlp_string = mlp_encoded.decode()

#define body and send PUT request
body = {'name': 'mlp',
       'model':  mlp_string}
r = requests.put(url, json=body)

if r.status_code == 200:
    print(r.status_code)
    #print('MLP successfully inserted.')
else:
    print(r.status_code)
    
tflite_cnn = open('cnn.tflite', 'rb').read()
#encoding in b64 binary object
cnn_encoded = b64encode(tflite_cnn)
#creating b64 string
cnn_string = cnn_encoded.decode()

#define body and send PUT request
body = {'name': 'cnn',
       'model':  cnn_string}
r = requests.put(url, json=body)
if r.status_code == 200:
    print(r.status_code)
    #print('CNN successfully inserted.')
else:
    print(r.status_code)
    
    
#List the models stored in the Model Registry and verify that their number is two. 
url = 'http://192.168.178.34:8080/list'
#send GET rquest
r = requests.get(url)
if r.status_code == 200:
    body = r.json()
    models_list = body["models"]
    
    print(tuple(models_list))
        
    if len(models_list) == 2:
        print("Two models in the list.")
        
    else: 
        print("Error: {} models in the list.".format(len(models_list)))
        
# 3. Invoke the registry to measure and predict temperature and humidity with the CNN model. Set tthres=0.1 and hthres=0.2. 

url = 'http://192.168.178.34:8080/predict?model=cnn&ttres=0.1&htres=0.2'
r = requests.get(url)


# In[ ]:




