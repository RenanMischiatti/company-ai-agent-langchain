from collections.abc import Sequence

from langchain.agents import create_agent
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool


class CompanyAgent:
    def __init__(
        self,
        model: BaseChatModel,
        tools: Sequence[BaseTool],
        system_prompt: str,
    ) -> None:
        self._agent = create_agent(
            model=model,
            tools=tools,
            system_prompt=system_prompt,
        )

    def answer(self, question: str) -> str:
        normalized_question = question.strip()

        if not normalized_question:
            raise ValueError("A pergunta nao pode estar vazia.")

        result = self._agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": normalized_question,
                    }
                ]
            }
        )
        final_message = result["messages"][-1]

        return str(final_message.content)
