import requests
import json
import sys
import getopt
import asyncio
import time
from threading import Thread

Parent = {}

Node = {}
AdjList = {}
stop = 0
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

###################################################

def getThread(token, channelId):
    getw="https://api.twistapp.com/api/v2/threads/get"
    Threads = CallApi(getw, {"Authorization" : token}, {"channel_id" : channelId})
    return Threads

def listThread(token, channelId):
    dic={}
    for Thread in getThread(token, channelId):
        print('-' , Thread["title"])
        dic[Thread["title"]]=[Thread["id"]]
    return dic

def existThread(name, token, channelId):
    for Thread in getThread(token, channelId):
        if Thread["title"]==name:
            return True
    return False

def joinThread(name, token, channelId):
    for Thread in getThread(token, channelId):
        if Thread["title"]==name:
            print("entered", name, "Thread")
            return Thread["id"]

#################################################


def addComment(threadId, message, token):
    url="https://api.twistapp.com/api/v2/comments/add"
    query = CallApi(url, {"Authorization" : token}, {"thread_id" : threadId, "content" : message})
    return 0

def sendMessage(convId, message, token):
    url = "https://api.twistapp.com/api/v2/conversation_messages/add"
    query = CallApi(url, {"Authorization" : token}, {"conversation_id" : convId, "content" : message})
    #print(query)
    return 0

#if it is a standalone thread call parentId = -1, else use the parent threads id
def addThread(parentId, title, content, channelId, token):
    url = "https://api.twistapp.com/api/v2/threads/add"
    NewThread = CallApi(url, {"Authorization" : token}, {"channel_id" : channelId, "title" : title, "content" : content})
    Node[NewThread["id"]] = 0;
    AdjList[NewThread["id"]] = []

    if parentId != -1:
        Parent[NewThread["id"]] = parentId
        if parentId in Node.keys() :
            Node[parentId] += 1
        else:
            Node[parentId] = 1
            AdjList[parentId] = []

        AdjList[parentId].append(NewThread["id"])

def finishThread(threadId):
    if Node[threadId] != 0:
        print("You cannot finish this thread because there are unfinished child threads")
        return 1
    Node[threadId] -= 1
    threadId = Parent[threadId]
    if threadId != -1:
        Node[threadId] -= 1

def isFinished(threadId):
    if Node[threadId] == -1:
        print("This thread and all it's child are finished")
    elif Node[threadId] == 0:
        print("All the childs are finished, but this thread is still in progress")
    else: print("This Thread still has unfinished childs")

def getThreadTitle(threadId, token):
    url = "https://api.twistapp.com/api/v2/threads/getone"
    q = CallApi(url, {"Authorization" : token}, {"id" : threadId})
    return q["title"]


def dfs(threadId, depth, token):
    tmp = ""
    for i in range(depth):
        tmp += "--"
    print (tmp + getThreadTitle(threadId, token))
    for child in AdjList[threadId]:
        dfs(child, depth+1, token)

def getMessages(token,id,index):
  url = "https://api.twistapp.com/api/v2/conversation_messages/get"
  query = CallApi(url, {"Authorization" : token}, {"conversation_id" : id, "from_obj_index" : index})
  return query

