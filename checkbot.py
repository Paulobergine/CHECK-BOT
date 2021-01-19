import mysql.connector;
import time;
import discord;
import json;

#Récupération du fichier json
with open('data.json') as file:
    data = json.load(file)

#Connexion à la base de données
conn = mysql.connector.connect(host = data['host'], user = data['user'], password = data['password'], database = data['database'])
cursor = conn.cursor()

#Création du bot
client = discord.Client()

#Fonction qui récupère le dernier log
def getLog():
    cursor.execute("SELECT * FROM logs ORDER BY DATE DESC LIMIT 1")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.commit()

#Lancement du bot
@client.event
async def on_ready():
    print("Ready !")

#Lors de la réception d'un message
@client.event
async def on_message(message):

    #Si le message est !check
    if message.content == '!check':
        #Appel infini de la fonction getLog
        while True:
            getLog()
            time.sleep(5)

client.run(data['token'])

conn.close()