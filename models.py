from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    # O ID é gerado automaticamente pelo banco
    id = Column(Integer, primary_key=True, index=True)
    
    nome = Column(String, nullable=False)
    
    # Marcamos o CPF como único para evitar cadastros duplicados
    cpf = Column(String, unique=True, index=True, nullable=False)
    
    cep = Column(String, nullable=False)
    
    telefone = Column(String, nullable=False)
    
    # Aqui guardaremos a senha criptografada (Hash), nunca a senha real
    hashed_password = Column(String, nullable=False)