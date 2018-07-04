import telebot
import random
from Listino import Listino
from Ordine import Ordini

BOT_TOKEN = ''
bot = telebot.TeleBot(BOT_TOKEN)

str_welcome = """Benvenuto nel bot per ordinare le pizze di *Ulisse*'"""

# Inizializzazione dei contenitori
ordinazioni = Ordini()
listino = Listino()

#Response del listino, calcolarla ogni volta fa merda
response_lista = 'Ecco le pizze che puoi ordinare\n\n'

for key in listino.get_listino().keys():
    response_lista += '*{pizza}*\t{prezzo}€\n'.format(pizza=key.upper(), prezzo=listino.get_price(key))
    response_lista += '**Ingredienti**:{ingredienti}\n\n'.format(ingredienti=listino.get_ingrediente(key))


# Benvenuto
@bot.message_handler(commands=['start', 'Start'])
def subscribe(message):
    bot.send_message(id, str_welcome, parse_mode='Markdown')  # Serve ad aggiungere la formattazione tipo grassetto


# Metodo per stampare il listino delle pizze
@bot.message_handler(commands=['listapizze', 'listapizza', 'lista_pizze'])
def lista_pizze(message):

    # Invio la response
    bot.send_message(message.chat.id, response_lista, parse_mode='Markdown')


# Pizza Random per gli indecisi
# Da testare
@bot.message_handler(commands=['randompizza'])
def pizza_random(message):
    utente = '{Nome} {Cognome}'.format(Nome=message.from_user.first_name, Cognome=message.from_user.last_name)
    # Da sistemare
    pizza_name = random.choice(listino.get_listino().keys())
    prezzo = listino.get_price(pizza_name)
    ordinazioni.add_ordine(utente, pizza_name)
    #Creo la risposta da dare all'utente
    response = 'Hai ordinato una *{pizza_name}*\nCosto: {prezzo} €\nBella vez' \
        .format(pizza_name=pizza_name, prezzo=str(prezzo))
    bot.send_message(message.chat.id, response, parse_mode='Markdown')


# Metodo per rimuovere il proprio ordine
@bot.message_handler(commands=["rimuovi"])
def rimuovi_ordine(message):
    utente = '{Nome} {Cognome}'.format(Nome=message.from_user.first_name, Cognome=message.from_user.last_name)
    ordinazioni.rem_ordine(utente)
    bot.send_message(message.chat.id, 'La tua ordinazione è stata *rimossa*', parse_mode='Markdown')


# Metodo per aggiungere una pizza
# Uno manda il comando ordina poi scrive il nome della pizza
@bot.message_handler(commands=["ordina", "Ordina"])
def ordina_pizza(message):
    text = bot.reply_to(message, 'Dimmi che pizza vorresti prendere tra quelle del listino')
    bot.register_next_step_handler(text, ordina_handler)


def ordina_handler(message):
    # Prendo il nome della pizza
    pizza_name = message.text.lower()
    # Prendo il prezzo dal listino
    prezzo = listino.get_price(pizza_name)
    # Prendo l'utente
    utente = '{Nome} {Cognome}'.format(Nome=message.from_user.first_name, Cognome=message.from_user.last_name)
    # Aggiungo l'ordine
    ordinazioni.add_ordine(utente, pizza_name)
    # Creo la risposta da dare all'utente
    response = 'Hai ordinato una *{pizza_name}*\nCosto: {prezzo} €\nBella vez' \
        .format(pizza_name=pizza_name, prezzo=str(prezzo))
    bot.send_message(message.chat.id, response, parse_mode='Markdown')


# Metodo per completare l'ordine
@bot.message_handler(commands=["completa", "Completa"])
def completa_ordini(message):
    response = ''
    # Pizza - Numero
    totale = {}

    # Guardo il numero di pizze
    for utente in ordinazioni.get_ordini().keys():
        if ordinazioni.get_ordini()[utente] not in totale.keys():
            totale[ordinazioni.get_ordini()[utente]] = 1
        else:
            totale[ordinazioni.get_ordini()[utente]] += 1

    # Produco la response
    for pizza in totale.keys():
        response += 'x{numero} *{pizza}* '.format(numero=totale[pizza], pizza=pizza)
        for user in ordinazioni.get_ordini().keys():
            if ordinazioni.get_ordini()[user] == pizza:
                response += '{user}, '.format(user=user)
        response = response[:len(response)-2] + '\n\n'
        print(response)
    # Rimuovo le ordinazioni
    ordinazioni.clean()

    if not response:
        response = """ Non c'è niente da completare"""

    # Invio la response
    bot.send_message(message.chat.id, response, parse_mode='Markdown')


# Fa partire il bot
while True:
    try:
        bot.polling(none_stop=True, timeout=60)
    except Exception as ex:
        print(ex)
