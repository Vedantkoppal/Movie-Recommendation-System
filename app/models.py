from app import db

class Movie(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(70))
    def __repr__(self):
        return '<Movie: {}>'.format(self.title)

class TopMovie(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(75))
    def __repr__(self):
        return '<Movie: {}>'.format(self.title)
