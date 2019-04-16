from json import dumps

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import relationship

from . import Base

__all__ = [
    'Users',
    'Playlists',
    'Songs',
]


class Users(Base):
    __tablename__ = 'Users'
    id_ = Column('id', Integer, primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    password = Column(String(72), nullable=False)
    admin = Column(Boolean, default=False)

    def __repr__(self):
        return f'<{"Admin" if self.admin else "User"} {self.username}>'

    def __str__(self):
        return dumps(self.to_json())

    def to_json(self):
        return {
            'id': self.id_,
            'username': self.username,
            'admin': self.admin,
        }


class Songs(Base):
    __tablename__ = 'Songs'
    id_ = Column('id', Integer, primary_key=True)
    filepath = Column(String)
    artist = Column(String(32))
    title = Column(String(64))
    album = Column(String(32))
    genre = Column(String(32))
    length = Column(Integer)

    def __repr__(self):
        return f'<Song {self.artist} - {self.title}>'

    def __str__(self):
        return dumps(self.to_json())

    def to_json(self):
        return {
            'id': self.id_,
            'filepath': self.filepath,
            'artist': self.artist,
            'title': self.title,
            'album': self.album,
            'genre': self.genre,
            'length': self.length,
        }


song_playlist_association_table = Table(
    'song_playlist_association', Base.metadata,
    Column('song_id', Integer, ForeignKey('Songs.id')),
    Column('playlist_id', Integer, ForeignKey('Playlists.id'))
)


class Playlists(Base):
    __tablename__ = 'Playlists'
    id_ = Column('id', Integer, primary_key=True)
    name = Column(String(32))
    user_id = Column(Integer, ForeignKey('Users.id'))
    user = relationship("Users", backref="playlists")
    songs = relationship('Songs', secondary=lambda: song_playlist_association_table, backref="playlists")

    def __repr__(self):
        return f'<Playlist {self.name}>'

    def __str__(self):
        return dumps(self.to_json())

    def to_json(self):
        return {
            'id': self.id_,
            'name': self.name,
            'user_id': self.user_id,
            'user': self.user.to_json(),
            'songs': self.songs,
        }
