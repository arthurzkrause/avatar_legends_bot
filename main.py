import random, copy
from typing import Final
from typing import List
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from tokentoken.token_username import TOKEN,BOT_USERNAME
from corebook_content.miscellaneous import miscellaneous_dict

TOKEN
BOT_USERNAME

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
'Hello, welcome to the Poa by Night Bot for the Avatar Legends RPG!\n- Poa by Night, is a World of Darkness encyclopedia project for Porto Alegre, Rio Grande do Sul, Brazil. For more information, visit our networks: https://linktr.ee/poabynight\n\n'
'In this bot for Avatar Legends:\n'
'- Roll dice with /dice and add modifiers with /dice -1\n'
'- Get information about the mechanics with /help.\n'
)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'COMMANDS:\n'
        '/dice: This command randomly generates two 6-sided dice. You can add the number of modifier (/dice 4).\n\n'
        "TERMS\n write in the message:\n"
        "• 'Four Nations': provide info about the four nations\n"
        "• 'Stats': provide info about the four stats\n"
        "• 'Background': provide all choices brackground info\n"
        "• Want to know more about The Trainings? Type 'waterbending', 'technology', 'weapons', etc.\n"
        "• Want to know more about the Core Moves? Type 'core moves' and type one to know more.\n"
        "• Want to know more about the Playbooks? Type 'Playbooks' and type one to know more.\n"
        )

#DADOS
async def dice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    # Divide o texto em partes usando espaços como delimitador
    args = text.split()
    #Possibilita rolar 2d6 sem modificadores
    if len(args) == 1:
        dado_d6 = 2
        rolagem = roll_dice(dado_d6)
        rolagem_int = rolagem
        
        #Mensagens
        if rolagem_int <= 6:
            response_message = f"Fail.\nPutz!"
        elif 7 <= rolagem_int <= 9:
            response_message = f"Weak Hit.\nMay be complications or costs to perform,."
        else:
            response_message = f"Strong Hit\nSuccess without complications!"

        await update.message.reply_text(f'Total: {rolagem_int}\n{response_message}\nNo Mods!')        

    # Verifica se há pelo menos dois argumentos
    elif len(args) == 2:
        # Converte os argumentos para inteiros
        try:
            modificador = int(args[1])
            if -3 <= modificador <= 4:
                dado_d6 = 2
                rolagem = roll_dice(dado_d6)
                rolagem_int = rolagem+ (modificador)
                
                    #Mensagens
                if rolagem_int <= 6:
                    response_message = f"Fail.\nPutz!"
                elif 7 <= rolagem_int <= 9:
                    response_message = f"Weak Hit.\nMay be complications or costs to perform,."
                else:
                    response_message = f"Strong Hit\nSuccess without complications!"

                await update.message.reply_text(f'Total: {rolagem_int}\nMod: {modificador}\n{response_message}')
            else:
                await update.message.reply_text(f'Please provide a modifier between -3 and 4.')
        except ValueError:
            await update.message.reply_text(f'Please provide a number modifier.')

def roll_dice(num_dice):
    # Realiza a rolagem de dados de 6 lados
    results = [random.randint(1, 6) for _ in range(num_dice)]
    return sum(results)



#Handle Responses - se o usuário digitar algo que não um comando,o bot devolve algo escrito
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if processed in miscellaneous_dict:
        return f'{miscellaneous_dict[processed]}'
    else:
        return "Here in the chat you will get information about game terms such as Waterbending, Guiding and comfort, etc. "
  
#Handling Messages - Diferencia se é grupo ou não.
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str=update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response:str=handle_response(new_text)
        else:
            return
    else:
        response: str=handle_response(text)
    print('Bot', response)
    await update.message.reply_text(response)

#Errors - imprimir no terminal pra eu saber o que tá acontecendo
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}'),

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('dice',dice_command))


    #Messages
    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    #Errors
    app.add_error_handler(error)
    
    #Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)