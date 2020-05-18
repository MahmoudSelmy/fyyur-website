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
                facebook_link=form['facebook_link'])
            db.session.add(new_artist)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.close()
            raise ValueError('This for is in valid')

