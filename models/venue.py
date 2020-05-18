from datetime import datetime

from .core_model import *
from .show import Show


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

    @classmethod
    def search_venues(cls, search_term):
        venues = Venue.query.filter(Venue.name.contains(search_term)).all()
        response = {
            "count": len(venues),
            "data": venues
        }
        return response

    @classmethod
    def get_all_venues_grouped_by_area(cls):
        data = db.session.query(Venue.city, cls.state).group_by(cls.city, cls.state)
        venues_data = []
        for a in data:
            area = a._asdict()
            area['venues'] = [ven.convert_to_dict() for ven in cls.query.filter_by(city=area['city']).all()]
            venues_data.append(area)
        return venues_data

    @classmethod
    def _get_show_data(cls, Artist, venue_id, date_filter_function):
        shows = (db.session.query(Artist.id.label("artist_id"), Artist.name.label("artist_name"),
                                  Artist.image_link.label("artist_image_link"), Show)
                 .filter(Show.c.venue_id == venue_id)
                 .filter(date_filter_function(Show.c.start_time, datetime.now()))
                 .all())
        return shows

    @classmethod
    def get_upcoming_shows(cls, Artist, venue_id):
        def date_filter_function(show_time, current_time):
            return show_time > current_time

        return cls._get_show_data(Artist, venue_id, date_filter_function)

    @classmethod
    def get_past_shows(cls, Artist, venue_id):
        def date_filter_function(show_time, current_time):
            return show_time <= current_time

        return cls._get_show_data(Artist, venue_id, date_filter_function)

    @classmethod
    def get_venue_show_data(cls, Artist, venue_id):
        venue = cls.query.get(venue_id)
        venue.past_shows = cls.get_past_shows(Artist, venue_id)
        venue.upcoming_shows = cls.get_upcoming_shows(Artist, venue_id)
        venue.past_shows_count = len(venue.past_shows)
        venue.upcoming_shows_count = len(venue.upcoming_shows)
        return venue
