import json
from sqlalchemy import create_engine, Column, String, Float, DateTime, ForeignKey, text
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv(".env.development")

URL_DB = os.environ["URL_DB"]

# Definir la base de datos
engine = create_engine(URL_DB)
Base = declarative_base()

class User(Base):
    __tablename__ = 'clients'

    id = Column(String, primary_key=True)
    name = Column(String(50), unique=False, nullable=False)
    email = Column(String(20), unique=True, nullable=False)
    role = Column(String(10), unique=False, nullable=False)
    policies = relationship("Policies", back_populates="client")

class Policies(Base):
    __tablename__ = 'policies'

    id = Column(String, primary_key=True)
    amountInsured = Column(Float, unique=False, nullable=False)
    email = Column(String(20), unique=False, nullable=False)
    inceptionDate = Column(DateTime, unique=False, nullable=False)
    installmentPayment = Column(String(20), unique=False, nullable=False)
    clientId = Column(String, ForeignKey('clients.id'), nullable=False)
    client = relationship("User", back_populates="policies")

# Crear las tablas
Base.metadata.create_all(engine)



########################


# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

# Cargar datos desde los archivos JSON
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

clients_data = load_data('data/clients.json')
policies_data = load_data('data/policies.json')

# Insertar datos en la tabla User
for client in clients_data:
    new_user = User(
        id=client['id'],
        name=client['name'],
        email=client['email'],
        role=client['role']
    )
    session.add(new_user)

# Insertar datos en la tabla Policies
for policy in policies_data:
    new_policy = Policies(
        id=policy['id'],
        amountInsured=policy['amountInsured'],
        email=policy['email'],
        inceptionDate=datetime.strptime(policy['inceptionDate'], '%Y-%m-%dT%H:%M:%SZ'),
        installmentPayment=policy['installmentPayment'],
        clientId=policy['clientId']
    )
    session.add(new_policy)

# Confirmar la transacción
session.commit()

# Cerrar la sesión
session.close()