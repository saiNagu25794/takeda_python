from lxml import etree
from output_data.fetch_xml import extract_expected_value_for_attribute
import os
from output_data.save_to_excel import save_output_to_excel


def read_xml_data(xml_file):
    try:
        with open(xml_file, 'r', encoding='utf-8') as file:
            xml_data = file.read()
        return xml_data
    except Exception as e:
        print("Error reading XML file:", e)


async def get_report_values_files(root_directory: str, file_name: str):
    report_file_path = None
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file == file_name:
                report_file_path = os.path.join(root, file)
    output_file_path = store_all_the_data(report_file_path, file_name)
    return output_file_path


def parse_xml(xml_file):
    xml_data = read_xml_data(xml_file)
    root = etree.fromstring(xml_data)
    main_samples, docugami_values = extract_expected_value_for_attribute(root)
    return main_samples, docugami_values


def store_all_the_data(report_files, file_name):
    output_file = file_name.split(".")
    output_file_path = os.path.join(os.path.dirname(report_files), "output")
    if not os.path.exists(output_file_path):
        os.makedirs(output_file_path)
    main_samples, docugami_values = parse_xml(report_files)
    output_path = os.path.join(output_file_path, output_file[0] + ".xlsx")
    save_output_to_excel(main_samples, docugami_values, output_path)
    return output_file_path
