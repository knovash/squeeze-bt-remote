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

SERVER = settings['server']
PLAYER = settings['player']
BTDEV = settings['btdevice']

print('SERVER ', SERVER)
print('PLAYER ', PLAYER)
print('BTDEV ', BTDEV)

ACTIONS = {
"115":["mixer", "volume", "+5" ], 
"114":["mixer", "volume", "-5" ],
"164":["pause"],
"163":["playlist","index","+1"], 
"165":["playlist","index","-1"] 
}
print('ACTIONS')
for key,value in ACTIONS.items(): 
    print(key, ':', value)

def send(ACTION):
    print('try send: ', ACTION)
    try:
        r = requests.post(SERVER, json={
        "method": "slim.request", 
        "params":[ PLAYER ,  ACTIONS[str(ACTION)]]
        }, timeout=5)
    except:
        print('no server')

def getkey():
    print('getkey started')
    remote = InputDevice(BTDEV)
    print(remote)    
    for event in remote.read_loop():
        if event.type == ecodes.EV_KEY:
            if event.value == 1:   
                print('key pressed ', event.code)     
                print(categorize(event))
                print('action: ', ACTIONS[str(event.code)])
                send(event.code)
          
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
