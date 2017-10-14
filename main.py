import requests
import json

parameter = { "email" : "deanzhu2@gmail.com",
              "password" : "dGOri9CY4O2k"
              }

response = requests.get("https://api.twistapp.com/api/v2/users/login", params = parameter)
Webjson = json.loads(response.content)
token = "Bearer " +  Webjson["token"]
workspace = Webjson["default_workspace"]

convapi = "https://api.twistapp.com/api/v2/conversations/get"

query1 = json.loads(requests.get(convapi,headers= {"Authorization" : token}, params={"workspace_id" : workspace}).content)
print(query1[0])
