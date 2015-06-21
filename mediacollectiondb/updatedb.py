"""updatedb module allows you to update a media collection database."""

import logging
import time

import mwclient

import media

DEFAULT_DB_FILE = 'category.db'

COMMONS_SITE_URL = 'commons.wikimedia.org'
COMMONS_PROTOCOL = 'https'
COMMONS_DEFAULT_CATEGORY = 'Images supported by Wikimedia France - Lutz'

COMMONS_QI_CATEGORY = 'Category:Quality images'
COMMONS_FP_CATEGORY = 'Category:Featured pictures on Wikimedia Commons'
COMMONS_VI_CATEGORY = 'Category:Valued images sorted by promotion date'

DEFAULT_DB_FILE = 'category.db'


def updatecategory(mediadatabase, category):
    """Add media from a category to a database.

    Args:
        mediadatabase (media.MediaCollection): database to save media
        category (str): category to update
    """
    site = mwclient.Site((COMMONS_PROTOCOL, COMMONS_SITE_URL))
    images = [img for img in site.Categories[category]]
    logging.debug("%d images in category %s", len(images), category)
    for img in images:
        image = make_media(img)
        mediadatabase.save(image)


def make_media(img):
    """Create a media from an API image information.

    Args:
        img (?): image information obtained from the API
    """
    info = img.imageinfo
    image = media.Media(img._info['pageid'],
                        img.name,
                        width=info['width'],
                        height=info['height'],
                        size=info['width'] * info['height'])
    cats = [cat for cat in img.categories()]
    revs = [rev for rev in img.revisions()]
    # upload date and uploader
    first_revision = revs[-1]
    image.uploader = first_revision['user']
    # qi/fp/vi
    for cat in cats:
        if cat.name == COMMONS_QI_CATEGORY:
            image.quality_image = True
        if cat.name == COMMONS_FP_CATEGORY:
            image.featured_picture = True
        if cat.name == COMMONS_VI_CATEGORY:
            image.valued_image = True
    return image


def main():
    """Main function of the updatedb module."""
    from argparse import ArgumentParser
    start_time = time.time()
    description = "MediaCollectionDB update script."
    parser = ArgumentParser(description=description)
    parser.add_argument("-c", "--category",
                        type=str,
                        dest="category",
                        required=False,
                        default=COMMONS_DEFAULT_CATEGORY,
                        help="Media Category")
    parser.add_argument("-f", "--file",
                        type=str,
                        dest="file",
                        require=False,
                        default=DEFAULT_DB_FILE,
                        help="Database file, default: category.db")
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument("-v",
                                 action="count",
                                 dest="verbose",
                                 default=1,
                                 help="Verbosity level. -v for DEBUG")
    verbosity_group.add_argument("-q", "--quiet",
                                 action="store_const",
                                 dest="verbose",
                                 const=0,
                                 help="To silence the INFO messages")
    args = parser.parse_args()
    logging_map = {0: logging.WARNING,
                   1: logging.INFO,
                   2: logging.DEBUG}
    logging_level = logging_map.get(args.verbose, logging.DEBUG)
    logging.basicConfig(level=logging_level)
    logging.info("Starting")
    mediadatabase = media.MediaCollection(args.dbfile)
    updatecategory(mediadatabase, args.category)
    logging.info("--- Ended in %s seconds", (time.time() - start_time))

if __name__ == '__main__':
    main()
