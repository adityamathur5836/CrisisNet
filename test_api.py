import requests
import json

base_url = "http://localhost:5001"
print("Testing /state")
st = requests.get(f"{base_url}/state").json()
print("state OK", st.get('time'))

print("Testing /step")
step = requests.post(f"{base_url}/step", json={"agent": "RLAgent"}).json()
print("step OK", step.get('state', {}).get('time'))

print("Testing /zone/1")
zone = requests.get(f"{base_url}/zone/1").json()
print("zone OK", zone.get('id'))

print("Testing /compare_agents")
comp = requests.get(f"{base_url}/compare_agents?seed=42").json()
print("compare OK", [c.get('agent') for c in comp])

