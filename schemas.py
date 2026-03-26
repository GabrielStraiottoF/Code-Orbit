from pydantic import BaseModel, Field, field_validator
import re

# Este esquema define o que o usuário precisa enviar para se cadastrar
class UserCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    cpf: str
    cep: str
    telefone: str
    password: str = Field(..., min_length=6)

    @field_validator('cpf')
    @classmethod
    def validar_e_limpar_cpf(cls, v: str) -> str:
        # 1. Limpeza: remove pontos e traços (ex: 123.456.789-10 -> 12345678910)
        cpf = ''.join(filter(str.isdigit, v))

        # 2. Sua Lógica de Validação
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            raise ValueError('CPF inválido: deve ter 11 dígitos e não ser sequência repetida')

        # Cálculo do 1º dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digito1 = (soma * 10) % 11
        if digito1 == 10: digito1 = 0

        # Cálculo do 2º dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digito2 = (soma * 10) % 11
        if digito2 == 10: digito2 = 0

        if cpf[-2:] != f"{digito1}{digito2}":
            raise ValueError('CPF inválido: dígitos verificadores não conferem')

        return cpf  # Retorna o CPF limpo para o banco

    @field_validator('cep')
    @classmethod
    def validar_cep(cls, v: str) -> str:
        cep = ''.join(filter(str.isdigit, v))
        if len(cep) != 8:
            raise ValueError('CEP deve conter 8 números')
        return cep

# Este esquema define o que o servidor devolve para o usuário (omitimos a senha por segurança)
class UserResponse(BaseModel):
    id: int
    nome: str
    cpf: str

    class Config:
        from_attributes = True