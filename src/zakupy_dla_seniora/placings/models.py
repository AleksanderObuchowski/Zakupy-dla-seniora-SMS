from zakupy_dla_seniora import sql_db as db
from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint, exc


class Placings(db.Model):
    __tablename__ = 'placing'
    __table_args__ = (UniqueConstraint('user_id', 'message_id', name='unique_message_user'),)
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    message_id = db.Column('message_id', db.Integer, db.ForeignKey('message.id'))
    placing_status = db.Column('placing_status', db.String(40), default='Waiting')
    placing_date = db.Column('placing_date', db.DateTime)

    def __init__(self, user_id, message_id, placing_status = "waiting for address", placing_date = datetime.now(timezone.utc)):
        self.user_id = user_id
        self.message_id = message_id
        self.placing_status = placing_status
        self.placing_date = placing_date

    def prepare_board_view(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'message_id': self.message_id,
            'placing_status': self.placing_status,
            'placing_date': str(self.placing_date)
        }

    def update_by_user_id(self, user_id, status):
        db.session.query(Placings).filter(Placings.user_id == user_id).update({'placing_status': status})
        db.session.commit()

    def update_by_message_id(self, message_id, status):
        db.session.query(Placings).filter(Placings.message_id == message_id).update({'placing_status' : status})
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()
