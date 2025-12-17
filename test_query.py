import requests

print("Testing Query...")
try:
    response = requests.post("http://localhost:8000/query", json={"question": "What is this knowledge base about?"})
    if response.status_code == 200:
        print("Success!")
        print(response.json())
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Connection Failed: {e}")
