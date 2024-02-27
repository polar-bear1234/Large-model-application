# -*- coding:utf-8 -*-
# @project: ChatGPT
# @filename: model
# @time: 2023/8/6 16:13
"""
    文件说明：
            
"""
from glm3.modeling_chatglm import ChatGLMForConditionalGeneration as ChatGLM3ForConditionalGeneration
from glm3.tokenization_chatglm import ChatGLMTokenizer as ChatGLM3Tokenizer
from glm3.configuration_chatglm import ChatGLMConfig as ChatGLM3Config
from utils import GLMPromptDataSet, GLM2PromptDataSet, GLM3PromptDataSet

MODE = {
        "glm3": {"model": ChatGLM3ForConditionalGeneration, "tokenizer": ChatGLM3Tokenizer, "config": ChatGLM3Config,
                 "dataset": GLM3PromptDataSet}
        }
