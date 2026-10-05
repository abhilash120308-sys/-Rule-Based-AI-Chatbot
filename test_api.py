import urllib.request
import json

base = 'http://127.0.0.1:5000'

# 1. Test Index
req = urllib.request.urlopen(base + '/')
print(f'GET / -> Status: {req.status}')

# 2. Test /api/chat with 'HELLO'
chat_data = json.dumps({'message': '  HELLO  '}).encode('utf-8')
req2 = urllib.request.Request(base + '/api/chat', data=chat_data, headers={'Content-Type': 'application/json'})
res2 = json.loads(urllib.request.urlopen(req2).read().decode('utf-8'))
print('POST /api/chat (HELLO):', res2)

# 3. Test /api/chat with 'xyzabc' (Fallback)
chat_fallback = json.dumps({'message': 'xyzabc'}).encode('utf-8')
req3 = urllib.request.Request(base + '/api/chat', data=chat_fallback, headers={'Content-Type': 'application/json'})
res3 = json.loads(urllib.request.urlopen(req3).read().decode('utf-8'))
print('POST /api/chat (xyzabc):', res3)

# 4. Test /api/chat with 'bye' (Exit)
chat_exit = json.dumps({'message': 'bye'}).encode('utf-8')
req4 = urllib.request.Request(base + '/api/chat', data=chat_exit, headers={'Content-Type': 'application/json'})
res4 = json.loads(urllib.request.urlopen(req4).read().decode('utf-8'))
print('POST /api/chat (bye):', res4)

# 5. Test /api/intents
req5 = urllib.request.urlopen(base + '/api/intents')
res5 = json.loads(req5.read().decode('utf-8'))
print(f"GET /api/intents -> Total Intents: {res5['total_intents']}")
