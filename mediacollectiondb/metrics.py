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
