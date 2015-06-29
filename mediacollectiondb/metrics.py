"""Metrics module provide metrics for the Media Collections."""


class MediaCollectionsMetrics(object):

    """Media Collections Metrics.

    Attributes:
        collections (list): list of MediaCollections
        cache_allmedia (list): cache list of all the media.Media from
            collections. None until cache is filled.
    """

    def __init__(self, collections):
        """Constructor.

        Args:
            collections (list): list of MediaCollections
        """
        self.collections = collections
        self.cache_allmedia = None

    def listall(self):
        """List all Media objects from the media collections."""
        if self.cache_allmedia is None:
            self.cache_allmedia = []
            for collection in self.collections:
                self.cache_allmedia.extend(collection.listall())
        # else returns the cache value
        return self.cache_allmedia

    def mediacount(self):
        """Count of media in the collections."""
        return len(self.listall())

    def qicount(self):
        """Amount of quality images in the set of collections."""
        qualityimages = [qi for qi in self.listall() if qi.quality_image]
        return len(qualityimages)

    def vicount(self):
        """Amount of valued images in the set of collections."""
        valuedimages = [vi for vi in self.listall() if vi.valued_image]
        return len(valuedimages)

    def fpcount(self):
        """Amount of featured pictures in the set of collections."""
        featuredpictures = [fp for fp in self.listall() if fp.featured_picture]
        return len(featuredpictures)

    def widthcount(self, width):
        """Amount of pictures with a wider border greater than minimal width.

        Args:
            width (int): minimal width.

        Returns:
            int: amount of picture with a wider border greater than minimal
                width
        """
        widthimages = [img for img in self.listall()
                       if img.width >= width or img.height >= width]
        return len(widthimages)

    def pixelcount(self):
        """Amount of pixels within all media collections."""
        return sum([img.size for img in self.listall()])

    def qualitypixelcount(self):
        """Amount of pixels from quality images in all media collections."""
        return sum([img.size for img in self.listall() if img.quality_image])
