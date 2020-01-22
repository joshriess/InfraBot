import enum
import InfraBot
from datetime import datetime

db = InfraBot.db

class request_status(enum.Enum):
    REQUESTED = 1
    ACCEPTED = 2
    DECLINED = 3
    IMPLEMENTED = 4

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    request_status = db.Column('request_status', db.Enum(request_status), nullable=False)
    request_time = db.Column(db.DateTime(), nullable=False)
    zone = db.relationship('ZoneRequest', lazy=True)
    dhcp = db.relationship('DHCPRequest', lazy=True)
    record = db.relationship('RecordRequest', lazy=True)

class ZoneRequest(db.Model):
    def __init__(self, user_id, ipaddr):
        newReq = Request(user_id=user_id, request_status=request_status.REQUESTED, request_time=datetime.now())
        db.session.add(newReq)
        db.commit()
        self.ipaddr = ipaddr
        self.request_id = newReq.id
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    ipaddr = db.Column(db.String(50), nullable=False)

class DHCPRequest(db.Model):
    def __init__(self, user_id, mac):
        newReq = Request(user_id=user_id, request_status=request_status.REQUESTED, request_time=datetime.now())
        db.session.add(newReq)
        db.commit()
        self.mac = mac
        self.request_id = newReq.id
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    mac = db.Column(db.String(50), nullable=False)

class UsernameRequest(db.Model):
    def __init__(self, user_id, username):
        newReq = Request(user_id=user_id, request_status=request_status.REQUESTED, request_time=datetime.now())
        db.session.add(newReq)
        db.commit()
        self.username = username
        self.request_id = newReq.id
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    username = db.Column(db.String(50), nullable=False)
