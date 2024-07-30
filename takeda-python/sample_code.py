from lxml import etree as ET

def extract_text_from_xml(xml_path, xpath):
    parser = ET.XMLParser(remove_comments= True)
    tree = ET.parse(xml_path, parser = parser)
    metadata_response = tree.xpath(xpath, namespaces={'xhtml': 'http://www.w3.org/1999/xhtml', 'dg':"http://www.docugami.com/2021/dgml"})
    return metadata_response

def extract_text_from_elements(elements):
    json_response = dict()
    for i, elem in enumerate(elements, start=1):
        text_content = ''.join(elem.itertext()).strip()
        json_response[i] = text_content
    return json_response



if __name__ == "__main__":
    xml_path = "Docs/document-dgml.xml"
    # search_text = input("Enter search text: ")
    xpath = f"//xhtml:td[dg:chunk[contains(text(), 'Class I: Diagnostic & Preventive')]]"
    elements = extract_text_from_xml(xml_path, xpath)
    json_data = extract_text_from_elements(elements)
    print(json_data)









