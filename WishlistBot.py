import discord
from discord import Game, Embed
import asyncio as asyncio
import logging
import datetime
import time
import random
import cmd_role
import perms

client = discord.Client()

prefix = "$"



commands = { "team": cmd_role}



config_file = open('config.conf')
log_file = 'wishlistbot.log'

playing = prefix+"help; Deine Wünsche"
for line in config_file:
    if line.startswith("token="):
        token = line[line.find("=")+1:].rstrip("\n")
    if line.startswith('playing=$help; Deine Wünsche'):
        playing = line[line.find("=")+1:].rstrip("\n")

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=log_file, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter( \
                       '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


#Python Console Login
@client.event
async def on_ready():
           print("Botogel logged in as")
           print(client.user.name)
           print(client.user.id)
           print("----------")
           await client.change_presence(game=discord.Game(name=playing))




@client.event
@asyncio.coroutine
def on_message(message):
    if message.attachments:        
        yield from client.add_reaction(message, '\U0001F44D')
    #Teamzuordnung
    if message.content.startswith(prefix):
        invoke = message.content[len(prefix):].split(" ")[0]
        args = message.content.split(" ")[1:]
        if commands.__contains__(invoke):
            cmd = commands[invoke]
            try:
                if not perms.check(message.author, cmd.perm):
                    yield from client.send_message(message.channel, embed=Embed(color=discord.Color.red(), description=("Du kannst dich nicht zwei Teams zuordnen!" % invoke)))
                    return
                yield from cmd.ex(args, message, client, invoke)
            except:
                cmd.ex(args, message, client, invoke)
                pass

        
            
        #membercount
        elif message.content.startswith(prefix+'membercount') or message.content.startswith(prefix+'Membercount'):
            current =  datetime.datetime.now()
            now = current.strftime ("%Y-%m-%d, um %H:%M:%S Uhr")

            #listen initialisieren
            InstinctMembers = [ ]
            MysticMembers = [ ]
            ValorMembers = [ ]
            BotMembers = [ ]
           
            x = message.server.members
            for member in x:
                    #print(member.name)
                    for role in member.roles:
                        if role.name=='instinct': #instinct
                            InstinctMembers.append(member.name)
                        elif role.name=='mystic': #mystic
                            MysticMembers.append(member.name)
                        elif role.name=='valor': #valor
                            ValorMembers.append(member.name)
                        elif role.name=='Bots': #bots
                            BotMembers.append(member.name)
          
            InstinctCount = len(InstinctMembers)
            #print('Instinct: \n' + str(InstinctMembers))
            print(InstinctCount)
            
            MysticCount = len(MysticMembers)
            #print('Mystic: \n' + str(MysticMembers))
            print(MysticCount)
            
            ValorCount = len(ValorMembers)
            #print('Valor: \n' + str(ValorMembers))
            print(ValorCount)

            BotCount = len(BotMembers)
            #print('Bots: \n' + str(BotMembers))
            print(BotCount)
            
            embed=Embed(
                   color=discord.Color.green()   ,
                   description=("**Trainer gesamt:**  %s \n**<:instinct:410759229473947649> Instinct:** %s \n**<:mystic:365202251691851786> Mystic:** %s \n**<:valor:410759232334462977> Valor:** %s \n\n**Bots:** %s  \n\nam %s" % (message.server.member_count, InstinctCount, MysticCount, ValorCount, BotCount , now))
                   

                )
            embed.set_author(name="PokéGo MS" , icon_url="https://www.pokewiki.de/images/9/96/Sugimori_001.png")
            
            yield from client.send_message(message.channel, embed=embed)

  
        #ich mag pokemon
        elif message.content.startswith(prefix+'ich mag pokemon') or message.content.startswith(prefix+'ich mag Pokemon') or message.content.startswith(prefix+'Ich mag Pokemon'):
            yield from client.add_reaction(message, '\U0001F44D')
            yield from client.send_message(message.channel, 'Ich auch :slight_smile: ')
            yield from client.send_message(message.channel, 'https://giphy.com/gifs/ash-s9x3racq2ZL5m ')
        #attack
        elif message.content.startswith(prefix+'attack') or message.content.startswith(prefix+'Attack'):
            random_attack = random.choice(open("Attacks.txt").readlines())
            print(random_attack)
            yield from client.send_message(message.channel, random_attack)
            
        #wunsch        
        elif message.content.startswith(prefix+'wunsch') or message.content.startswith(prefix+'Wunsch'): 
            current =  datetime.datetime.now()
            now = current.strftime ("[%d-%m-%Y / %H:%M:%S Uhr]")
               
            file = open("wishes.txt","a")                        
            file.write("Wunsch: " + message.content[8:] + now + " (" + str(message.author) + ") " + "\n")
                
            file.close()
            yield from client.send_message(message.channel, 'Danke! Dein Wunsch wurde entgegengenommen :smiley: ')

        #liste
        elif message.content.startswith(prefix+'liste') or message.content.startswith(prefix+'Liste'):
            file = open("wishes.txt","r")
            yield from client.send_message(message.channel, embed=Embed(color=discord.Color.orange(), description=(file.read())))            
            file.close()
            
        #spawns
        elif message.content.startswith(prefix+'spawns') or message.content.startswith(prefix+'Spawns'):
            s = open("spawns.txt","r")
            yield from client.send_message(message.channel, embed=Embed(color=discord.Color.orange(), description=(s.read())))            
            s.close()

        #raids
        elif message.content.startswith(prefix+'raids') or message.content.startswith(prefix+'Raids'):
            r = open("raids.txt","r")
            yield from client.send_message(message.channel, embed=Embed(color=discord.Color.orange(), description=(r.read())))            
            r.close()        

        #help
        elif message.content.startswith(prefix+'help') or message.content.startswith(prefix+'Help'):
            yield from client.send_message(message.channel, embed=Embed(color=discord.Color.orange(), description=("Es gibt folgende Befehle: \n\n**$team [Teamname]**: Fügt dich einem Team hinzu \n**$raids**: Sagt dir, welche Raids in den Raidkanälen durchgegeben werden\n**$spawns**: Sagt dir, welche wilden Pokémon in den Spawnkanälen durchgegeben werden\n**$ich mag pokemon**: Gibt dir eine Antwort \n**$attack**: Gibt eine zufällige Attacke zurück \n**$wunsch [beliebiger Inhalt]**: Wünsche dir etwas, was du in Zukunft gerne auf dem Server/Map hättest! \n**$liste**: Gibt dir eine Liste, was bisher schon gewünscht wurde \n**$membercount**: Gibt aus, wie viele User auf dem Server sind \n**$invite**: Schickt dir per PN eien Invite-Link für den Server" )))

        #invite
        elif message.content.startswith(prefix+'invite') or message.content.startswith(prefix+'Invite'):
            embed=Embed(
                   color=discord.Color.green()   ,
                   description=("Hey " + message.author.name +"!\n\n**mit diesem Link kommt man auf den Server:**  \nhttps://discord.gg/QEXfBJB \n**Discord im Apple App Store:** \nhttps://itunes.apple.com/de/app/discord/id985746746?mt=8 \n**Discord im Google Play Store:** \nhttps://play.google.com/store/apps/details?id=com.discord&hl=de ")
                )
            embed.set_author(name="PokéGo MS" , icon_url="https://www.pokewiki.de/images/9/96/Sugimori_001.png")
            yield from client.send_message(message.author, embed=embed)
            yield from client.send_message(message.channel, "Ich habe dir eine PN geschickt " + message.author.name + " :wink:")
       
      
    
       #meetup
        elif message.content.startswith(prefix+'meetup') or message.content.startswith(prefix+'Meetup'):
            meetup = discord.utils.get(message.server.roles, name='meetup')
            if meetup in message.author.roles:
                yield from client.remove_roles(message.author, meetup)
                yield from client.send_message(message.channel,embed=Embed(color=discord.Color.green(), description=( "%s \nDu bist aus der Rolle ** %s ** *ausgetreten* und wirst ab jetzt *nicht mehr* benachrichtigt, wenn jemand eine wichtige Nachricht für das nächste Meetup sendet <:Wobbuffet:365242567312539659> " % (message.author.mention , meetup.name))))
            else:
                yield from client.add_roles(message.author, meetup)
                yield from client.send_message(message.channel,embed=Embed(color=discord.Color.green(), description=( "%s \nDu bist der Rolle ** %s ** *beigetreten* und wirst ab jetzt *immer* benachrichtigt, wenn jemand eine wichtige Nachricht für das nächste Meetup sendet <:Wobbuffet:365242567312539659> " % (message.author.mention , meetup.name))))

       #admincheck
        elif message.content.startswith(prefix+'count') or message.content.startswith(prefix+'Count'):
            admin = discord.utils.get(message.server.roles, name='admin')
            if admin in message.author.roles:
                current =  datetime.datetime.now()
                now = current.strftime ("%Y-%m-%d, um %H:%M Uhr")

                #listen initialisieren
                InstinctMembers = [ ]
                MysticMembers = [ ]
                ValorMembers = [ ]
                BotMembers = [ ]
                CheckedMembers = [ ]
           
                x = message.server.members
                for member in x:
                    #print(member.name)
                    for role in member.roles:
                        if role.name=='instinct': #instinct
                            InstinctMembers.append(member.name)
                        elif role.name=='mystic': #mystic
                            MysticMembers.append(member.name)
                        elif role.name=='valor': #valor
                            ValorMembers.append(member.name)
                        elif role.name=='Bots': #bots
                            BotMembers.append(member.name)
                        elif role.name=='Checked': #checked
                            CheckedMembers.append(member.name)
                    
          
                InstinctCount = len(InstinctMembers)
                #print('Instinct: \n' + str(InstinctMembers))
                print(InstinctCount)
            
                MysticCount = len(MysticMembers)
                #print('Mystic: \n' + str(MysticMembers))
                print(MysticCount)
            
                ValorCount = len(ValorMembers)
                #print('Valor: \n' + str(ValorMembers))
                print(ValorCount)

                BotCount = len(BotMembers)
                #print('Bots: \n' + str(BotMembers))
                print(BotCount)

                CheckedCount = len(CheckedMembers)
                #print('Akzeptiert: \n' + str(CheckedMembers))
                print(CheckedCount)
                percentage=CheckedCount/message.server.member_count*100
                print('Satz: ' + str(percentage))
                CheckedPercentage=str(int(percentage))
            
                embed=Embed(
                   color=discord.Color.green()   ,
                   description=("**Trainer gesamt:**  %s \n**<:instinct:410759229473947649> Instinct:** %s \n**<:mystic:365202251691851786> Mystic:** %s \n**<:valor:410759232334462977> Valor:** %s \n\n**Bots:** %s  \n\n**Checked:** %s (%s %s) \n\nam %s" % (message.server.member_count, InstinctCount, MysticCount, ValorCount, BotCount , CheckedCount, CheckedPercentage , '%' ,  now))
                   

                    )
                embed.set_author(name="PokéGo MS" , icon_url="https://www.pokewiki.de/images/9/96/Sugimori_001.png")
            
                yield from client.send_message(message.channel, embed=embed)

            if not admin in message.author.roles:
                embed=Embed(
                   color=discord.Color.red()   ,
                   description=('Du bist nicht dazu authorisiert, diesen Befehl zu nutzen')
                   

                    )
                yield from client.send_message(message.channel, embed=embed)
                
            
            
       #Errorcode
        else:
            yield from client.send_message(message.channel, embed=Embed(color=discord.Color.red(), description=("Dieser Befehl `%s` ist nicht gültig!" % invoke)))


            



#Willkommensnachricht             
@client.event
@asyncio.coroutine
def on_member_join(member):
    yield from client.send_message(member, embed=Embed(color=discord.Color.green(), description=( "Hey %s :-)  \n\nWillkommen auf dem Server %s \n\nBitte lies als erstes %s, %s und ordne dich einem Team in %s zu,  dann findest du dich hier sicher schnell zurecht :smiley: \n\nWir wünschen dir viel Spaß bei uns! "% (member.name, member.server.name, discord.utils.get(member.server.channels, id="331120649021947905").mention, discord.utils.get(member.server.channels, id="348825175862804481").mention, discord.utils.get(member.server.channels, id="331113926135906305").mention ))))





#Einloggen
client.run('Mzg1MTYwNTgyNjY5NjY0MjU4.DP9X9Q.Cuk1i0V7LElHACkiO1LCGkFPIAI')



