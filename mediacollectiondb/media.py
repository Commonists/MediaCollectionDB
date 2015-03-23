""" mediacollectiondb database define the media collection datbase
and provides tools to manage the database.
"""

import sqlite3


class Media(object):

    """ Media representation in database.

    Attributes:
        pageid (str): MediaWiki pageid
        filename (unicode): MediaWiki filename
        uploader (unicode): Username of the uploader
        width (int): width of the image
        height (int): height of the image
        size (int): Size in pixels of the image (width x height)
        quality_image (bool): Whether the image is quality image or
            not
        featured_picture (bool): Whether the image is featured
            picture or not
        valued_image (bool): Whether the image is valued image or not
        timestamp (date): Datetime of upload
    """

    def __init__(self, pageid, filename, uploader=None, width=None,
                 height=None, size=None, quality_image=None,
                 featured_picture=None, valued_image=None, timestamp=None):
        """ Constructor.

        Args:
            pageid (str): MediaWiki pageid
            filename (unicode): MediaWiki filename
            uploader (unicode, optional): Username of the uploader
            width (int, optional): width of the image
            height (int, optional): height of the image
            size (int, optional): Size in pixels of the image (width x height)
            quality_image (bool, optional): Whether the image is quality image
                or not
            featured_picture (bool, optional): Whether the image is featured
                picture or not
            valued_image (bool, optional): Whether the image is valued image or
                not
            timestamp (date, optional): Datetime of upload
        """
        self.pageid = str(pageid)
        self.filename = filename
        self.uploader = uploader
        self.width = width
        self.height = height
        self.size = size
        self.quality_image = quality_image
        self.featured_picture = featured_picture
        self.valued_image = valued_image
        self.timestamp = timestamp

    def totuple(self):
        """ Return the object as a tuple of all values. """
        return (self.pageid, self.filename, self.uploader, self.width,
                self.height, self.size, self.quality_image,
                self.featured_picture, self.valued_image, self.timestamp)

    @classmethod
    def fromtuple(cls, media):
        """ Return a Media from a tuple. """
        return cls(media[0], media[1], media[2], media[3], media[4], media[5],
                   media[6], media[7], media[8], media[9])


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
                                featured_picture,
                                valued_image,
                                timestamp)
                        """ % MediaCollection.COLLECTIONS_TABLE
        self.cursor.execute(table_creation)
        self.connection.commit()

    def save(self, media):
        """ Add media to the persistent media collection.

        Args:
            media: media object to save to the into the persistent collection.
        """
        if self.exists(media):
            self.update(media)
        else:
            self.insert(media)

    def exists(self, media):
        """ Testing whether a media is already in database or not.

        In order to test whether the media is already in the database we count
        whether there is more than 0 element in the table with the same pageid

        Args:
            media (dict): a media to check if it is in the database.

        Returns:
            bool: True if a media with the same pageid exists in the database
                False otherwise
        """
        select_query = """SELECT * FROM %s
            WHERE pageid=?""" % MediaCollection.COLLECTIONS_TABLE
        self.cursor.execute(select_query, (media.pageid,))
        pages = self.cursor.fetchall()
        return len(pages) > 0

    def update(self, media):
        """ Updating a media already in database. """
        update_query = """UPDATE %s
            SET
                filename=?,
                uploader=?,
                width=?,
                height=?,
                size=?,
                quality_image=?,
                featured_picture=?,
                valued_image=?,
                timestamp=?
            WHERE pageid=?""" % MediaCollection.COLLECTIONS_TABLE
        fields = list(media.totuple())
        fields.append(fields[0])
        fields.remove(fields[0])
        fields = tuple(fields)  # generate tuple with pageid as last element
        self.cursor.execute(update_query, fields)
        self.connection.commit()

    def insert(self, media):
        """ Inserting a media into the database. """
        insert_query = """INSERT INTO %s VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """ % MediaCollection.COLLECTIONS_TABLE
        self.cursor.execute(insert_query, media.totuple())
        self.connection.commit()

    def listall(self):
        """ List all elements of the collection. """
        list_query = """SELECT * FROM %s""" % MediaCollection.COLLECTIONS_TABLE
        self.cursor.execute(list_query)
        return [Media.fromtuple(media) for media in self.cursor.fetchall()]

    def reset(self):
        """ Delete all entry in the database. """
        reset_query = "DELETE * FROM %s" % MediaCollection.COLLECTIONS_TABLE
        self.cursor.execute(reset_query)
