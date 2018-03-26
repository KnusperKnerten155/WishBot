perm = 0

import os
from os import path
import discord

def error(content, channel, client):
    yield from client.send_message(channel, embed=discord.Embed(color=discord.Color.red(), description=content))

def get(server):
    h="SETTINGS" + server.id + "/role"
    if path.isfile(h):
        with open(h) as h:
            return discord.utils.get(server.roles, id=h.read())
    else:
        return None
    
def saveFile(id, server):
    if not path.isdir("SETTINGS/" + server.id):
        os.makedirs("SETTINGS/" + server.id)
    with open("SETTINGS/" + server.id + "/role", "w") as h:
        h.write(id)
        h.close()
    
    
def ex(args, message, client, invoke):

    print(args)

    if len(args) > 0:
        rolename = args.__str__()[1:-1].replace(",","").replace("'","")
        role = discord.utils.get(message.server.roles, name=rolename)
        if role == None:
            yield from error("Dieses Team existiert nicht", message.channel, client)
        else:
            try:
                saveFile(role.id, message.server)
                yield from client.add_roles(message.author, role)
                yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description=("Du bist ` team %s ` beigetreten! Du kannst nun den Teamchat #chat-%s benutzen :wink:  \nBitte schicke dort einen Screenshot vom Trainerprofil :-)" % (role.name, role.name))))
                
            except Exception:
                yield from error("Etwas is schief gelaufen!", message.channel, client)
                raise Exception
            #except discord.Forbidden:
             #   yield from client.send_message(message.channel, "I don't have perms to add roles.")

     

