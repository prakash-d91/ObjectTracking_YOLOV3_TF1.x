import logging
import xml.etree.ElementTree as ElementTree
import time
from datetime import datetime

class Utils:
    trajectory_line_color = (0, 255, 0)
    trajectory_line_thickness = 2

    def getBottomCentroid(self, bbox):
        try:
            return (int(bbox[0]) + int(bbox[2])) // 2, (int(bbox[3]) + int(bbox[3])) // 2
        except Exception as e:
            logging.error(e, exc_info=True)

    def create_ONVIF(self, objects):
        FlexCameraNumber = 1
        StreamSource = "192.168.101.240/live/camera1/stream1"

        # ONVIF Creation
        root_node = ElementTree.Element("tt:MetadataStream")
        root_node.attrib['xmlns:tt'] = "http://www.onvif.org/ver10/schema"

        node_va = ElementTree.SubElement(root_node, 'tt:VideoAnalytics')
        node_frame = ElementTree.SubElement(node_va, 'tt:Frame')

        # need to change
        timestamp = datetime.now().timestamp()

        node_frame.attrib['UtcTime'] = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(timestamp))
        for i in range(len(objects)):
            node_Object = ElementTree.SubElement(node_frame, 'tt:Object')
            node_Object.attrib['ObjectID'] = str(objects[i]['id'])

            node_appearance = ElementTree.SubElement(node_Object, 'tt:Appearance')
            node_shape = ElementTree.SubElement(node_appearance, 'tt:Shape')

            node_BoundaryBox = ElementTree.SubElement(node_shape, 'tt:BoundingBox')
            node_BoundaryBox.attrib['left'] = str(objects[i]['bbox'][0])
            node_BoundaryBox.attrib['top'] = str(objects[i]['bbox'][1])
            node_BoundaryBox.attrib['right'] = str(objects[i]['bbox'][2])
            node_BoundaryBox.attrib['bottom'] = str(objects[i]['bbox'][3])

            node_COG = ElementTree.SubElement(node_shape, 'tt:CenterOfGravity')
            node_COG.attrib['x'] = str(objects[i]['center_of_gravity'][0])
            node_COG.attrib['y'] = str(objects[i]['center_of_gravity'][1])

            node_class = ElementTree.SubElement(node_appearance, 'tt:Class')
            node_type = ElementTree.SubElement(node_class, 'tt:Type')
            node_type.attrib['Likelihood'] = str(objects[i]['confidence'])
            node_type.text = str(objects[i]['type'])

            node_Extension = ElementTree.SubElement(node_Object, 'tt:Extension')

            node_Path = ElementTree.SubElement(node_Extension, 'tt:Path')
            node_Path.text = '[]'

        node_Extension = ElementTree.SubElement(node_frame, 'tt:Extension')

        node_SimpleItem = ElementTree.SubElement(node_Extension, 'tt:SimpleItem')
        node_SimpleItem.attrib['Name'] = "StreamSource"
        node_SimpleItem.attrib['Value'] = str(StreamSource)

        print((ElementTree.tostring(root_node, encoding='unicode', method='xml')))

        filename = "DT_Frame_" + str(datetime.now().strftime("%d.%m.%Y_%H%M%S")) + ".xml"
        with open(filename, "w") as f:
            f.write((ElementTree.tostring(root_node, encoding='unicode', method='xml')))

