from output_data.expected_values_with_regex import regex_expressions, content_expressions


def get_all_the_values_from_document(xml_data):
    content_dict = {}
    x_path = "//pr:Project/pr:DocumentId"
    values = xml_data.xpath(x_path, namespaces=xml_data.nsmap)
    if values:
        extracted_content = values[0].text.split()
        content_dict["Record ID"] = ""
        content_dict["Record External ID"] = ""
        content_dict["Record External Source"] = ""
        content_dict['Study Name'] = next(
            (item for item in extracted_content if content_expressions['study_name_pattern'].match(item)), "")
        content_dict['Consent Type'] = ' '.join(extracted_content[:2]) if content_expressions[
                                                                              'consent_type_pattern'].match(
            extracted_content[0]) and content_expressions['consent_type_pattern'].match(extracted_content[1]) else ""
        content_dict["Country"] = next(
            (item for item in extracted_content if content_expressions['country_pattern'].match(item)), "USA")
        content_dict["site"] = next(
            (item for item in extracted_content if content_expressions['site_pattern'].match(item)), "Master")
        content_dict["Protocol Amendment Number"] = 0
        content_dict["ICF Version Number"] = 0
        for item in extracted_content:
            match = content_expressions['effective_start_date_pattern'].match(item)
            if match:
                year, month, day = match.group(0).split('.')
                content_dict["Effective Start Date"] = f"{month}-{day}-{year}"
                break
        content_dict["Sample Tracking Code"] = "ICF"
    return content_dict


def check_attribute_value_with_regex(heading, value):
    # print(heading, value)
    if value is None:
        if heading in regex_expressions:
            if "Silent" in regex_expressions[heading]:
                return "Silent"
            else:
                return "Not Applicable"

    if heading in regex_expressions:
        for expected_value, pattern in regex_expressions[heading].items():
            if pattern != "":
                if pattern.search(value):
                    return expected_value

    return "Unknown"
