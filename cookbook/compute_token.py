import tiktoken
import openai
import warnings
import json
from tqdm import tqdm
from langchain_community.llms import OpenAI
from transformers import BertTokenizer

warnings.filterwarnings("ignore")
openai.api_base = "https://api.theb.ai/v1"
# openai.api_base = "https://api.baizhi.ai/v1"
openai.api_key = "sk-XsgkR7jwUtRV5yBxahebVGhlQi5BSQThqx4N8awhpPlYFUY3"
tokenizer = BertTokenizer.from_pretrained("/Users/zyl/Desktop/LLM/pretrain_models/bert-base-multilingual-cased")

def function_tokenizer(text_input):
	encode_input = tokenizer.encode(text_input, add_special_tokens=True)
	# decoded_text = tokenizer.decode(encode_input)
	num_tokens = len(encode_input)
	print("5. bert(作为对比)： token:", num_tokens)
	# print("bert tokenizer:", decoded_text)

def num_tokens_from_string(string, encoding_name):
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    # print("string nums is :", len(string))
    print("3. GPT4 token:", num_tokens)
    return num_tokens

def total_counts(tokens_nums):    
    #计算本次任务花了多少钱和多少tokens：
    price = 0.01/1000                                   #根据openai的美元报价算出的token美元单价
    cost = '{:.5f}'.format(price * tokens_nums * 7.19)   # 
    cost_ =  '{:.5f}'.format(price * tokens_nums)
    all_cost = f'4. GPT4： 花费{cost_}($)，折合人民币{cost}(¥)，'
    print(all_cost)
    # return float(cost)

def gpt_request(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=messages,
        stream=False,
        model_params={
            "temperature": 0.7
        }
    )
    response_json = response.choices[0].message
    result_str = json.dumps(response_json, ensure_ascii=False)
    result_json = json.loads(result_str)
    return result_json['content']

def main_test_zh(text):
	print('*'*50)
	# print("1. 输入文本为:", "\n", text, end="\n")
	print("2. 文本字符串数量为:", len(text))
	num_tokens = num_tokens_from_string(text, "cl100k_base")
	total_counts(num_tokens)
	function_tokenizer(text)
	print("\n")

def main_test_en(text):
	print('*'*50)
	print("1. 输入文本为:", "\n", text, end="\n")
	print("2. 文本字符串数量为:", len(text.split(' ')))
	num_tokens = num_tokens_from_string(text, "cl100k_base")
	total_counts(num_tokens)
	function_tokenizer(text)
	print("\n")

if __name__ == "__main__":

	# save_path = "/Users/zyl/Desktop/告警标签库2/测试GPT4极限/GPT4生成标签4.txt"
	# prompt_path = "/Users/zyl/Desktop/告警标签库2/测试GPT4极限/提示词.txt"
	# alarm_path = "/Users/zyl/Desktop/告警标签库2/测试GPT4极限/宁波银行告警content.txt"
	# alarm_text_path = "/Users/zyl/Desktop/告警标签库2/gpt4_content_text.txt"
	# gpt4_test_path = "/Users/zyl/Desktop/告警标签库2/测试GPT4极限/GPT4极限测试.txt"
	# with open(prompt_path, 'r') as f:
	# 	prompt = f.read()
	# with open(alarm_text_path, 'r',encoding="utf-8") as file:
	#     content = file.read()
	# text = '\n'.join([prompt, content])

	text = "我是一个语言模型，无法获取实时天气信息。建议您查看当地天气预报或相关天气应用程序获取最新天气信息。"
	# text2 = "Learning English is good for Chinese"
	main_test_zh(text)
	# main_test_en(text2)
	
	# 构建messages
	# dict1 = {"role": "system"}
	# dict2 = {"role": "user"}
	# dict1["content"] = prompt 
	# dict2["content"] = content
	# messages = [dict1, dict2]
	# fout = open(save_path, "w")
	# result = gpt_request(messages)
	# fout.write(result)
	# fout.flush()
	# fout.close()