from models import Venue, Artist, Show, db
from datetime import datetime


class VenueAccess:
    @classmethod
    def create_venue_using_form(cls, form):
        try:
            new_venue = Venue(
                name=form['name'],
                city=form['city'],
                state=form['state'],
                address=form['address'],
                phone=form['phone'],
                genres=form.getlist('genres'),
                facebook_link=form['facebook_link']
            )
            db.session.add(new_venue)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.close()
            raise ValueError('This for is in valid')
        
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
        data = db.session.query(Venue.city, Venue.state).group_by(Venue.city, Venue.state)
        venues_data = []
        for a in data:
            area = a._asdict()
            area['venues'] = [ven.convert_to_dict() for ven in Venue.query.filter_by(city=area['city']).all()]
            venues_data.append(area)
        return venues_data

    @classmethod
    def _get_show_data(cls, venue_id, date_filter_function):
        shows = (db.session.query(Artist.id.label("artist_id"), Artist.name.label("artist_name"),
                                  Artist.image_link.label("artist_image_link"), Show)
                 .filter(Show.c.venue_id == venue_id)
                 .filter(date_filter_function(Show.c.start_time, datetime.now()))
                 .all())
        return shows

    @classmethod
    def get_upcoming_shows(cls, venue_id):
        def date_filter_function(show_time, current_time):
            return show_time > current_time

        return cls._get_show_data(venue_id, date_filter_function)

    @classmethod
    def get_past_shows(cls, venue_id):
        def date_filter_function(show_time, current_time):
            return show_time <= current_time

        return cls._get_show_data(venue_id, date_filter_function)

    @classmethod
    def get_venue_show_data(cls, venue_id):
        venue = Venue.query.get(venue_id)
        venue.past_shows = cls.get_past_shows(venue_id)
        venue.upcoming_shows = cls.get_upcoming_shows(venue_id)
        venue.past_shows_count = len(venue.past_shows)
        venue.upcoming_shows_count = len(venue.upcoming_shows)
        return venue