def messageListener(token,curConv):
	global stop
	index = -1
	while stop == 0:
		query = getMessages(token,curConv,index+1)
		for dic in query:
			ifjoin
				print(dic["content"])
				index = dic["obj_index"]
		time.sleep(5)

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
    curChannel = -1
    curThread = -1
    print("Hello", response["name"], '!')
    while 1:
        s = input()
        params = s.split(' ',1)
        sz = len(params)
        command = params[0]

        #if curConv != -1:
            #getMessage()

        if command == "quit":
            return 0

        elif command == "help":
             print(
                 "[list|join] + [Workspace|Conversation|Channel|Thread] [Name] to connect or see the available room\n"+
                 "[sendMessage] to send a message to a conversation\n[addComment] to add a comment to a thread\n" +
                 "[addThread] to create a new parentless thread\n" +
                 "[addChildThread] to create a child thrad to the current Thread\n"+
                 "[finishThread] to finish the child Thread\n" +
                 "[isFinishedThread] to ask the state of the thread and its child\n" +
                 "[quit] if you want to exit the app"
             )
        elif command == "listWorkspace":
            listWorkspace(token)

        elif command == "joinWorkspace":
            if sz < 2:
                Input_numerror(sz-1, 1)
            elif not existWorkspace(params[1], token):
                print("This workspace doesn't exist")
            else: curWorkspace = joinWorkspace(params[1], token)

        elif command == "listConversation":
            if curWorkspace == -1:
                print("you have to join a Workspace to see its Conversations\n try joinWorkspace")
            else: listConversation(token, curWorkspace)

        elif command == "joinConversation":
            if curWorkspace == -1:
                print("you have to join a Workspace to join its Conversations\n try joinWorkspace")
            elif sz < 2:
                Input_numerror(sz-1, 1)
            elif not existConversation(params[1], token, curWorkspace):
                print("This conversation doesn't exist")
            else: curConv = joinConversation(params[1], token, curWorkspace)


        elif command == "listChannel":
            if curWorkspace == -1:
                print("you have to join a Workspace to see its Channels\n try joinWorkspace")
            else: listChannel(token, curWorkspace)

        elif command == "joinChannel":
            if curWorkspace == -1:
                print("you have to join a Workspace to join its Channels\n try joinWorkspace")
            elif sz < 2:
                Input_numerror(sz-1, 1)
            elif not existChannel(params[1], token, curWorkspace):
                print("This channel doesn't exist")
            else: curChannel = joinChannel(params[1], token, curWorkspace)

        elif command == "listThread":
            if curWorkspace == -1:
                print("you have to join a Workspace to see its threads\n try joinWorkspace")
            elif curChannel == -1:
                print("You have to join a Channel to see it's threads\n try joinChannel")
            else: listThread(token, curChannel)

        elif command == "joinThread":
            if curWorkspace == -1:
                print("you have to join a Workspace to join\n try joinWorkspace")
            elif curChannel == -1:
                print("You have to join a Channel to join\n try joinChannel")
            elif sz < 2:
                Input_numerror(sz-1, 1)
            elif not existThread(params[1], token, curChannel):
                print("This Thread  doesn't exist")
            else: curThread = joinThread(params[1], token, curChannel)

        elif command == "sendMessage":
            if curWorkspace == -1:
                print("you have to join a Workspace to send a Message\n try joinWorkspace")
            elif curConv == -1:
                print("You have to join a Conversation to send a Message\n try joinConversation")
            elif sz < 2:
                Input_numerror(sz - 1,1)
            else: sendMessage(curConv, params[1], token)

        elif command == "addComment":
            if curWorkspace == -1:
                print("you have to join a Workspace to send a Comment\n try joinWorkspace")
            elif curChannel == -1:
                print("You have to join a Channel to send a Comment\n try joinChannel")
            elif curThread == -1:
                print("You have to join a Thread to send a Comment\n try joinThread")
            elif sz < 2:
                Input_numerror(sz - 1,1)
            else: addComment(curThread, params[1], token)

        elif command == "addChildThread":
            if curWorkspace == -1:
                print("You have to be in a Workspace to add a child")
            elif curChannel == -1:
                print("You have to be in a Channel to add a child")
            elif curThread == -1:
                print("You have to be in a Thread to add a Child Thread")
            elif sz < 2:
                 Input_numerror(sz - 1,1)
            else:
                print("What's the content for this new thread?")
                Content = input()
                addThread(curThread, params[1], Content, curChannel, token)

        elif command == "addThread":
            if curWorkspace == -1:
                print("You have to be in a Workspace to add a child")
            elif curChannel == -1:
                print("You have to be in a Channel to add a child")
            elif sz < 2:
                 Input_numerror(sz - 1,1)
            else:
                print("What's the content for this new thread?")
                Content = input()
                addThread(-1, params[1], Content, curChannel, token)

        elif command == "finishThread":
            if curWorkspace == -1:
                print("You have to be in a Workspace to finish a Node")
            elif curChannel == -1:
                print("You have to be in a Channel to finish a Node")
            elif curThread == -1:
                print("You have to be in a Thread to finish it")
            else:
                finishThread(curThread)

        elif command == "isFinishedThread":
            if curWorkspace == -1:
                print("You have to be in a Workspace to check a Thread")
            elif curChannel == -1:
                print("You have to be in a Channel to check a Thread")
            elif curThread == -1:
                print("You have to be in a Thread check it")
            else:
                isFinished(curThread)

        elif command == "listChildrenThread":
            if curWorkspace == -1:
                print("You have to be in a Workspace to check a Thread")
            elif curChannel == -1:
                print("You have to be in a Channel to check a Thread")
            elif curThread == -1:
                print("You have to be in a Thread check it")
            else:
                dfs(curThread, 1, token)


        else: print("invalid command - There is a [help] command in case you need it")

main()
