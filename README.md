# MEM1

 ## 概述

Mem0(发音为“mem-zero”)通过智能记忆层增强AI助手和Agent的个性化的人工智能交互。Mem0会记住用户的偏好和特点，并随着时间的推移不断更新，使其非常适合于客户支持聊天机器人和人工智能助手等应用。

本质是一个通过AI处理对话并提炼成记忆，存入向量或图知识库的项目

mem1是魔改版本。目前我的魔改能让它生成效果更可用和更适合做情感陪伴项目。情感陪伴需要多用户的长期记忆解决方案。将使用pip安装在venv依赖中的MEM0源文件替换即可（不用手动安装依赖）

原项目地址：https://github.com/mem0ai/mem0

使用文档：https://docs.mem0.ai/overview

### 我的魔改进度

1. 可以接入国内大模型和embedding模型，并可以在config中设置向量维度
2. 我把记忆分为时序信息和恒常信息，
   时序信息例子#ai:我今天去滑雪了——10月18号ai去滑雪 
   恒常信息例子#ai：我喜欢滑雪——ai喜欢滑雪 
   然后在获取所有记忆里会将这两种信息进行区分。
3. 支持把多条对话记录（建议为十条）一次性让AI提炼记忆
4. AI不仅能从对话记录中提炼用户的信息作为记忆，也会提炼自己的信息（在情感陪伴上，AI角色应该能记住自己所说过的话）
5. 针对国内大模型的输出方式做了json后处理，否则无法正常运行
6. 翻译了mem0所有的提示词，可以自定义修改

### 使用指南

```python
config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": "deepseek-ai/DeepSeek-V2.5",
            "temperature":0.0,
            "max_tokens": 1500,
            "openai_base_url":"https://api.siliconflow.cn/v1/",
            "api_key":""

        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "embedding_model_dims" : 1024,
            "collection_name": "test",
            "url":"http://101.35.160.32:6333/dashboard",
            "api_key": "123456",

        },

    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "BAAI/bge-m3",
            "embedding_dims": 1024

        }
    },
    "version": "v1.1"
}

```

​			

- 使用国内的大模型和embedding模型，embedding模型需要将模型名和embedding_dims更改，否则会对应不上.可以参考我的配置

+ 国内大模型生成结果是md格式，即生成的json会有'''json '''包裹，我已经用正则去做后处理
+ 使用qdrant的话，需要先生成一个表，然后在config把表名的配置上
+ 使用图数据库需要在MemoryGraph的add做json后处理，并在openAILLM类的_parse_response通过except json.JSONDecodeError:捕获json问题之后修改。这一步是避免大模型回复因为长度问题截断。前面这些我都完成了。为了进一步完善这个问题可以给llm设置"max_tokens":
+ 由于mem0是prompt驱动的，LLM配置最好将温度调为0.0降低多样性，防止作妖
+ 如果对响应速度有要求，可以
  1. 用更快的大模型和embedding模型，线上embedding模型速度大概在两秒以内，建议本地部署embedding或者用siliconflow的高速模型。
  2. 放弃用自然语言查询，提前用get_all生成记忆文本，可以是日记格式然后放入ai上下文（我目前是这么做的）
+ 总结：用siliconflow里的bge作为embedding模型，对记忆的增删改查会比较快。其次可以把它理解成一个多租户的rag系统，通过user_id和agent_id处理个性化内容