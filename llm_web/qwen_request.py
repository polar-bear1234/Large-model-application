# import openai
# import os
# from openai import OpenAI
# # http://61.241.103.69:9095/v1
# # http://61.241.103.69:9095/v1/chat/completions
# openai.api_base = "http://61.241.103.69:9095/v1/chat/completions"
# openai.api_key = "xxx"

# completion = openai.ChatCompletion.create(
# 	model="qwen-7b-chat", 
# 	messages=[
# 		{
# 			"role": "user", 
# 			"content": "你好"
# 		}
# 	],
# 	stream=False,
# )
# print(completion.choices[0].message.content)
# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
import requests
import json

api_url = "http://61.241.103.69:9095/v1/chat/completions"

def qwen_request(url):
	data = {
	    "model": "qwen-7b-chat",
	    "messages": [{"role": "user","content": "今天天气怎么样？"}],
	    "stream": False
	}
	# headers: 身份验证 & 服务器请求主体的数据格式
	headers = {
	    "Authorization": "Bearer xxx",
	    "Content-Type": "application/json"
	}
	response = requests.post(url, json=data, headers=headers)  #
	return response.json()


if __name__ == "__main__":

	result = qwen_request(url=api_url)
	print("AI:", result['choices'][0]['message']['content'])
# -----------------------------------------------------------------------------------------

"""
curl http://61.241.103.69:9095/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
     "model": "qwen-7b-chat",
     "messages": [{"role": "user", "content": "今天天气怎么样？"}],
     "temperature": 0.5
   }'
"""
