# chatgpt多轮对话
import openai
import easygui as g

openai.api_key = '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'

class Chat:
    def __init__(self,conversation_list=[]) -> None:
        # 初始化对话列表，可以加入一个key为system的字典，有助于形成更加个性化的回答
        # self.conversation_list = [{'role':'system','content':'你是一个非常友善的助手'}]
        self.conversation_list = []  # 初始化对话列表
        self.costs_list = [] # 初始化聊天开销列表
            
    def show_conversation(self,msg_list):
        for msg in msg_list[-2:]:
            if msg['role'] == 'user': # 如果是用户的话
                #print(f"\U0001f47b: {msg['content']}\n")
                pass
            else: # 如果是机器人的话
                message = msg['content']
                print(f"\U0001f47D: {message}\n")                
            print()

    def ask(self,prompt):
        self.conversation_list.append({"role":"user","content":prompt})

        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=self.conversation_list)
        answer = response.choices[0].message['content']
        self.conversation_list.append({"role":"assistant","content":answer})


        self.show_conversation(self.conversation_list)    # 打印对话
        人民币花费 = total_counts(response)                 # 计算消耗人民币
        self.costs_list.append(人民币花费)
        print("conversation_list:----------------------------------")
        print(self.conversation_list)

def total_counts(response):    
    
    #计算本次任务花了多少钱和多少tokens：
    tokens_nums = int(response['usage']['total_tokens']) #计算一下token的消耗
    price = 0.002/1000                                   #根据openai的美元报价算出的token美元单价
    cost = '{:.5f}'.format(price * tokens_nums * 7.5)   #  
    all_cost = f'本次对话共消耗了{tokens_nums}个token，花了{cost}元（¥）'
    print(all_cost)
    return float(cost)


def main(count_limit):
    talk = Chat()
    count = 0 	
    while count < count_limit: #上下文token数量是有极限的，理论上只能支持有限轮次的对话，况且，钱花光了也就不能用了。。。
        if count < 1: 
            words = input("请问有什么可以帮助你的呢？\n(请输入您的需求或问题)：")
        else:
            words = input("您还可以继续与我交流，请您继续说：\n(请输入您的需求或问题)：")
        print()
        talk.ask(words)
        count += 1
    
    g.msgbox("对不起，您已达到使用次数的限额，欢迎您下次使用！")      
    print(f'本轮聊天合计花费{sum(talk.costs_list)}元人民币。')



if __name__ == "__main__":
    
    count_limit = 6
    main(count_limit)
