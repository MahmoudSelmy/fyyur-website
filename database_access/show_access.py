from models import Venue, Artist, Show, db
from datetime import datetime


class ShowAccess:
    @classmethod
    def create_show_using_form(cls, form):
        try:
            new_show = Show.insert().values(
                venue_id=form['venue_id'],
                artist_id=form['artist_id'],
                start_time=form['start_time']
            )
            db.session.execute(new_show)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.close()
            raise ValueError('This for is in valid')

    @classmethod
    def get_all_shows_display_data(cls):
        shows = (db.session.query(Venue.id.label("venue_id"), Venue.name.label("venue_name"),
                                  Artist.id.label("artist_id"),
                                  Artist.name.label("artist_name"),
                                  Artist.image_link.label("artist_image_link"),
                                  Show)
                 .filter(Show.c.venue_id == Venue.id)
                 .filter(Show.c.artist_id == Artist.id)
                 .all())
        return shows
