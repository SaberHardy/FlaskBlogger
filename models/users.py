# from datetime import datetime
#
# from app import db
#
#
# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(200), nullable=False, unique=True)
#     date_added = db.Column(db.DateTime, default=datetime.utcnow)
#
#     # Create string
#
#     def __repr__(self):
#         return '<Name %r>' % self.name
