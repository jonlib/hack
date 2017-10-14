import requests
import json
import sys
import getopt

#llama a la api
def CallApi (url, Headers, Params):
    q = json.loads(requests.get(url, headers = Headers, params = Params).content)
    #tratamiento de error
    return q

def Input_numerror(cur,need):
    print("needed", need, "parameters and only got", cur)


def getWorkspace(token):
    getw="https://api.twistapp.com/api/v2/workspaces/get"
    getworkspace= CallApi(getw, {"Authorization" : token}, {})
    return getworkspace


def listWorkspace(token):
    dic={}
    for workspace in getWorkspace(token):
        l=[]
        for user in workspace["users"]:
            l.append(user["name"])
        dic[workspace["name"]]=[workspace["id"],l]

    print(dic.keys())
    return dic

def sendMessage(Conv_id, message, token):
    url = "https://api.twistapp.com/api/v2/conversation_messages/add"
    query = CallApi(url, {"Authorization" : token}, {"conversation_id" : id, "content" : message})
    #print(query)
    return 0

def main():
    #argument extractor
    parameter = { "email" : "deanzhu2@gmail.com",
                  "password" : "dGOri9CY4O2k"
    }
    login_url = "https://api.twistapp.com/api/v2/users/login"
    response = CallApi(login_url, {},  parameter)
    token = "Bearer " +  response["token"]
    curWorkspace = -1
    curConv = -1
    Workspaces={}
    while 1:
        s = input()
        params = s.split(' ',1)
        sz = len(params)
        command = params[0]
        print(params[1])
        if command == "quit":
            return 0

        elif command == "listWorkspace":
            Workspaces = listWorkspace(token)


        elif command == "joinWorkspace":
            if sz < 2:
                Input_numerror(sz-1, 1)
            elif not WorkspaceExist(params[1], token):
                print("This workspace doesn't exist")
            else: curWorkspace = joinWorkspace(params[1], token)

        elif command == "listConversation":
            listConversation(token)

        elif command == "joinConversation":
            if sz < 2:
                Input_numerror(sz-1, 1)
            elif not ConversationExist(params[1], token):
                print("This workspace doesn't exist")
            else: curConv = joinConversation(params[1], token)


        elif command == "sendMessage":
            if curWorkspace == -1:
                print("you have to join a Workspace to send a Message\n try joinWorkspace")
            elif curConv == -1:
                print("You have to join a Conversation to send a Message\n try joinConversation")
            elif sz < 2:
                Input_numerror(sz - 1,1)
            else: sendMessage(curConv, params[1], token)
        else: print("invalid command")

main()
