""" Metrics module provide metrics for the Media Collections. """


class MediaCollectionsMetrics(object):

    """ Media Collections Metrics.

    Attributes:
            collections (list): list of MediaCollections
    """

    def __init__(self, collections):
        """ Constructor. """
        self.collections = collections
        self.cache_allmedia = None

    def listall(self):
        """ List allmedia Media objects from the list of the set
        of media collections. """
        if self.cache_allmedia is None:
            self.cache_allmedia = []
            for collection in self.collections:
                self.cache_allmedia.append(collection.listall())
        # else returns the cache value
        return self.cache_allmedia

    def mediacount(self):
        """ Return the mediacount metric. """
        return len(self.listall())

    def qicount(self):
        """ Return the qicount metric which represents the amount of
        quality images in the set of collections."""
        qualityimages = [qi for qi in self.listall() if qi.quality_image]
        return len(qualityimages)

    def vicount(self):
        """ Return the vicount metric which counts the amount of valued images
        in the set of collections. """
        valuedimages = [vi for vi in self.listall() if vi.valued_images]
        return len(valuedimages)
