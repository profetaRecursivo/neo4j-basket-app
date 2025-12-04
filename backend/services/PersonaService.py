from backend.database.DBManager import DBManager


class PersonaService:
    def __init__(self):
        self.db = DBManager()

    def create_persona(
        self, nombres: str, apellidos: str, fecha_nacimiento: str, sexo: str, pais
    ):
        session = self.db.get_session()
        try:
            record = session.run(
                """
                MATCH (country:Pais WHERE country.nombre = $pais)
                CREATE (p:Persona{id_persona:randomUUID(), nombres:$nombres, apellidos:$apellidos, fecha_nacimiento:$fecha_nacimiento, sexo:$sexo})-[:NACIDO_EN]->(country)
                RETURN p
            """,
                pais=pais,
                nombres=nombres,
                apellidos=apellidos,
                fecha_nacimiento=fecha_nacimiento,
                sexo=sexo,
            ).single()
            if not record:
                return {
                    "success": False,
                    "error": "País no encontrado o error en query create_persona",
                }
            return {"success": True, "Persona": record["p"]}
        finally:
            session.close()
