import time
import json
import telebot

# TOKEN DETAILS
TOKEN = "TRON"

BOT_TOKEN = "7178545425:AAHUUxXbKXqDwSt_BYcq31HAUJkvx2qeL6U"
PAYMENT_CHANNEL = "@cookwithd"  # add payment channel here including the '@' sign
OWNER_ID = 5577450357  # write owner's user id here.. get it from @MissRose_Bot by /id
CHANNELS = ["@dailynetflixcookiesfree"]  # add channels to be checked here in the format - ["Channel 1", "Channel 2"]
# you can add as many channels here and also add the '@' sign before channel username
Daily_bonus = 1  # Put daily bonus amount here!
Mini_Withdraw = 0.5  # remove 0 and add the minimum withdraw you want to set
Per_Refer = 0.0001  # add per refer bonus here

bot = telebot.TeleBot(BOT_TOKEN)

def check(id):
    for i in CHANNELS:
        check = bot.get_chat_member(i, id)
        if check.status != 'left':
            pass
        else:
            return False
    return True

bonus = {}

def menu(id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🆔 Account')
    keyboard.row('🙌🏻 Referrals', '🎁 Bonus', '💸 Withdraw')
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
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = "0"
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total'] + 1
            json.dump(data, open('users.json', 'w'))
            print(data)
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(
                text='🤼‍♂️ Joined', callback_data='check'))
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
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = 0
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total'] + 1
            json.dump(data, open('users.json', 'w'))
            print(data)
            markups = telebot.types.InlineKeyboardMarkup()
            markups.add(telebot.types.InlineKeyboardButton(
                text='🤼‍♂️ Joined', callback_data='check'))
            msg_start = "*🍔 To Use This Bot You Need To Join This Channel - \n➡️ @ Fill your channels at line: 101 and 157*"
            bot.send_message(user, msg_start, parse_mode="Markdown", reply_markup=markups)
    except:
        bot.send_message(message.chat.id, "This command has an error, please wait for the admin to fix it.")
        bot.send_message(OWNER_ID, "Your bot got an error. Fix it ASAP!\n Error on command: " + message.text)
        return

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    try:
        ch = check(call.message.chat.id)
        if call.data == 'check':
            if ch:
                data = json.load(open('users.json', 'r'))
                user_id = call.message.chat.id
                user = str(user_id)
                bot.answer_callback_query(callback_query_id=call.id, text='✅ You joined. Now you can earn money.')
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
                bot.answer_callback_query(callback_query_id=call.id, text='❌ You have not joined.')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='🤼‍♂️ Joined', callback_data='check'))
                msg_start = "*🍔 To Use This Bot You Need To Join This Channel - \n➡️ @ Fill your channels at line: 101 and 157*"
                bot.send_message(call.message.chat.id, msg_start, parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"This command had an error: {e}")
        bot.send_message(OWNER_ID, "Your bot got an error. Fix it ASAP!\n Error on command: " + call.data)
        return

@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        if message.text == '🆔 Account':
            data = json.load(open('users.json', 'r'))
            accmsg = '*👮 User : {}\n\n⚙️ Wallet : *`{}`*\n\n💸 Balance : *`{}`* {}*'
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"

            json.dump(data, open('users.json', 'w'))

            balance = data['balance'][user]
            wallet = data['wallet'][user]
            msg = accmsg.format(message.from_user.first_name,
                                wallet, balance, TOKEN)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")
        
        elif message.text == '🙌🏻 Referrals':
            data = json.load(open('users.json', 'r'))
            ref_msg = "*⏯️ Total Invites : {} Users\n\n👥 Referrals System\n\n1 Level:\n🥇 Level°1 - {} {}\n\n🔗 Referral Link ⬇️\n{}*"

            bot_name = bot.get_me().username
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['referred']:
                data['referred'][user] = 0
            json.dump(data, open('users.json', 'w'))

            ref_count = data['referred'][user]
            ref_link = 'https://telegram.me/{}?start={}'.format(
                bot_name, message.chat.id)
            msg = ref_msg.format(ref_count, Per_Refer, TOKEN, ref_link)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")
        
        elif message.text == "⚙️ Set Wallet":
            user_id = message.chat.id
            user = str(user_id)

            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('🚫 Cancel')
            send = bot.send_message(message.chat.id, "_⚠️Send your TRX Wallet Address._",
                                    parse_mode="Markdown", reply_markup=keyboard)
            # Next message will call the name_handler function
            bot.register_next_step_handler(message, trx_address)
        
        elif message.text == "🎁 Bonus":
            user_id = message.chat.id
            user = str(user_id)
            cur_time = int((time.time()))
            data = json.load(open('users.json', 'r'))
            # bot.send_message(user_id, "*🎁 Bonus Button is Under Maintenance*", parse_mode="Markdown")
            if (user_id not in bonus.keys()) or (cur_time - bonus[user_id] > 60*60*24):
                data['balance'][(user)] += Daily_bonus
                bot.send_message(
                    user_id, f"Congrats you just received {Daily_bonus} {TOKEN}")
                bonus[user_id] = cur_time
                json.dump(data, open('users.json', 'w'))
            else:
                bot.send_message(
                    message.chat.id, "❌*You can only take bonus once every 24 hours!*", parse_mode="markdown")
            return
        
        elif message.text == "💸 Withdraw":
            user_id = message.chat.id
            user = str(user_id)

            data = json.load(open('users.json', 'r'))
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            json.dump(data, open('users.json', 'w'))

            bal = data['balance'][user]
            wall = data['wallet'][user]
            if wall == "none":
                bot.send_message(user_id, "_❌ wallet Not set_",
                                 parse_mode="Markdown")
                return
            if bal >= Mini_Withdraw:
                bot.send_message(user_id, "_Enter Your Amount_",
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, amo_with)
            else:
                bot.send_message(
                    user_id, f"_❌Your balance low you should have at least {Mini_Withdraw} {TOKEN} to Withdraw_", parse_mode="Markdown")
                return
        
        elif message.text == "📊Statistics":
            user_id = message.chat.id
            user = str(user_id)
            data = json.load(open('users.json', 'r'))
            msg = "*📊 Total members : {} Users\n\n🥊 Total successful Withdraw : {} {}*"
            msg = msg.format(data['total'], data['totalwith'], TOKEN)
            bot.send_message(user_id, msg, parse_mode="Markdown")
            return

        else:
            bot.send_message(message.chat.id, "❌ Invalid command! Please use the provided inline keyboard.")
            return

    except Exception as e:
        bot.send_message(message.chat.id, f"This command had an error: {e}")
        bot.send_message(OWNER_ID, "Your bot got an error. Fix it ASAP!\n Error on command: "+message.text)
        return
