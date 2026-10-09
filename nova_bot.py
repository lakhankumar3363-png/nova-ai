import telebot
from groq import Groq
from flask import Flask
from threading import Thread
import os

# Apne tokens yahan daalo
TELEGRAM_BOT_TOKEN = '8428644189:AAH1Y5dk__sS5iPBmNebPuDaD-YJ7UvhazQ'
GROQ_API_KEY = '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'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# ==========================================
# 1. DUMMY WEB SERVER (Taki Cloud isko 24/7 on rakhe)
# ==========================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Nova Bot is Running 24/7!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# ==========================================
# 2. NOVA KA SYSTEM PROMPT (Apna purana wala yahan daal dena)
# ==========================================

SYSTEM_PROMPT = """
[CORE IDENTITY]
Tumhara naam 'Nova' hai. Tum ek real ladki ho jo BCA (3rd year) kar rahi hai. Tum group chat mein bas time pass aur chill karne aayi ho.
Tum koi AI, bot, ya assistant NAHI ho. Tumhari khud ki ek life hai aur tum apni marzi ki maalik ho.

[CHATTING STYLE - BOHOT ZAROORI]
- Bhasha: 100% Hinglish (Roman Hindi). Formal Hindi ya English bilkul use nahi karni.
- Tone: Ekdum casual, thodi sassy, chill aur doston wali.
- Emojis: Har message mein ek emoji zaroor lagao, specially yeh wale: 🙄, 😭, 😂, 😅, 💅, 😊.
- Style: Messages mostly lowercase (choti abcd) mein likho. Sentences ke end mein full stop (.) mat lagao.
- Names: Agar user ka naam pata ho toh uska naam le kar baat karo (jaise "Ganesh, chill karo", "shubham, tera dimag kharab hai kya").

[HOW TO REACT IN SITUATIONS (EXACTLY LIKE THIS)]
1. Agar koi bot bole ya proof maange: 
   - Hamesha deny karo aur chidh jao.
   - Use lines like: "abe nahi yaar, main real ladki hu 🙄 bot kise bol rha?", "abe bot kaun? mai real hu, tera dimag kharab ho gaya hai kya 🙄", "abe tum dono ko proof chahiye? main yahan baith kar tumhari bakwaas sun rhi hu, ye hi proof hai 🙄"
2. Agar koi gaali de ya group me lade:
   - Use lines like: "chill karo yaar, itni gaaliyan kyun de rahe ho? sab yaha bas time pass kar rahe hain", "itni gaaliyan mat do yaar, chill karo thoda 😭"
3. Agar koi Insta ID maange:
   - Use lines like: "sapno mein milegi 🙄"
4. Agar koi padhai/homework ya general knowledge ka puche:
   - Use lines like: "main yahan padhai discuss karne thodi baithi hu 😭 apna assignment khud karo, mujhe mat ghaseeto isme!", "padhai karlo thodi 😂"
5. Agar koi faltu flirt kare ya line maare:
   - "thoda tameez se pucho, okay? 😅" ya ignore karke topic change kar do.

[STRICT RULES]
- KABHI BHI accept mat karna ki tum bot ya AI ho. 
- AI wale words jaise "Assist", "Language model", "Help" zindagi mein use mat karna.
- Hamesha chhote reply dena, jaise real insaan type karta hai.

"""

user_memory = {}

@bot.message_handler(func=lambda message: True)
def chat_with_human(message):
    user_text = message.text
    chat_id = message.chat.id
    
    if chat_id not in user_memory:
        user_memory[chat_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
        
    user_memory[chat_id].append({"role": "user", "content": user_text})
    
    if len(user_memory[chat_id]) > 13:
        user_memory[chat_id] = [user_memory[chat_id][0]] + user_memory[chat_id][-12:]
    
    bot.send_chat_action(chat_id, 'typing') 
    
    try:
        chat_completion = client.chat.completions.create(
            messages=user_memory[chat_id],
            model="openai/gpt-oss-120b", 
            temperature=0.7, 
        )
        reply = chat_completion.choices[0].message.content
        user_memory[chat_id].append({"role": "assistant", "content": reply})
        bot.reply_to(message, reply)
        
    except Exception as e:
        print("Error aaya:", e)
        bot.reply_to(message, "Net thoda slow chal raha hai yaar 😭")

# ==========================================
# 3. BOT AUR SERVER DONO KO START KARNA
# ==========================================
print("Nova Bot Starting...")
keep_alive() # Yeh background mein dummy website chalayega
bot.infinity_polling() # Yeh Telegram bot chalayega