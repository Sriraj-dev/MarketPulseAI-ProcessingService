
from .llm_interfacer import LLM_Interfacer
from .openai_impl import OpenAI_Impl

llm_impl = OpenAI_Impl() ## We can change to other implementations if required from here.

# Define the public API
__all__ = ["LLM_Interfacer", "llm_impl"]
