import logging
import xml.etree.ElementTree as ElementTree

class Utils:
    trajectory_line_color = (0, 255, 0)
    trajectory_line_thickness = 2

    def getBottomCentroid(self, bbox):
        try:
            return (int(bbox[0]) + int(bbox[2])) // 2, (int(bbox[3]) + int(bbox[3])) // 2
        except Exception as e:
            logging.error(e, exc_info=True)
