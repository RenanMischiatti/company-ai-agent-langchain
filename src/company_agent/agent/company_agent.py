from langchain_core.language_models.chat_models import BaseChatModel


class CompanyAgent:
    def __init__(self, model: BaseChatModel) -> None:
        self._model = model

    def answer(self, question: str) -> str:
        normalized_question = question.strip()

        if not normalized_question:
            raise ValueError("A pergunta nao pode estar vazia.")

        response = self._model.invoke(normalized_question)

        return str(response.content)
