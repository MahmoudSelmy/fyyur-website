from .core_model import *
from forms import ArtistForm


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String())

    def convert_venue_to_form(self):
        form = ArtistForm()
        form.name.data = self.name
        form.city.data = self.city
        form.state.data = self.state
        form.address.data = self.address
        form.phone.data = self.phone
        form.genres.data = self.genres
        form.facebook_link.data = self.facebook_link
        return form
