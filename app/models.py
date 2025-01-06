from app import db

class Movie(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    moviename = db.Column(db.String(70),unique = True)
    rating = db.Column(db.Float)
    def __repr__(self):
        return '<Movie: {}>'.format(self.moviename)

class MovieMain(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(75),unique = False)
    year = db.Column(db.Integer,unique = False)
    def __repr__(self):
        return '<Movie: {}>'.format(self.title)
