from requests import get
from random import randint
from threading import Event , Thread
from thread_pool import ThreadPool , CustomThread
from os import system
th = ThreadPool(max_workers=300)
proxy_type = input("enter proxy type : ")
ev = Event()
HTTP_LINK = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
SOCKS4_LINK = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all&ssl=all&anonymity=all"
SOCKS5_LINK = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all"
proxies = []
def setTitle(title):
    try:
        system(f"title \"{title}\"")
    except:
        pass
def get_proxy(refresh_time):
    global proxies
    global ev
    while True:
        http = get(HTTP_LINK)
        socks4 =get(SOCKS4_LINK)
        socks5 = get(SOCKS5_LINK)
        proxies.clear()
        for http_proxy in [{"http":f"http://{x.strip()}","https":f"http://{x.strip()}"} for x in http.text.split("\n")]:
            proxies.append(http_proxy)
        for socks4_proxy in [{"http":f"socks4://{x.strip()}","https":f"socks4://{x.strip()}"} for x in socks4.text.split("\n")]:
            proxies.append(socks4_proxy)
        for socks5_proxy in [{"http":f"socks5://{x.strip()}","https":f"socks5://{x.strip()}"} for x in socks5.text.split("\n")]:
            proxies.append(socks5_proxy)
        ev.wait(refresh_time)
def random_proxy():
    global proxies
    return proxies[randint(0, len(proxies) - 1)]
found = 0
file = open("Results.txt","a+")
def check(ip):
    global file
    global found
    try:
        req = get(f"https://api.hackertarget.com/reverseiplookup/?q={ip}", proxies=random_proxy())
        if req.status_code == 200 and not "API count exceeded" in req.text and not "No DNS A records found" in req.text:
            for x in req.text.split("\n"):
                file.write(x+"\n")
                file.flush()
                found += 1
                setTitle(f"MJ Mass Reverse Ip | Found : {found}")
        else:
            check(ip)
    except Exception as e:
        check(ip)

Thread(target=get_proxy,args=(int(input("Enter Proxy Refresh Interval : ")),)).start()
ev.wait(3)
list_ips = [x.strip() for x in open("ips.txt").readlines()]
for ip in list_ips:
    th.appendThread(CustomThread(target=check,args=(ip,)))
