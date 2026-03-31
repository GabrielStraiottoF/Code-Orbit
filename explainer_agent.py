from models.schemas import Profile, Recommendation, SafetyResult
from services.llm_service import FoundryAgentService
from config import FOUNDRY_EXPLAINER_AGENT_NAME


class ExplainerAgent:
    def __init__(self) -> None:
        self.service = FoundryAgentService()

    def process(
        self,
        user_message: str,
        profile: Profile,
        recommendation: Recommendation,
        safety: SafetyResult,
    ) -> str:
        prompt = f"""
Gere a resposta final ao usuário.

Mensagem original:
{user_message}

Perfil:
{profile}

Recomendação:
{recommendation}

Validação de segurança:
{safety}

Regras:
- escreva em português
- seja amigável
- explique o motivo da recomendação
- se houver observação relevante de classificação indicativa, inclua isso de forma natural
- não responda em JSON
""".strip()

        response_text = self.service.ask_agent(
            agent_name=FOUNDRY_EXPLAINER_AGENT_NAME,
            content=prompt,
        )

        if response_text.strip():
            return response_text.strip()

        filme = recommendation["recomendacoes"][0]
        return (
            f"Uma ótima opção é {filme['titulo']}. "
            f"{filme['motivo']} "
            f"A classificação indicativa é {filme['classificacao_indicativa']}."
        )

    def close(self) -> None:
        self.service.close()