import os, telebot, time
from telebot import types
BOT_TOKEN=os.environ["BOT_TOKEN"]
ADMIN_ID=int(os.environ["ADMIN_ID"])
bot=telebot.TeleBot(BOT_TOKEN)
users={}
def anti_fraud(uid):
    uid=str(uid)
    if uid not in users: users[uid]={"coins":0,"last":0,"clicks":[],"ban":0}
    u=users[uid]; now=time.time()
    if u.get("ban",0)>now: return False, f"BAN {int((u['ban']-now)/60)}m"
    if now-u.get("last",0)<15: return False, f"WAIT {int(15-(now-u['last']))}s"
    clicks=u.get("clicks",[])[-4:]+[now]
    if len(clicks)==5 and clicks[-1]-clicks[0]<25:
        u["ban"]=now+3600; return False, "BOT Ban 1h"
    u["clicks"]=clicks; u["last"]=now; return True,"OK"
@bot.message_handler(commands=['start'])
def start(m):
    uid=str(m.from_user.id)
    if uid not in users: users[uid]={"coins":0,"last":0,"clicks":[],"ban":0}
    mk=types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("Watch Ad (+1)",callback_data="watch"))
    mk.add(types.InlineKeyboardButton("Balance",callback_data="bal"))
    mk.add(types.InlineKeyboardButton("Withdraw",callback_data="with"))
    bot.send_message(m.chat.id,f"Bot LIVE Coins: {users[uid]['coins']}",reply_markup=mk)
@bot.callback_query_handler(func=lambda c:True)
def call(c):
    uid=str(c.from_user.id); chat=c.message.chat.id
    if uid not in users: users[uid]={"coins":0,"last":0,"clicks":[],"ban":0}
    if c.data=="watch":
        ok,msg=anti_fraud(c.from_user.id)
        if not ok: bot.answer_callback_query(c.id,msg,show_alert=True); return
        users[uid]["coins"]+=1
        bot.send_message(chat,f"+1 Total: {users[uid]['coins']}")
    if c.data=="bal": bot.send_message(chat,f"Coins: {users[uid]['coins']}")
    if c.data=="with": bot.send_message(chat,f"Coins: {users[uid]['coins']} Need 100")
bot.infinity_polling()
