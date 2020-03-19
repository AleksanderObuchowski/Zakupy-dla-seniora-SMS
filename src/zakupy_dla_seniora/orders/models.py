from zakupy_dla_seniora import sql_db as db
from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint, exc
from zakupy_dla_seniora.sms_handler.models import Messages


class Orders(db.Model):
    __tablename__ = 'order'
    __table_args__ = (UniqueConstraint('user_id', 'message_id', name='unique_message_user'),)
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    message_id = db.Column('message_id', db.Integer, db.ForeignKey('message.id'))
    order_status = db.Column('order_status', db.String(40))
    order_date = db.Column('order_date', db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, message_id, order_status, order_date):
        self.user_id = user_id
        self.message_id = message_id
        self.order_status = order_status
        self.order_date = order_date

    def prepare_board_view(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'message_id': self.message_id,
            'order_status': self.order_status,
            'order_date': str(self.order_date)
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
