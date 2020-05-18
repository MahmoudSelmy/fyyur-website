from models import Venue, Artist, Show, db
from datetime import datetime


class ArtistAccess:
    @classmethod
    def create_artist_from_form(cls, form):
        try:
            new_artist = Artist(
                name=form['name'],
                city=form['city'],
                state=form['state'],
                phone=form['phone'],
                genres=form.getlist('genres'),
                image_link=form['image_link'],
                facebook_link=form['facebook_link'])
            db.session.add(new_artist)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.close()
            raise ValueError('This for is in valid')

    @classmethod
    def get_all_artists(cls):
        return Artist.query.all()

    @classmethod
    def search_artists(cls, search_term):
        artists = Artist.query.filter(Artist.name.contains(search_term)).all()
        response = {
            "count": len(artists),
            "data": artists
        }
        return response

    @classmethod
    def _get_show_data(cls, artist_id, date_filter_function):
        shows = (db.session.query(Venue.id.label("venue_id"),
                                  Venue.name.label("venue_name"),
                                  Venue.image_link.label("venue_image_link"), Show)
                 .filter(Show.c.artist_id == artist_id)
                 .filter(Show.c.venue_id == Venue.id)
                 .filter(date_filter_function(Show.c.start_time, datetime.now()))
                 .all())
        return shows

    @classmethod
    def get_upcoming_shows(cls, artist_id):
        def date_filter_function(show_time, current_time):
            return show_time > current_time

        return cls._get_show_data(artist_id, date_filter_function)

    @classmethod
    def get_past_shows(cls, artist_id):
        def date_filter_function(show_time, current_time):
            return show_time <= current_time

        return cls._get_show_data(artist_id, date_filter_function)

    @classmethod
    def get_artist_show_data(cls, artist_id):
        artist = Artist.query.get(artist_id)
        artist.past_shows = cls.get_past_shows(artist_id)
        artist.upcoming_shows = cls.get_upcoming_shows(artist_id)
        artist.past_shows_count = len(artist.past_shows)
        artist.upcoming_shows_count = len(artist.upcoming_shows)
        return artist

    @classmethod
    def get_artist_by_id(cls, artist_id):
        return Artist.query.get(artist_id)

    @classmethod
    def update_artist_using_form(cls, artist_id, form):
        artist = Artist.query.get(artist_id)
        artist.name = form['name'],
        artist.city = form['city'],
        artist.state = form['state'],
        artist.phone = form['phone'],
        artist.genres = form.getlist('genres'),
        artist.facebook_link = form['facebook_link']
        db.session.add(artist)
        db.session.commit()
        db.session.close()
