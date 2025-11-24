from ctypes import resize
from neo4j import Session
from backend.database.DBManager import DBManager


class Auth:
    def __init__(self):
        self.db = DBManager()

    def login(self, username: str, password: str) -> dict:
        session = self.db.get_session()
        record = session.run("MATCH (p:UserN) where p.user = $user and p.password = $pword return p", user=username, pword=password).single()

        if not record:
            return {"success": False, "error": "Credenciales inválidas"}
        node = record["p"]
        id_userN = node["id_userN"]
        pid = str(self.db.get_pid())
        record = session.run("create (s:Sesion {id_sesion:randomUUID(), PID:$pid, active:true, id_userN:$id_userN}) return s.id_sesion as id_sesion", pid=pid, id_userN = id_userN).single()
        id_sesion = record["id_sesion"]
        return {
            "success": True,
            "user_id": id_userN,
            "sesion_id": id_sesion,
            "username": username,
        }
    

    def logout(self, id_sesion: int) -> dict:
        session = self.db.get_session()
        try:
            record = session.run("match (s:Sesion) where s.id_sesion = $id_sesion return s", id_sesion=id_sesion).single()
            if record:
                session.run("match (s:Sesion) where s.id_sesion = $id_sesion set s.active = false")
                return {"success": True}
            return {"success": False, "error": "Sesión no encontrada"}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            session.close()
if __name__ == "__main__":
    auth = Auth()
    result = auth.login("gordon", "freeman")
    if result["success"]:
        print("se logro")
    else: 
        print("nimodo")