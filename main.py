from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

import models, schemas, database

# 1. Configuração de Segurança (Criptografia)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Cria as tabelas no banco de dados automaticamente ao iniciar
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Sistema de Login Profissional")

# 3. Dependência para abrir/fechar o banco de dados
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROTAS ---

@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verifica se o CPF já existe no banco
    db_user = db.query(models.User).filter(models.User.cpf == user.cpf).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Este CPF já está cadastrado.")
    
    # Criptografa a senha antes de salvar
    hashed_password = pwd_context.hash(user.password)
    
    # Cria a instância do modelo
    novo_usuario = models.User(
        nome=user.nome,
        cpf=user.cpf,
        cep=user.cep,
        telefone=user.telefone,
        hashed_password=hashed_password
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@app.post("/login")
def login(cpf: str, password: str, db: Session = Depends(get_db)):
    # Busca o usuário pelo CPF
    user = db.query(models.User).filter(models.User.cpf == cpf).first()
    
    # Verifica se usuário existe e se a senha "bate" com o hash
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="CPF ou senha incorretos"
        )
    
    return {"message": "Login realizado com sucesso!", "usuario": user.nome}