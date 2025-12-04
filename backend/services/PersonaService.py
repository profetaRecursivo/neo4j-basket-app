from backend.database.DBManager import DBManager


class PersonaService:
    def __init__(self):
        self.db = DBManager()

    def create_persona(
        self, nombres: str, apellidos: str, fecha_nacimiento: str, sexo: str, pais
    ):
        session = self.db.get_session()
        record = session.run("""
            match(country:Pais{nombre=$pais})
            create(p:Persona{id_persona:randomUUID(),  nombres:$nombres, apellidos:$apellidos, fecha_nacimiento:$fecha_nacimiento, sexo:$sexo}) -[NACIDO_EN]->(country)
            return p;
        """, pais=pais, nombres=nombres, apellidos=apellidos, fecha_nacimiento=fecha_nacimiento, sexo=sexo).single()
        if not record:
            return {"success": False, "error":"error on query create_persona"}
        return {"success":True, "Persona":record["p"]}
        
