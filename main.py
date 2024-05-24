import time
import json
import telebot

# TOKEN DETAILS
BOT_TOKEN = "7178545425:AAHofOSNj901M6TNYiJzVsHdMyi-7r-K65s"
PAYMENT_CHANNEL = "@cookwithd"  # add payment channel here including the '@' sign
OWNER_ID = 5577450357  # write owner's user id here
CHANNELS = ["@dailynetflixcookiesfree"]  # add channels to be checked here in the format - ["Channel 1", "Channel 2"]

Mini_Withdraw = 3  # minimum withdrawal amount

bot = telebot.TeleBot(BOT_TOKEN)

def check(id):
    for i in CHANNELS:
        check = bot.get_chat_member(i, id)
        if check.status != 'left':
            pass
        else:
            return False
    return True

def menu(id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🆔 Account')
    keyboard.row('🙌🏻 Referrals', '💸 Withdraw')
    keyboard.row('⚙️ Set Wallet', '📊 Statistics')
    bot.send_message(id, "*🏡 Home*", parse_mode="Markdown", reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = message.chat.id
        msg = message.text
        if msg == '/start':
            user = str(user)
            data = json.load(open('users.json', 'r'))
            if user not in data['referred']:
                data['referred'][user] = 0
                data['total'] = data['total'] + 1
            if user not in data['referby']:
                data['referby'][user] = user
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total'] + 1
            json.dump(data, open('users.json', 'w'))
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='🤼‍♂️ Joined', callback_data='check'))
            msg_start = "*🍔 To Use This Bot You Need To Join This Channel - "
            for i in CHANNELS:
                msg_start += f"\n➡️ {i}\n"
            msg_start += "*"
            bot.send_message(user, msg_start, parse_mode="Markdown", reply_markup=markup)
        else:
            data = json.load(open('users.json', 'r'))
            user = message.chat.id
            user = str(user)
            refid = message.text.split()[1]
            if user not in data['referred']:
                data['referred'][user] = 0
                data['total'] = data['total'] + 1
            if user not in data['referby']:
                data['referby'][user] = refid
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total'] + 1
            json.dump(data, open('users.json', 'w'))
            markups = telebot.types.InlineKeyboardMarkup()
            markups.add(telebot.types.InlineKeyboardButton(text='🤼‍♂️ Joined', callback_data='check'))
            msg_start = "*🍔 To Use This Bot You Need To Join This Channel - \n➡️ @ Fill your channels at line: 101 and 157*"
            bot.send_message(user, msg_start, parse_mode="Markdown", reply_markup=markups)
    except Exception as e:
        bot.send_message(message.chat.id, "This command is having an error. Please wait for fixing the glitch by the admin.")
        bot.send_message(OWNER_ID, "Your bot got an error. Please fix it fast!\n Error on command: " + str(e))

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    try:
        ch = check(call.message.chat.id)
        if call.data == 'check':
            if ch == True:
                data = json.load(open('users.json', 'r'))
                user_id = call.message.chat.id
                user = str(user_id)
                bot.answer_callback_query(callback_query_id=call.id, text='✅ You joined. Now you can earn points.')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                if user not in data['refer']:
                    data['refer'][user] = True

                    if user not in data['referby']:
                        data['referby'][user] = user
                        json.dump(data, open('users.json', 'w'))
                    if int(data['referby'][user]) != user_id:
                        ref_id = data['referby'][user]
                        ref = str(ref_id)
                        if ref not in data['balance']:
                            data['balance'][ref] = 0
                        if ref not in data['referred']:
                            data['referred'][ref] = 0
                        json.dump(data, open('users.json', 'w'))
                        data['balance'][ref] += Per_Refer
                        data['referred'][ref] += 1
                        bot.send_message(ref_id, f"*🏧 New Referral on Level 1, You Got: +{Per_Refer} {TOKEN}*", parse_mode="Markdown")
                        json.dump(data, open('users.json', 'w'))
                        return menu(call.message.chat.id)

                    else:
                        json.dump(data, open('users.json', 'w'))
                        return menu(call.message.chat.id)

                else:
                    json.dump(data, open('users.json', 'w'))
                    menu(call.message.chat.id)

            else:
                bot.answer_callback_query(callback_query_id=call.id, text='❌ You have not joined the required channel.')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='🤼‍♂️ Joined', callback_data='check'))
                msg_start = "*🍔 To Use This Bot You Need To Join This Channel - \n➡️ @ Fill your channels at line: 101 and 157"
                bot.send_message(call.message.chat.id, msg_start, parse_mode="Markdown", reply_markup=markup)
        elif call.data == 'withdraw':
            user = str(call.message.chat.id)
            data = json.load(open('users.json', 'r'))
            if user in data['balance'] and data['balance'][user] >= Mini_Withdraw:
                data['balance'][user] -= Mini_Withdraw
                data['withd'][user] = Mini_Withdraw  # Record withdrawal amount
                json.dump(data, open('users.json', 'w'))
                bot.send_message(user, "You will receive cookies as a reward for withdrawal.")
    except Exception as e:
        bot.send_message(call.message.chat.id, "This command is having an error. Please wait for fixing the glitch by the admin.")
        bot.send_message(OWNER_ID, "Your bot got an error. Please fix it fast!\n Error on command: " + str(e))

if __name__ == '__main__':
    bot.polling(none_stop=True)
