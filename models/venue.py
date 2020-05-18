from datetime import datetime

from .core_model import *
from .show import Show

from forms import VenueForm


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())
    artists = db.relationship('Artist', secondary=Show, backref=db.backref('venues', lazy=True))

    def convert_to_dict(self):
        upcoming_count = (db.session.query(func.count(Show.c.venue_id))
            .filter(Show.c.venue_id == self.id)
            .filter(Show.c.start_time > datetime.now()).all()[0][0])
        return {
            'id': self.id,
            'name': self.name,
            'num_upcoming_shows': upcoming_count
        }

    def convert_venue_to_form(self):
        form = VenueForm()
        form.name.data = self.name
        form.city.data = self.city
        form.state.data = self.state
        form.address.data = self.address
        form.phone.data = self.phone
        form.genres.data = self.genres
        form.facebook_link.data = self.facebook_link
        return form
