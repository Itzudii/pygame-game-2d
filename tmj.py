import xml.etree.ElementTree as ET
import json


def xml_to_dict(element):
    data = {}

    # Add attributes
    if element.attrib:
        data.update(element.attrib)

    # Add text if exists
    text = (element.text or "").strip()
    if text:
        data["text"] = text

    # Add child elements
    children = list(element)
    if children:
        child_dict = {}

        for child in children:
            child_data = xml_to_dict(child)

            if child.tag in child_dict:
                if not isinstance(child_dict[child.tag], list):
                    child_dict[child.tag] = [child_dict[child.tag]]
                child_dict[child.tag].append(child_data)
            else:
                child_dict[child.tag] = child_data

        data.update(child_dict)

    return data


def tsx_to_json(tsx_file, json_file=None):
    tree = ET.parse(tsx_file)
    root = tree.getroot()

    result = {
        root.tag: xml_to_dict(root)
    }

    if json_file:
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)

    return result


    
def fetch_data(tmj_file:str)->dict:
    with open(tmj_file,'r') as f:
        raw = f.read()

    data = json.loads(raw)

    tilesets = data['tilesets']

    imgs = []
    for tileset in tilesets:    
        fg = tileset['firstgid']
        src = tileset['source']

        dat = tsx_to_json(src)
        if dat['tileset'].get('image'):
            img = dat['tileset'].get('image')
            img['firstgid'] = fg
            img['lastgid'] = int(fg)+int(dat['tileset'].get('tilecount'))
            imgs.append(img)
        else:
            tiles = dat['tileset'].get('tile')
            for tile in tiles:
                id = tile['id']
                img = tile['image']
                img['id'] = id
                img['gid'] = int(fg)+int(id)
                objg = tile.get('objectgroup')
                if objg:
                    obj = objg.get('object')
                    img['rect'] = obj
                imgs.append(img)

    data['tilesets'] = imgs
    return data

