from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload # Usamos joinedload para asegurar que la informacion del continente se cargue junto con el pais para evitar multiples consultas a la BD
from typing import List
from models import  Usuario, UsuarioCreate, UsuarioResponse, SessionLocal, Base, engine, Persona, PersonaCreate, PersonaResponse, Fan_Page, Fan_PageCreate, Fan_PageResponse, Rol, RolCreate, RolResponse, Rol_Fan_Page, Rol_Fan_PageCreate, Rol_Fan_PageResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/")
def read_root():
    return {"API": "rol_fan_page - fan_page - persona - rol - usuario"}

@app.post("/rol_fan_pages/", response_model=Rol_Fan_PageResponse)
def crear_rol_fan(rol_fan_page: Rol_Fan_PageCreate, db: Session = Depends(get_db)):
    # Verificar si las entidades relacionadas existen
    persona_existente = db.query(Persona).filter(Persona.cod_per == rol_fan_page.fky_per).first()
    fan_page_existente = db.query(Fan_Page).filter(Fan_Page.cod_fan_pag == rol_fan_page.fky_fan_pag).first()
    rol_existente = db.query(Rol).filter(Rol.cod_rol == rol_fan_page.fky_rol).first()

    if persona_existente is None or fan_page_existente is None or rol_existente is None:
        raise HTTPException(status_code=400, detail="Entidad relacionada no encontrada")

    # Crear el nuevo registro de Rol_Fan_Page
    db_rol_fan = Rol_Fan_Page(**rol_fan_page.dict())
    db.add(db_rol_fan)
    db.commit()
    db.refresh(db_rol_fan)
    return db_rol_fan

@app.get("/rol_fan_pages/", response_model=List[Rol_Fan_PageResponse])
def leer_rol_fan(db: Session = Depends(get_db)):
    rols_fan = db.query(Rol_Fan_Page).options(
        joinedload(Rol_Fan_Page.persona),
        joinedload(Rol_Fan_Page.fan_page),
        joinedload(Rol_Fan_Page.rol)
    ).order_by(Rol_Fan_Page.cod_rol_fan).all()
    return rols_fan

@app.get("/rol_fan_pages/{cod_rol_fan}", response_model=Rol_Fan_PageResponse)
def leer_rol_fan(cod_rol_fan: int, db: Session = Depends(get_db)):
    rol_fan = db.query(Rol_Fan_Page).options(
        joinedload(Rol_Fan_Page.persona),
        joinedload(Rol_Fan_Page.fan_page),
        joinedload(Rol_Fan_Page.rol)
    ).filter(Rol_Fan_Page.cod_rol_fan == cod_rol_fan).first()

    if rol_fan is None:
        raise HTTPException(status_code=404, detail="Rol Fan Page no encontrado")
    return rol_fan

@app.put("/rol_fan_pages/{cod_rol_fan}", response_model=Rol_Fan_PageResponse)
def actualizar_rol_fan(cod_rol_fan: int, rol_fan_page: Rol_Fan_PageCreate, db: Session = Depends(get_db)):
    # Obtener el registro existente de Rol_Fan_Page
    db_rol_fan = db.query(Rol_Fan_Page).options(
        joinedload(Rol_Fan_Page.persona),
        joinedload(Rol_Fan_Page.fan_page),
        joinedload(Rol_Fan_Page.rol)
    ).filter(Rol_Fan_Page.cod_rol_fan == cod_rol_fan).first()

    if db_rol_fan is None:
        raise HTTPException(status_code=404, detail="Rol Fan Page no encontrado")

    # Verificar si las entidades relacionadas existen
    persona_existente = db.query(Persona).filter(Persona.cod_per == rol_fan_page.fky_per).first()
    fan_page_existente = db.query(Fan_Page).filter(Fan_Page.cod_fan_pag == rol_fan_page.fky_fan_pag).first()
    rol_existente = db.query(Rol).filter(Rol.cod_rol == rol_fan_page.fky_rol).first()

    if persona_existente is None or fan_page_existente is None or rol_existente is None:
        raise HTTPException(status_code=400, detail="Entidad relacionada no encontrada")

    # Actualizar los campos del registro
    db_rol_fan.fky_per = rol_fan_page.fky_per
    db_rol_fan.fky_fan_pag = rol_fan_page.fky_fan_pag
    db_rol_fan.fky_rol = rol_fan_page.fky_rol
    db_rol_fan.est_rol_fan = rol_fan_page.est_rol_fan  # Actualizar el campo est_rol_fan

    db.commit()
    db.refresh(db_rol_fan)
    return db_rol_fan

@app.delete("/rol_fan_pages/{cod_rol_fan}", response_model=Rol_Fan_PageResponse)
def eliminar_rol_fan(cod_rol_fan: int, db: Session = Depends(get_db)):
    # Obtener el registro existente de Rol_Fan_Page
    db_rol_fan = db.query(Rol_Fan_Page).options(
        joinedload(Rol_Fan_Page.persona),
        joinedload(Rol_Fan_Page.fan_page),
        joinedload(Rol_Fan_Page.rol)
    ).filter(Rol_Fan_Page.cod_rol_fan == cod_rol_fan).first()

    if db_rol_fan is None:
        raise HTTPException(status_code=404, detail="Rol Fan Page no encontrado")

    # Eliminar el registro de la base de datos
    db.delete(db_rol_fan)
    db.commit()

    return db_rol_fan

