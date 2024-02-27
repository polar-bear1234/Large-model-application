import openai
import streamlit as st
import json
import pandas as pd

openai.api_base = "https://api.theb.ai/v1"
# openai.api_base = "https://api.baizhi.ai/v1"
openai.api_key = "sk-XsgkR7jwUtRV5yBxahebVGhlQi5BSQThqx4N8awhpPlYFUY3"

if 'OUTPUT_JSON' not in st.session_state:
    st.session_state['OUTPUT_JSON'] = {}
OUTPUT_JSON = st.session_state['OUTPUT_JSON']

def gpt_request(select_model, messages):
    response = openai.ChatCompletion.create(
        model=select_model,
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

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as config_json:
        config_data = json.load(config_json)
        labels = tuple(config_data.keys())
    return labels

labels = load_config('./config40.json')
def get_prompt(input_alarm):
    # Prompt:
    prompt1 = """
    告警标签是对告警数据的归纳总结和分类,我将输入样例，按照告警数据的序号返回标签，请学习这种为告警打标签的模式：
    1 531企业网银系统（境内）2019-11-01 13~13服务进程:182.251.48.53_CEBSSvr02,1小时交易量低持续52次,当前值0阈值1   
    2 19:38”19:39 业务返回码:PB521099(付款行填写的其他快捷支付失败说明)，1分钟交易量高，闻值:100笔，实际值:421笔  
    3 DTTDCGF NUCPNETepcc101001.0111 busTransCount 300秒内无数据推送]          
    以上三条样例的标签为：应用系统业务告警：[2023-04-23T18:51:00.000+08:00]财资管理系统_财资web（江北）的响应时间发生突增异常，当前值为:6.869377,高于动态基线值:1.884699,同时对应交易量和响应率发生突变异常，请注意! 
    1. 交易量持续低
    2. 交易量突增
    3. 交易量无推送
    请学习这种为告警打标签的方法，为后续告警打上正确的标签，要求只输出告警序号和标签，如（1. 交易量持续低），无需输出告警数据：
    """
    # input_alarm = input("请输入告警数据:")
    prompt2 = """
    请为下列告警打上正确的标签,告警数据: {};
    要求:1.输出格式为：告警标签(比如：交易量持续低)；2.仅输出告警数据和标签，不要输出其他任何内容。
    """.format(input_alarm)
    prompt3 = """3.标签范围包含在{}中:""".format(labels)
    return prompt1, prompt2, prompt3

def gpt_demo(select_model, prompt_nums, input_alarm):
    prompt1, prompt2, prompt3 = get_prompt(input_alarm)
    st.caption("Prompt 示例:")
    st.text(prompt2)
    input_text2 = st.text_area("修改部分 Prompt:")
    if input_text2 and st.button("**Running...**"):
        messages = [
                {"role": "system", "content": "您是一位智能运维专家，告警数据有着深刻的理解，能够通过告警标签生成不同类型的告警数据，下面请解决运维领域告警数据相关的问题:"},
                {"role": "user", "content": prompt1},
                {'role': "user", "content": input_text2},
                {'role': "user", "content": prompt3}
            ]
    else:
        messages = [
                {"role": "system", "content": "您是一位智能运维专家，告警数据有着深刻的理解，能够通过告警标签生成不同类型的告警数据，下面请解决运维领域告警数据相关的问题:"},
                {"role": "user", "content": prompt1},
                {'role': "user", "content": prompt2},
                {'role': "user", "content": prompt3}
            ]
    result = gpt_request(select_model, messages[:prompt_nums])
    return result

def convert_df(df):
    return df.to_csv(index=False, encoding='utf-8')

def llm_main():
    st.sidebar.title("**「GPT4-Turbo」**")
    with st.sidebar.expander("LLM选项", expanded=True):
        st.write(
            """
            - GPT4-Turbo
            - GPT3.5-Turbo
            - ChatGLM3-6B
            - LlaMA-2-7B
            - Qwen-7B
            """)
    # 上传告警文件（可编辑）   
    # st.markdown("<h3 style='text-align: left;'>1. 告警打标签</h1>", unsafe_allow_html=True)
    # uploaded_file = st.file_uploader("upload", type=['csv'])
    # if 'load_csv' not in st.session_state:
    #     st.session_state["load_csv"] = pd.DataFrame()
    # if 'data_editor' not in st.session_state:
    #     st.session_state["data_editor"] = pd.DataFrame()
    # if 'output_csv' not in st.session_state:
    #     st.session_state["output_csv"] = pd.DataFrame()
    # if uploaded_file:
    #     st.session_state['load_csv'] = pd.read_csv(uploaded_file)
    # df = pd.DataFrame()
    # df = st.session_state['load_csv']
    # for col in ["content", "label", "bert_model", "prob", "人工修改"]:
    #     if col not in df.columns:
    #         df.insert(loc=0, column=col, value=False)
    # st.session_state['data_editor'] = st.data_editor(
    #     st.session_state['load_csv'], hide_index=None, num_rows="dynamic", 
    #     column_order=("content", "label", "bert_model", "prob", "人工修改")
    # ) 
    # # 保存文件
    # csv = convert_df(st.session_state['data_editor'])
    # st.download_button(
    #     label="⬇️  Download data as CSV", 
    #     data=csv, 
    #     file_name='output.csv',
    #     mime='text/csv')

    with st.sidebar.expander("**标签类别**", expanded=True):
        st.write(list(labels))
    st.markdown("<h3 style='text-align: left;'>告警数据打标签 - LLM</h1>", unsafe_allow_html=True)
    
    with st.expander("GPT4-Turbo", expanded=True):
        text_ = st.text_area("告警数据1")
        contain = st.checkbox("是否在标签空间里选择标签(是/否)")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            button_clicked1 = st.button("GPT4-Turbo")
        with col2:
            button_clicked2 = st.button("GPT3.5-Turbo")
        with col3:
            button_clicked3 = st.button("LlaMA2-7B")
        with col4:
            button_clicked4 = st.button("Qwen-7B")
        if button_clicked1:
            select_model = "gpt-4-turbo"
            if contain:
                result = gpt_demo(select_model=select_model, input_alarm=text_, prompt_nums=4)
                # st.write("GPT4-Turbo (包含标签空间): ", result)
                OUTPUT_JSON["GPT4-Turbo (包含标签空间)"] = result
            else:
                result = gpt_demo(select_model=select_model, input_alarm=text_, prompt_nums=3)
                # st.write("GPT4-Turbo (不包含标签空间): ", result)
                OUTPUT_JSON["GPT4-Turbo (不包含标签空间)"] = result
        if button_clicked2:
            select_model = "gpt-3.5-turbo"
            if contain:
                result = gpt_demo(select_model=select_model, input_alarm=text_, prompt_nums=4)
                # st.write("GPT3.5-Turbo (包含标签空间): ", result)
                OUTPUT_JSON["GPT3.5-Turbo (包含标签空间)"] = result
            else:
                result = gpt_demo(select_model=select_model, input_alarm=text_, prompt_nums=3)
                st.write("GPT3.5-Turbo (不包含标签空间): ", result)
                OUTPUT_JSON["GPT3.5-Turbo (不包含标签空间)"] = result
        if button_clicked3:
            select_model = "llama-2-7b-chat"
            if contain:
                result = gpt_demo(select_model=select_model, input_alarm=text_, prompt_nums=4)
                # st.write("LlaMA-2-7B (包含标签空间): ", result)
                OUTPUT_JSON["LlaMA2-7B (包含标签空间)"] = result
            else:
                result = gpt_demo(select_model=select_model, input_alarm=text_, prompt_nums=3)
                # st.write("LlaMA-2-7B (不包含标签空间): ", result)
                OUTPUT_JSON["LlaMA-2-7B (不包含标签空间)"] = result
        if button_clicked4:
            select_model = "qwen-7b-chat"
            if contain:
                result = gpt_demo(select_model=select_model, input_alarm=text_, prompt_nums=4)
                # st.write("Qwen-7B (包含标签空间): ", result)
                OUTPUT_JSON["Qwen-7B (包含标签空间)"] = result
            else:
                result = gpt_demo(select_model=select_model, input_alarm=text_, prompt_nums=3)
                # st.write("Qwen-7B (不包含标签空间): ", result)
                OUTPUT_JSON["Qwen-7B (不包含标签空间)"] = result
    st.write(OUTPUT_JSON)

if __name__ == "__main__":

    llm_main()