from datetime import datetime
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    # CHILD - MANY TO ONE
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

#       caretaker_id = db.Column(db.Integer, db.ForeignKey('caretaker.id'))
#   caretaker = db.relationship("Caretaker", back_populates="cats")

    # TURN TO JSON
    def to_json(self):
        is_complete = True if self.completed_at else False;
        if self.goal_id:
            return{
                    "id": self.task_id,
                    "title": self.title,
                    "description" : self.description,
                    "is_complete" : is_complete,
                    "goal_id" : self.goal_id
            }
        else:
            return{
                    "id": self.task_id,
                    "title": self.title,
                    "description" : self.description,
                    "is_complete" : is_complete
            }


    # UPDATE
    def update(self, request_body):
        # is_complete = True if self.completed_at else None;
        self.title = request_body["title"]
        self.description = request_body["description"]


    # CREATE
    @classmethod
    def create(cls, request_body):
        if "completed_at" in request_body:
            new_task = cls(
                title = request_body["title"],
                description = request_body["description"],
                completed_at = request_body["completed_at"]
            )
        else:
            new_task = cls(
                title = request_body["title"],
                description = request_body["description"],
            )

        return new_task

    # MARK
    def patch_complete(self, request_body):
        self.completed_at = datetime.utcnow()

    # MARK
    def patch_imcomplete(self, request_body):
        self.completed_at = None