# Endpoint para crear un Fan_Page
@app.post("/fan_pages/", response_model=Fan_PageResponse)
def create_fan_page(fan_page: Fan_PageCreate, db: Session = Depends(get_db)):
    db_fan_page = Fan_Page(**fan_page.dict())
    db.add(db_fan_page)
    db.commit()
    db.refresh(db_fan_page)
    return db_fan_page

# Endpoint para leer todos los Fan_Page
@app.get("/fan_pages/", response_model=List[Fan_PageResponse])
def read_fan_pages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    fan_pages = db.query(Fan_Page).offset(skip).limit(limit).all()
    return fan_pages

# Endpoint para leer un Fan_Page por ID
@app.get("/fan_pages/{cod_fan_pag}", response_model=Fan_PageResponse)
def read_fan_page(cod_fan_pag: int, db: Session = Depends(get_db)):
    db_fan_page = db.query(Fan_Page).filter(Fan_Page.cod_fan_pag == cod_fan_pag).first()
    if db_fan_page is None:
        raise HTTPException(status_code=404, detail="Fan Page not found")
    return db_fan_page

# Endpoint para actualizar un Fan_Page
@app.put("/fan_pages/{cod_fan_pag}", response_model=Fan_PageResponse)
def update_fan_page(cod_fan_pag: int, fan_page: Fan_PageCreate, db: Session = Depends(get_db)):
    db_fan_page = db.query(Fan_Page).filter(Fan_Page.cod_fan_pag == cod_fan_pag).first()
    if db_fan_page is None:
        raise HTTPException(status_code=404, detail="Fan Page not found")
    for key, value in fan_page.dict().items():
        setattr(db_fan_page, key, value)
    db.commit()
    db.refresh(db_fan_page)
    return db_fan_page

# Endpoint para eliminar un Fan_Page
@app.delete("/fan_pages/{cod_fan_pag}", response_model=Fan_PageResponse)
def delete_fan_page(cod_fan_pag: int, db: Session = Depends(get_db)):
    db_fan_page = db.query(Fan_Page).filter(Fan_Page.cod_fan_pag == cod_fan_pag).first()
    if db_fan_page is None:
        raise HTTPException(status_code=404, detail="Fan Page not found")
    db.delete(db_fan_page)
    db.commit()
    return db_fan_page

# Endpoint para crear un Rol
@app.post("/roles/", response_model=RolResponse)
def create_rol(rol: RolCreate, db: Session = Depends(get_db)):
    db_rol = Rol(**rol.dict())
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

# Endpoint para leer todos los Roles
@app.get("/roles/", response_model=List[RolResponse])
def read_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    roles = db.query(Rol).offset(skip).limit(limit).all()
    return roles

# Endpoint para leer un Rol por ID
@app.get("/roles/{cod_rol}", response_model=RolResponse)
def read_rol(cod_rol: int, db: Session = Depends(get_db)):
    db_rol = db.query(Rol).filter(Rol.cod_rol == cod_rol).first()
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol not found")
    return db_rol

# Endpoint para actualizar un Rol
@app.put("/roles/{cod_rol}", response_model=RolResponse)
def update_rol(cod_rol: int, rol: RolCreate, db: Session = Depends(get_db)):
    db_rol = db.query(Rol).filter(Rol.cod_rol == cod_rol).first()
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol not found")
    for key, value in rol.dict().items():
        setattr(db_rol, key, value)
    db.commit()
    db.refresh(db_rol)
    return db_rol

# Endpoint para eliminar un Rol
@app.delete("/roles/{cod_rol}", response_model=RolResponse)
def delete_rol(cod_rol: int, db: Session = Depends(get_db)):
    db_rol = db.query(Rol).filter(Rol.cod_rol == cod_rol).first()
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol not found")
    db.delete(db_rol)
    db.commit()
    return db_rol


# Endpoints CRUD para Persona
@app.post("/personas/", response_model=PersonaResponse)
def create_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    db_persona = Persona(**persona.dict())
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona

@app.get("/personas/", response_model=List[PersonaResponse])
def read_personas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    personas = db.query(Persona).offset(skip).limit(limit).all()
    return personas

@app.get("/personas/{cod_per}", response_model=PersonaResponse)
def read_persona(cod_per: int, db: Session = Depends(get_db)):
    db_persona = db.query(Persona).filter(Persona.cod_per == cod_per).first()
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona not found")
    return db_persona

@app.put("/personas/{cod_per}", response_model=PersonaResponse)
def update_persona(cod_per: int, persona: PersonaCreate, db: Session = Depends(get_db)):
    db_persona = db.query(Persona).filter(Persona.cod_per == cod_per).first()
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona not found")
    for key, value in persona.dict().items():
        setattr(db_persona, key, value)
    db.commit()
    db.refresh(db_persona)
    return db_persona

@app.delete("/personas/{cod_per}", response_model=PersonaResponse)
def delete_persona(cod_per: int, db: Session = Depends(get_db)):
    db_persona = db.query(Persona).filter(Persona.cod_per == cod_per).first()
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona not found")
    db.delete(db_persona)
    db.commit()
    return db_persona
