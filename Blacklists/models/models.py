import datetime

from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

import pytz

db = SQLAlchemy()

class Blacklist(db.Model):
    id = db.Column(db.String(50), primary_key=True)  
    email = db.Column(db.String(140))  
    app_uuid = db.Column(db.String(50), nullable=False, name="app_uuid")  
    blocked_reason = db.Column(db.String(255))  
    ip = db.Column(db.String(255))  
    requestDate = db.Column(db.DateTime, default=lambda: datetime.now(pytz.utc), nullable=False, name="requestDate")          

    def __init__(self, id, email, app_uuid, blocked_reason, ip, requestDate=None):
        self.id = id
        self.email = email
        self.app_uuid = app_uuid
        self.blocked_reason = blocked_reason
        self.ip = ip
        self.requestDate = requestDate or datetime.datetime.now(pytz.utc)                

    def __repr__(self):
        return "{}-{}-{}-{}-{}-{}".format(self.id, self.email, self.app_uuid, self.blocked_reason, self.ip, self.requestDate)

class BlacklistSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Blacklist
        include_relationships = True
        load_instance = True
