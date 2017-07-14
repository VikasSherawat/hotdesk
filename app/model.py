from middleware import db, bcrypt

class Seats(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    building = db.Column(db.Integer, unique = False)
    floor = db.Column(db.Integer, unique = False)
    seatnum = db.Column(db.Integer, unique = True)

    def __repr__(self):
        return '<User %r>' % self.user_id

    def save(self):
        db.session.add(self)
        db.session.commit()
    
