from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date
from pydantic import BaseModel

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/red_social2"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#------------ Usuario ----------------

class Usuario(Base):
    __table_args__ = {"schema": "seguridad"}
    __tablename__ = "usuario"
    cod_usu = Column(Integer, primary_key=True, index=True)
    ali_usu = Column(String, index=True)
    ema_usu = Column(String)
    cla_usu = Column(String)
    est_usu = Column(String)
    persona = relationship("Persona", back_populates="usuario")

class UsuarioCreate(BaseModel):
    ali_usu: str
    ema_usu: str
    cla_usu: str
    est_usu: str

class UsuarioResponse(UsuarioCreate):
    cod_usu: int

    class Config:
        from_attributes = True

# --------- Persona ---------

class Persona(Base):
    __tablename__ = "persona"
    __table_args__ = {"schema": "perfil_personal"}
    cod_per = Column(Integer, primary_key=True, index=True)
    nm1_per = Column(String, index=True)
    nm2_per = Column(String)
    ap1_per = Column(String)
    ap2_per = Column(String)
    nac_per = Column(Date)
    sex_per = Column(String)
    per_per = Column(String)
    por_per = Column(String)
    fky_usu = Column(Integer, ForeignKey("seguridad.usuario.cod_usu"), index=True)

    usuario = relationship("Usuario", back_populates="persona")
    rol_fan_page = relationship("Rol_Fan_Page", back_populates="persona")

class PersonaCreate(BaseModel):
    nm1_per: str
    nm2_per: str
    ap1_per: str
    ap2_per: str
    nac_per: date
    sex_per: str
    per_per: str
    por_per: str
    fky_usu: int

class PersonaResponse(PersonaCreate):
    cod_per: int
    usuario: UsuarioResponse

    class Config:
        from_attributes = True

#---------------- Fan Page --------------------

class Fan_Page(Base):
    __tablename__ = "fan_page"
    __table_args__ = {"schema": "perfil_empresarial"}
    cod_fan_pag = Column(Integer, primary_key=True, index=True)
    nom_fan_pag = Column(String, index=True)
    des_fan_pag = Column(String)
    per_fan_pag = Column(String)
    fec_fan_pag = Column(Date)
    est_fan_pag = Column(String)
    rol_fan_page = relationship("Rol_Fan_Page", back_populates="fan_page")

class Fan_PageCreate(BaseModel):
    nom_fan_pag: str
    des_fan_pag: str
    per_fan_pag: str
    fec_fan_pag: date
    est_fan_pag: str

class Fan_PageResponse(Fan_PageCreate):
    cod_fan_pag: int

    class Config:
        from_attributes = True

#---------- Rol -------------

class Rol(Base):
    __tablename__ = "rol"
    __table_args__ = {"schema": "seguridad"}
    cod_rol = Column(Integer, primary_key=True, index=True)
    nom_rol = Column(String, index=True)
    des_rol = Column(String)
    est_rol = Column(String)
    rol_fan_page = relationship("Rol_Fan_Page", back_populates="rol")

class RolCreate(BaseModel):
    nom_rol: str
    des_rol: str
    est_rol: str

class RolResponse(RolCreate):
    cod_rol: int

    class Config:
        from_attributes = True

# --------- Rol Fan Page ---------

class Rol_Fan_Page(Base):
    __tablename__ = "rol_fan_page"
    __table_args__ = {"schema": "seguridad"}
    cod_rol_fan = Column(Integer, primary_key=True, index=True)
    fky_per = Column(Integer, ForeignKey("perfil_personal.persona.cod_per"), index=True)
    fky_fan_pag = Column(Integer, ForeignKey("perfil_empresarial.fan_page.cod_fan_pag"), index=True)
    fky_rol = Column(Integer, ForeignKey("seguridad.rol.cod_rol"), index=True)
    est_rol_fan = Column(String)

    persona = relationship("Persona", back_populates="rol_fan_page")
    fan_page = relationship("Fan_Page", back_populates="rol_fan_page")
    rol = relationship("Rol", back_populates="rol_fan_page")

class Rol_Fan_PageCreate(BaseModel):
    fky_per: int
    fky_fan_pag: int
    fky_rol: int
    est_rol_fan: str

class Rol_Fan_PageResponse(Rol_Fan_PageCreate):
    cod_rol_fan: int
    persona: PersonaResponse
    fan_page: Fan_PageResponse
    rol: RolResponse

    class Config:
        from_attributes = True
