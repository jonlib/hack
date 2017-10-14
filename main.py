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
        print('-' , workspace["name"])
        l=[]
        for user in workspace["users"]:
            l.append(user["name"])
        dic[workspace["name"]]=[workspace["id"],l]
    return dic

def existWorkspace(name,token):
    for workspace in getWorkspace(token):
        if workspace["name"]==name:
            return True
    return False


def joinWorkspace(name,token):
    for workspace in getWorkspace(token):
        if workspace["name"]==name:
            print("entered", name, "workspace")
            return workspace["id"]

###################################################

def getConversation(token, id):
    getw="https://api.twistapp.com/api/v2/conversations/get"
    Conversations = CallApi(getw, {"Authorization" : token}, {"workspace_id" : id})
    return Conversations

def listConversation(token, id):
    dic={}
    for Conversation in getConversation(token, id):
        print('-' , Conversation["name"])
        dic[Conversation["name"]]=[Conversation["id"]]
    return dic

def existConversation(name, token, id):
    for Conversation in getConversation(token, id):
        if Conversation["name"]==name:
            return True
    return False

def joinConversation(name, token, id):
    for Conversation in getConversation(token, id):
        if Conversation["name"]==name:
            print("entered", name, "Conversation")
            return Conversation["id"]

################################################

def getChannel(token, id):
    getw="https://api.twistapp.com/api/v2/channels/get"
    Channels = CallApi(getw, {"Authorization" : token}, {"workspace_id" : id})
    return Channels

def listChannel(token, id):
    dic={}
    for Channel in getChannel(token, id):
        print('-' , Channel["name"])
        dic[Channel["name"]]=[Channel["id"]]
    return dic

def existChannel(name, token, id):
    for Channel in getChannel(token, id):
        if Channel["name"]==name:
            return True
    return False

def joinChannel(name, token, id):
    for Channel in getChannel(token, id):
        if Channel["name"]==name:
            print("entered", name, "Channel")
            return Channel["id"]

##############################################

###################################################

def getConversation(token, id):
    getw="https://api.twistapp.com/api/v2/conversations/get"
    Conversations = CallApi(getw, {"Authorization" : token}, {"workspace_id" : id})
    return Conversations

def listConversation(token, id):
    dic={}
    for Conversation in getConversation(token, id):
        print('-' , Conversation["name"])
        dic[Conversation["name"]]=[Conversation["id"]]
    return dic

def existConversation(name, token, id):
    for Conversation in getConversation(token, id):
        if Conversation["name"]==name:
            return True
    return False

def joinConversation(name, token, id):
    for Conversation in getConversation(token, id):
        if Conversation["name"]==name:
            print("entered", name, "Conversation")
            return Conversation["id"]

############################################

def sendMessage(convId, message, token):
    url = "https://api.twistapp.com/api/v2/conversation_messages/add"
    query = CallApi(url, {"Authorization" : token}, {"conversation_id" : convId, "content" : message})
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
    curChan = -1
    Workspaces={}
    while 1:
        s = input()
        params = s.split(' ',1)
        sz = len(params)
        command = params[0]

        #if curConv != -1:
            #getMessage()

        if command == "quit":
            return 0

        elif command == "listWorkspace":
            Workspaces = listWorkspace(token)


        elif command == "joinWorkspace":
            if sz < 2:
                Input_numerror(sz-1, 1)
            elif not existWorkspace(params[1], token):
                print("This workspace doesn't exist")
            else: curWorkspace = joinWorkspace(params[1], token)

        elif command == "listConversation":
            listConversation(token, curWorkspace)

        elif command == "joinConversation":
            if sz < 2:
                Input_numerror(sz-1, 1)
            elif not existConversation(params[1], token, curWorkspace):
                print("This conversation doesn't exist")
            else: curConv = joinConversation(params[1], token, curWorkspace)


        elif command == "listChannel":
            listChannel(token, curWorkspace)

        elif command == "joinChannel":
            if sz < 2:
                Input_numerror(sz-1, 1)
            elif not existChannel(params[1], token, curWorkspace):
                print("This conversation doesn't exist")
            else: curChan = joinChannel(params[1], token, curWorkspace)

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
