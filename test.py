import requests
import json

# Define the endpoint and headers
endpoint = ""
headers = {
    "Content-Type": "application/json",
    # "api-key": "",  # Your actual API key
    "api-version": "2021-04-30-Preview"
}

# Define the index schema
index_definition = {
    "name": "documents",
    "fields": [
        {"name": "id", "type": "Edm.String", "key": True, "retrievable": True},
        {"name": "content", "type": "Edm.String", "retrievable": True},
        {"name": "sourcepage", "type": "Edm.String", "retrievable": True},
        # Add more fields as needed
    ]
}

# Create the index
response = requests.post(f"{endpoint}/indexes?api-version=2021-04-30-Preview", headers=headers, data=json.dumps(index_definition))

# Check the response status
if response.status_code == 201:
    print("Index created successfully.")
else:
    print(f"Failed to create index: {response.status_code} - {response.text}")
