from backend.database.DBManager import DBManager


class Auth:
    def __init__(self):
        self.db = DBManager()

    def login(self, username: str, password: str) -> dict:
        session = self.db.get_session()
        try:
            record = session.run(
                "MATCH (p:UserN) where p.user = $user and p.password = $pword return p",
                user=username,
                pword=password,
            ).single()

            if not record:
                return {"success": False, "error": "Credenciales inválidas"}
            user_node = record["p"]
            self.create_session(user_node=user_node)
            return {"success": True, "user": username}
        finally:
            session.close()

    def logout(self, user):
        session = self.db.get_session()
        try:
            session.run(
                """
            match(u:UserN {user:$user})-[r:TIENE_SESION]->(s:Sesion)
            set r.active = false
            """,
                user=user,
            )
        finally:
            session.close()

    def create_session(self, user_node):
        session = self.db.get_session()
        try:
            session.run(
                """
                MATCH  (p:UserN{user:$u})
                CREATE (s:Sesion{PID:$connection_id})
                CREATE (p)-[:TIENE_SESION {active:true}]->(s)
                """,
                connection_id=self.db.get_pid(),
                u=user_node["user"],
            )
        finally:
            session.close()


if __name__ == "__main__":
    auth = Auth()
    result = auth.login("gordon", "freeman")
    if result["success"]:
        print("se logro")
    else:
        print("nimodo")
