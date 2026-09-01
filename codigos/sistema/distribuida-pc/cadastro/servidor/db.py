from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine("sqlite+pysqlite:///client-server.db", echo=False, future=True)
Base = declarative_base()
Session = sessionmaker(bind=engine, expire_on_commit=False)
session = Session()


def createNewDB():
    choice = input("Esse procedimento resultará na PERDA de TODOS OS DADOS.\nTem certeza que deseja continuar? (s/N) ")
    if choice.lower() == "s":
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("Banco de dados recriado!")
    else:
        print("Procedimento abortado.")


def startDatabase():
    Base.metadata.create_all(bind=engine)


def addRegisters(registers):
    if len(registers) == 1:
        session.add(registers[0])
    else:
        session.add_all(registers)


def saveSession():
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
