import datetime

import mysql.connector;
import time;
import discord;
import json;

#Récupération du fichier json
with open('data.json') as file:
    data = json.load(file)

#Connexion à la base de données
conn = mysql.connector.connect(host=data['host'], user=data['user'], password=data['password'], database=data['database'])
cursor = conn.cursor()

#Création du bot
client = discord.Client()

#Initialisation du nombre de logs
def setupNblogs():
    cursor.execute("SELECT COUNT(*) FROM logs")
    result = cursor.fetchone()
    return result[0]

#Lancement du bot
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='les logs'))
    print("Ready !")

#Lors de la réception d'un message
@client.event
async def on_message(message):

    #Si le message est !check
    if message.content == '!check':
        #Affichage du lancement de la détection
        embedCheck = discord.Embed(title="Check started", description="The bot will check every 5 secondes if a new log has been created !")
        await message.channel.send(embed=embedCheck)

        #Appel infini de la fonction getLog
        nbLogs = setupNblogs()
        print("Initial logs number : ", nbLogs)
        while True:
            if setupNblogs() > nbLogs:
                #Si nouveau log, alors affichage des informations de ce dernier
                cursor.execute("SELECT * FROM logs ORDER BY DATE DESC LIMIT 1")
                result = cursor.fetchone()

                #Si IP connue
                if result[3] in data['IPS']:
                    embedNewLog = discord.Embed(title=":ballot_box_with_check: New Log ! :ballot_box_with_check:")
                #Sinon
                else:
                    await message.channel.send("<@353154747185889281>")
                    embedNewLog = discord.Embed(title=":warning: Unknown ip ! :warning:")

                embedNewLog.add_field(name="Type", value=result[1], inline=True)
                embedNewLog.add_field(name="Objet", value=result[2], inline=True)
                embedNewLog.add_field(name="Info", value=result[3], inline=True)
                embedNewLog.timestamp = datetime.datetime.now()
                await message.channel.send(embed=embedNewLog)

                nbLogs = setupNblogs()
                time.sleep(5)

            conn.commit()

client.run(data['token'])

conn.close()