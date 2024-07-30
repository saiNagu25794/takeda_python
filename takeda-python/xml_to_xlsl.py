import os
import pandas as pd
from lxml import etree


def read_xml_data(xml_file):
    with open(xml_file, 'r', encoding='utf-8') as file:
        xml_data = file.read()
    return xml_data


def extract_values(xml_data):
    root = etree.fromstring(xml_data)
    namespace = {
        'pr': 'http://www.docugami.com/2021/dgml/project',
        'docset': 'http://www.docugami.com/2021/dgml/Takeda(TEST)/FinalTest',  # Update with actual URI
        'dg': 'http://www.docugami.com/2021/dgml',
        'dgm': 'http://www.docugami.com/2021/dgml/docugami/medical',
        'dgc': 'http://www.docugami.com/2021/dgml/docugami/contracts',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xhtml': 'http://www.w3.org/1999/xhtml'
    }
    entries_xpath = "//pr:Entries/pr:Entry"
    entries = root.xpath(entries_xpath, namespaces=namespace)
    data = []
    for entry in entries:
        heading_element = entry.find('pr:Heading', namespaces=namespace)
        value_element = entry.find('pr:Value/*', namespaces=namespace)
        heading = heading_element.text if heading_element is not None else None
        value = ''.join(value_element.itertext()).strip() if value_element is not None else None
        data.append((heading, value))
    return data


def get_report_values_files(root_directory):
    report_files = []
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file == 'report-values.xml':
                report_files.append(os.path.join(root, file))
    return report_files


def parse_xml(xml_file, parent_folder_name):
    xml_data = read_xml_data(xml_file)
    values = extract_values(xml_data)
    data = [(parent_folder_name, heading, value) for heading, value in values]
    return data


def store_all_the_data(report_files):
    all_data = []
    for xml_file in report_files:
        parent_folder_name = os.path.basename(os.path.dirname(os.path.dirname(xml_file)))
        file_data = parse_xml(xml_file, parent_folder_name)
        all_data.extend(file_data)
    return all_data


def save_to_excel(data, output_path):
    df = pd.DataFrame(data, columns=['File name', 'Attribute', 'Actual Mapped Value'])
    df.to_excel(output_path, index=False)


if __name__ == "__main__":
    root_directory = 'C:\\Users\\rrguest.RR-ITS\\Desktop\\Takeda\\ICF Export (1)'
    report_files = get_report_values_files(root_directory)
    all_data = store_all_the_data(report_files)
    output_path = os.path.join(root_directory, 'report-output.xlsx')
    save_to_excel(all_data, output_path)
