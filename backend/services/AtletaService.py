from backend.database.DBManager import DBManager
from backend.services.PersonaService import PersonaService


class AtletaService:
    def __init__(self):
        self.db = DBManager()

    def create_atleta(
        self,
        nombres: str,
        apellidos: str,
        fecha_nacimiento: str,
        sexo: str,
        pais: str,
        altura: float,
        peso_kg: float,
    ):
        session = self.db.get_session()
        insercion = PersonaService().create_persona(
            nombres, apellidos, fecha_nacimiento, sexo, pais
        )
        if insercion["success"]:
            session.run(
                """
                Match (p: Persona {id_persona:$id_persona})
                Set p:Atleta,
                p.altura = $altura,
                p.peso_kg = $peso_kg;
            """,
                altura=altura,
                peso_kg=peso_kg,
                id_persona=insercion["Persona"]["id_persona"]
            )
            return {"success": True}
        else:
            return {"success": False, "error": insercion["error"]}
