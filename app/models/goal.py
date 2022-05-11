from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    # TURN INTO JSON
    def g_json(self):
        return {
            "id": self.id,
            "title": self.title
        }

    @classmethod
    def create(cls, request_body):
        new_goal = cls(
            title = request_body["title"],
        )
    
        return new_goal


    # UPDATE GOAL
    def update_goal(self, request_body):
        self.title =  request_body["title"]




