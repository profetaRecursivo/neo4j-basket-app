from backend.database.DBManager import DBManager

class UIService:
    def __init__(self, user):
        self.db = DBManager()
        self.user = user

    def get_ui_ids(self) -> dict:
        with self.db.get_session() as session:
            try:
                query = """
                MATCH (u:UserN {user: $user})-[r1:TIENE_ROL]->(rol:Rol)-[r2:TIENE_FUNCION]->(f:Funcion)-[r3:TIENE_UI]->(ui:UI)
                WHERE r1.active = true AND r2.active = true AND r3.active = true
                RETURN collect(DISTINCT ui.nombre) as ui_list
                """
                
                result = session.run(query, user=self.user)
                record = result.single()
                
                if record:
                    lista_uis = record["ui_list"]
                    return {"success": True, "ui_ids": lista_uis}
                else:
                    return {"success": True, "ui_ids": []}

            except Exception as e:
                print(f"Error en get_ui_ids: {e}")
                return {"success": False, "ui_ids": [], "error": str(e)}