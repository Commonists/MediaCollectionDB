""" mediacollectiondb database define the media collection datbase
and provides tools to manage the database."""
import sqlite3


class MediaCollection(object):

    """ Persistent media collection, i.e. collection saved into
    SQLite database.

    Attributes:
        connection: sqlite connection.
        cursor: sqlite cursor.
    """

    COLLECTIONS_TABLE = "media_collections"

    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
        table_creation = """CREATE TABLE IF NOT EXISTS %s
                                (pageid, 
                                filename,
                                uploader,
                                width,
                                height,
                                size,
                                quality_image,
                                featured_pictured,
                                valued_image,
                                timestamp)
                        """ % MediaCollection.COLLECTIONS_TABLE
        self.cursor.execute(table_creation)
        self.cursor.commit()

    def add(self, media):
        """ Add media to the persistent media collection.

        Args:
            media: media object to save to the into the persistent collection.
        """
        pass

    def reset(self):
        """ Delete all entry in the database. """
        reset_query = "DELETE * FROM %s" % MediaCollection.COLLECTIONS_TABLE
        self.cursor.execute(reset_query)
