import xml.etree.ElementTree as et


def parse_file(file):
    data = {}
    tree = et.parse(file)
    root = tree.getroot()
    for child in root:
        values = []
        print(child.attrib['id'])
        for subchild in child:
            print(subchild.tag, subchild.attrib)
            values.append(subchild.attrib['v'])
        data[child.attrib['id']] = values
        print('End of subchild')
    return data