from evdev import InputDevice, categorize, ecodes
import time, sys, json, requests

try:
    print('try open btremote.conf')
    with open('btremote.conf') as json_file:
        settings = json.load(json_file)
    print('file open ok')
except:
    print('no file btremote.conf')
    sys.exit() 

print('---settings---')
print(settings)
print('-----')

VOLSTEP = settings['volstep']
BTDEV = settings['btdevice']
PLAYER = settings['player']
SERVER = settings['server']
VOLUP = settings['volup']
VOLDN = settings['voldn']
PAUSE =  settings['pause']
PREV =  settings['prev']
NEXT =  settings['next']
MUTE =  settings['mute']
HOME =  settings['home']
EXIT =  settings['exit']
SYNC =  settings['google']
channel = 0

ACTIONS = {
VOLUP:["mixer", "volume", "+" + VOLSTEP ], 
VOLDN:["mixer", "volume", "-" + VOLSTEP ]
}

#{"id":"1","method":"slim.request","params":["JBL white",["pause"]]}
#{"id":"1","method":"slim.request","params":["JBL white",["mixer", "volume", "-5"]]}
#{"id":"1","method":"slim.request","params":["JBL white",["favorites","playlist","play","item_id:1"]]}
#{"id":"1","method":"slim.request","params":["JBL white",["sync","-"]]}
#{"id":"1","method":"slim.request","params":["HomePod",["sync","JBL white"]]}

print('ACTIONS')
for key,value in ACTIONS.items(): 
    print(key, ':', value)

def voldn():
    print('VOL DN')
    try:
        r = requests.post(SERVER, json={"id":"1","method":"slim.request","params":["JBL white",["mixer", "volume", "-"+VOLSTEP]]}, timeout=5)
        print("RESPONSE ", r)
    except:
        print('server error')

def volup():
    print('VOL UP')
    try:
        r = requests.post(SERVER, json={"id":"1","method":"slim.request","params":["JBL white",["mixer", "volume", "+"+VOLSTEP]]}, timeout=5)
        print("RESPONSE ", r)
    except:
        print('server error')

def pause():
    print('PAUSE')
    try:
        r = requests.post(SERVER, json={"id":"1","method":"slim.request","params":["JBL white",["pause"]]}, timeout=5)
        print("RESPONSE ", r)
    except:
        print('server error')

def first():
    global channel
    print('FIRST')
    channel = 0
    print('CHANNEL ', channel)
    try:
        r = requests.post(SERVER, json={"id":"1","method":"slim.request","params":["JBL white",["favorites","playlist","play","item_id:" + str(channel)]]}, timeout=5)
        print("RESPONSE ", r)
    except:
        print('server error')

def prev():
    global channel
    print('PREV')
    channel = channel -1
    if channel < 0:
        channel = 10
        print('CHANNEL ', channel)
    try:
        r = requests.post(SERVER, json={"id":"1","method":"slim.request","params":["JBL white",["favorites","playlist","play","item_id:" + str(channel)]]}, timeout=5)
        print("RESPONSE ", r)
    except:
        print('server error')

def next():
    global channel
    print('NEXT')
    channel = channel + 1
    if channel > 10:
        channel = 0
        print('CHANNEL ', channel)
    try:
        r = requests.post(SERVER, json={"id":"1","method":"slim.request","params":["JBL white",["favorites","playlist","play","item_id:" + str(channel)]]}, timeout=5)
        print("RESPONSE ", r)
    except:
        print('server error')

def sync():
    print('SYNC')
    try:
        r = requests.post(SERVER, json={"id":"1","method":"slim.request","params":["HomePod",["sync","JBL white"]]}, timeout=5)
        print("RESPONSE ", r)
    except:
        print('server error')

def unsync():
    print('UNSYNC')
    try:
        r = requests.post(SERVER, json={"id":"1","method":"slim.request","params":["JBL white",["sync","-"]]}, timeout=5)
        print("RESPONSE ", r)
    except:
        print('server error')

def send(ACTION):
    print('SEND ACTION: ', ACTION)
    print('try send: ', ACTIONS[str(ACTION)])
    try:
        r = requests.post(SERVER, json={"method": "slim.request", "params":[ PLAYER ,  ACTIONS[str(ACTION)]]}, timeout=5)
        print("RESPONSE ", r)
    except:
        print('server error')

def getkey():
    print('getkey started')
    remote = InputDevice(BTDEV)
    print(remote)    
    for event in remote.read_loop():
        if event.type == ecodes.EV_KEY:
            if event.value == 1:   
                print('key pressed ', event.code)     
                print(categorize(event))
                if str(event.code) == VOLDN:
                    voldn()
                if str(event.code) == VOLUP:
                    volup()
                if str(event.code) == PREV:
                    unsync()
                    prev()
                if str(event.code) == NEXT:
                    unsync()
                    next()
                if str(event.code) == PAUSE:
                    unsync()
                    pause()
                if str(event.code) == SYNC:
                    sync()
                if str(event.code) == HOME:
                    unsync()
                    first()
          
def main():
    while True:
        print('try bt device: ', BTDEV)
        try:
            remote = InputDevice(BTDEV)
            print('bt device ok: ', remote)
            print('start get key')
            getkey()
        except OSError as err:
            print("OS error: {0}".format(err))
            print('no bt device')
        time.sleep(5)

main()
