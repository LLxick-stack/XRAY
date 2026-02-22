import requests
import random
import socket
import ssl
from concurrent.futures import ThreadPoolExecutor

HEADER = (
    "#profile-title: LLxickVPN\n"
    "#profile-update-interval: 12\n"
    "#subscription-userinfo: total=0; expire=17837459931\n"
    "#profile-web-page-url: https://t.me/LLxickVPN\n"
    "#announce: base64:0J/QtdGA0LXQtCDQuNGB0L/QvtC70YzQt9C+0LLQsNC90LjQtSDQv9GA0L7Qv9C40L3Qs9GD0LnRgtC1INCy0YHQtSDRgdC10YDQstC10YDQsCDQuCDQstGL0LHQtdGA0LjRgtC1INC70YPRh9GI0LjQuSDRgdC10YDQstC10YAu0JXRgdC70Lgg0L3QtSDRgNCw0LHQvtGC0LDRjtGCINCy0YHQtSDRgdC10YDQstC10YDQsCDQvtCx0L3QvtCy0LjRgtC1INGB0L/QuNGB0L7QuiDRgdC10YDQstC10YDQvtCyLg==\n\n"
)

EURO_COUNTRIES = [("🇩🇪", "Германия"), ("🇫🇷", "Франция"), ("🇳🇱", "Нидерланды"), ("🇬🇧", "Великобритания")]
SOURCES = [
    ("https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS_mobile.txt", 10, 0),
    ("https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile.txt", 20, 1)
]

def is_alive(link):
    try:
        part = link.split('@')[-1]
        host_port = part.split('?')[0].split('#')[0]
        host, port = host_port.rsplit(':', 1)
        # Просто проверка порта + TLS handshake
        context = ssl._create_unverified_context()
        with socket.create_connection((host, int(port)), timeout=2) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                return link
    except:
        return None

def main():
    final_configs = []
    lte_counter = 1
    for url, limit, source_type in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                raw_links = [l.strip() for l in r.text.splitlines() if "://" in l][:limit+20]
                with ThreadPoolExecutor(max_workers=10) as ex:
                    valid = [res for res in ex.map(is_alive, raw_links) if res][:limit]
                for link in valid:
                    base = link.split('#')[0]
                    name = f"🇷🇺 [LTE] №{lte_counter}" if source_type != 0 else f"{random.choice(EURO_COUNTRIES)[0]} [WI-FI] {random.choice(EURO_COUNTRIES)[1]}"
                    if source_type != 0: lte_counter += 1
                    final_configs.append(f"{base}#{name}")
        except: continue
    with open("results.txt", "w", encoding="utf-8") as f:
        f.write(HEADER + "\n".join(final_configs))

if __name__ == "__main__":
    main()