from .core_model import *

Show = db.Table('show',
                db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')),
                db.Column('venue_id', db.Integer, db.ForeignKey('venue.id')),
                db.Column('start_time', db.DateTime)
                )
