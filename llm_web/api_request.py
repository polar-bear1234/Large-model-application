import requests
from pprint import pprint
import json


def llm_request_api(url, input_text, history):
	data = {
			"prompt": input_text,
			"history": history,
			"max_length": 4096, 
			"top_p": 0.8, 
			"temperature": 0.6
		}
	
	response = requests.post(url, json=data)
	return response.json()


if __name__ == "__main__":

	URL = "http://127.0.0.1:9898"
	# URL = "http://61.241.103.69:9095"
	while True:
		input_text = input("User:")
		history = []
		result = llm_request_api(URL, input_text, history)
		print("AI:", result['response'])

"""
curl -X POST "http://127.0.0.1:8000" \
     -H 'Content-Type: application/json' \
     -d '{"prompt": "你好", "history": []}'
"""
