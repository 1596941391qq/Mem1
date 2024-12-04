'''
Author: nzgw
Date: 2024-12-04 18:30:48
LastEditors: nzgw
LastEditTime: 2024-12-04 18:39:09
FilePath: \mem0\embeddings\openai.py
Description: 

Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
'''
import os
from typing import Optional

from openai import OpenAI

from mem0.configs.embeddings.base import BaseEmbedderConfig
from mem0.embeddings.base import EmbeddingBase


class OpenAIEmbedding(EmbeddingBase):
    def __init__(self, config: Optional[BaseEmbedderConfig] = None):
        super().__init__(config)

        self.config.model = self.config.model or "text-embedding-3-small"
        self.config.embedding_dims = self.config.embedding_dims or 1536

        api_key = self.config.api_key or os.getenv("OPENAI_API_KEY")
        base_url = self.config.openai_base_url or os.getenv("OPENAI_API_BASE")
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def embed(self, text):
        """
        Get the embedding for the given text using OpenAI.

        Args:
            text (str): The text to embed.

        Returns:
            list: The embedding vector.
        """
        text = text.replace("\n", " ")
        return (
            self.client.embeddings.create(input=[text], model=self.config.model, dimensions=self.config.embedding_dims)
            .data[0]
            .embedding
        )