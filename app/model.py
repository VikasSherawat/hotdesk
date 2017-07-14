from middleware import db, bcrypt

class Seats(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    building = db.Column(db.Integer, unique = False)
    floor = db.Column(db.Integer, unique = False)
    seatnum = db.Column(db.Integer, unique = True)
    user = db.Column(db.String(100), default="0", nullable = True)
    status = db.Column(db.String(25), default = 'Free', nullable = True)
    teamname = db.Column(db.String(25), nullable = True)
    row = db.Column(db.Integer, unique = False)

    def __repr__(self):
        return '<Seat %r>' % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    building = db.Column(db.Integer, unique = False)
    floor = db.Column(db.Integer, unique = False)
    roomnum = db.Column(db.Integer, unique = True)
    bookings = db.relationship('Booking', backref='Room',lazy='dynamic')

    def __repr__(self):
        return '<Room %r>' % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    user = db.Column(db.String(100), nullable = True)
    

