from backend.database.DBManager import DBManager


class PaisService:
    def __init__(self):
        self.db = DBManager()
    def get_all_countries(self):
        session = self.db.get_session()
        record = session.run("""
        Match(p:Pais)
        return collect(p.nombre) as all_countries
        """).single()
        if record:
            return record["all_countries"]
        return []