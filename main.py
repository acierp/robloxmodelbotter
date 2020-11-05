import requests
import threading
from itertools import cycle
import ctypes
import os
import termcolor
from colorama import Fore
from termcolor import colored 
os.system('color')
buys = []

with open('cookies.txt','r+', encoding='utf-8') as f:
	logins = f.read().splitlines()
with open('proxies.txt','r+', encoding='utf-8') as f:
	ProxyPool = cycle(f.read().splitlines())

def getSellerInfo(cookie, itemid, proxy):
    cookies = {
        '.ROBLOSECURITY': cookie
    }
    url = f"https://api.roblox.com/Marketplace/ProductInfo?assetId={itemid}"
    r = requests.get(url, cookies=cookies, proxies=proxy)
    json = r.json()
    if "Authorization" in str(json) and "errors" in str(json):
        print(f"{Fore.WHITE}[ {Fore.RED}- {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Ran into an error | Invalid cookie")
        return False
    creatorid = int(json['Creator']['Id'])
    ProductId = int(json['ProductId'])
    return [creatorid, ProductId]

def deleteAsset(modelid, cookie, proxy):
    token = getToken(cookie, proxy)
    cookies = {
        ".ROBLOSECURITY": cookie
    }
    headers= {
        'x-csrf-token': token
    }
    r = requests.post('https://www.roblox.com/asset/delete-from-inventory', data={'assetId': modelid}, proxies=proxy, cookies=cookies, headers=headers)
    if r.status_code == 200:
        print(f"{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Success | Successfully deleted from inventory")
    else:
        print(f"{Fore.WHITE}[ {Fore.RED}- {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Ran into an error | Error when deleting from inventory")
def getToken(cookie, proxy):
    cookies = {
        '.ROBLOSECURITY': cookie
    }
    r = requests.post("https://auth.roblox.com/v1/logout", cookies=cookies, proxies=proxy)
    if r.status_code == 200 or r.status_code == 403:
        return r.headers["x-csrf-token"]
def buyModel(modelid, cookie, proxy):
    while True:
        token = getToken(cookie, proxy)
        cookies = {
            '.ROBLOSECURITY': cookie
        }
        sellerinfo = getSellerInfo(cookie, modelid, proxy)
        sellerid = sellerinfo[0]
        productid = sellerinfo[1]
        buy = requests.post(f'https://economy.roblox.com/v1/purchases/products/{productid}', data={'expectedCurrency': 1, 'expectedPrice': 0, 'expectedSellerId': sellerid}, cookies=cookies, headers={'x-csrf-token': token}, proxies=proxy)
        if buy.status_code == 200:
            print(colored(f'Successfully purchased model. Total: {len(buys)}', color='green'))
            print(f"{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Success | Successfully purchased model. Total: {Fore.WHITE}{len(buys)}")
            buys.append(productid)
        elif buy.status_code == 429:
            print(f"{Fore.WHITE}[ {Fore.RED}- {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Ran into an error | Ratelimited on proxy")
        deleteAsset(modelid, cookie, proxy)

print(f"{Fore.WHITE}[ {Fore.CYAN}§ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Roblox Model Botter made by {Fore.WHITE}Acier{Fore.LIGHTBLACK_EX} | Licensed under {Fore.WHITE}MIT {Fore.LIGHTBLACK_EX}License\n")
threads = input(f"{Fore.WHITE}[ {Fore.CYAN}- {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Threads: ")
modelid = input(f"{Fore.WHITE}[ {Fore.CYAN}- {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Model ID: ")
os.system('cls()')
for i in range(int(threads)):
        for login in logins:
            proxy = {
                "https": "https://" + next(ProxyPool)
            }
        threading.Thread(target=buyModel, args=[modelid, login, proxy]).start()
while True:
    ctypes.windll.kernel32.SetConsoleTitleW(f"Total Purchased: {len(buys)}")
