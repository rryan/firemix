import numpy as np

from lib.colors import hls_blend
from lib.transition import Transition

class MaskBlend(Transition):
    """
    This approximates color subtraction for the HLS color space.
    """

    def __init__(self, app):
        Transition.__init__(self, app)
        self._buffer = None

    def __str__(self):
        return "Mask Blend"

    def get(self, start, end, progress, fade_length=0.5):
        
        start_transpose = start.T
        end_transpose = end.T

        # lums = start_transpose[1].clip(0,1)
        lums = start_transpose[1]
        hues = end_transpose[0]
        sats = end_transpose[2]

        self.frame = np.asarray([hues, lums, sats]).T
        
#         if np.random.random() > 0.95:
#             print "lums", lums
#             print "hues", hues
#             print "sats", sats

        return self.frame
