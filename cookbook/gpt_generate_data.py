import openai
import time

# openai.api_key = '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'
# openai.api_key = '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'
openai.api_key = "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"


def chatgpt_function(prompt):
    while True:
        try:
            completion = openai.Completion.create(
                    engine="text-davinci-003",   # GPT 模型ID，不同的模型会生成不同的结果
                    prompt=prompt,
                    max_tokens=1024,
                    n=1,
                    stop=None,
                    temperature=0.5,    # 0～1，控制模型生成文本的创新程度
                    timeout=50000
                )
            answer = completion.choices[0].text
            if answer:
                break
        except Exception as ex:
            print(ex)
    return answer


def chatgpt_multi(conversation_list):
    # GPT-3.5-turbo 模型是以一系列消息作为输入，并将模型生成的消息作为输出。
    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=conversation_list)
            break  # Exit the loop if the API call succeeds
        except (openai.error.RateLimitError, openai.error.APIError,
                openai.error.ServiceUnavailableError) as e:
            time.sleep(3)
    answer = response.choices[0].message['content']
    return answer


if __name__ == "__main__":

    # function1:
    # --------------------------------
    text = "基于bert的预训练模型简介。"
    Q = chatgpt_function(text)
    print(Q)

    # function2:
    # --------------------------------
    # task_description = "在智能运维领域，日志数据中包含着大量实体，接下来请使用 BMES 方法对日志文本中的实体进行序列标注。"
    # prompt1 = "请使用 BMES 方法进行序列标注，示例'中   B'：" \
    #           "虚拟机IP地址为：10.0.177.126 指标: [APP_PORT] 8940 port status 在时间" \
    #           " 2023-02-08 21:49:21 发生了异常,指标值变化了:-1.0，中间件tomcat发生异常，MySQL数据库异常，网络延迟超过5000ms。"
    # pre_answers = {0: "", 1: ""}
    # prompt2 = "把如该序列标注的内容转化成与label-studio输出json相同的格式"
    # prompt3 = "请输出您优化后的答案"
    # conversation_list = [# {"role": "system", "content": "你是一个经验丰富的擅长故障根因定位的系统运维专家。"},
    #                      {"role": "user", "content": task_description},       # 任务描述
    #                      {"role": "user", "content": prompt1},                # 提问
    #                      {"role": "assistant", "content": pre_answers[0]},    # 存储先前回复
    #                      {"role": "user", "content": prompt2},                # 继续发问
    #                      {"role": "assistant", "content": pre_answers[1]},    # 存储
    #                      # {"role": "user", "content": prompt3}
    #                      ]                # 继续发问
    # """
    #     系统 消息有助于设置助手的行为。在上面的例子中，助手被指示 “你是一个得力的助手”。
    #     用户 消息有助于指导助手。 就是用户说的话，向助手提的问题。
    #     助手 消息有助于存储先前的回复。这是为了持续对话，提供会话的上下文。
    # """
    # Q = chatgpt_multi(conversation_list)
    # print("pre_answers[0]--------------", "\n", pre_answers[0])
    # print("pre_answers[1]--------------", "\n", pre_answers[1])
    # print("最后回答-----------------------", "\n", Q)