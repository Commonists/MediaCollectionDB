""" Metrics module provide metrics for the Media Collections. """


class MediaCollectionsMetrics(object):

    """ Media Collections Metrics.

    Attributes:
            collections (list): list of MediaCollections
    """

    def __init__(self, collections):
        """ Constructor. """
        self.collections = collections

    def listall(self):
        """ List allmedia Media objects from the list of Media Collections. """
        allmedia = []
        for collection in self.collections:
            allmedia.append(collection.listall())
        return allmedia

    def mediacount(self):
        """ Return the mediacount metric. """
        return len(self.listall())

    def qicount(self):
        """ Return the qicount metric which represents the amount of 
        quality images in the set of collection."""
        qualityimages = [qi for qi in self.listall() if qi.quality_image]
        return len(qualityimages)
