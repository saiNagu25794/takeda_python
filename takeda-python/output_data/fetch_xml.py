import re
from output_data.fetch_data_regex import check_attribute_value_with_regex, get_all_the_values_from_document
from output_data.attribute_values_dict import allowed_headings


def create_entry(content_data, attribute, expected_value):
    return (
        content_data["Record ID"], content_data["Record External ID"], content_data["Record External Source"],
        content_data["Study Name"], content_data["Consent Type"], content_data["Country"], content_data["site"],
        content_data["Protocol Amendment Number"], content_data["ICF Version Number"],
        content_data["Effective Start Date"], content_data["Sample Tracking Code"], attribute, expected_value
    )


# Function to normalize headings
def normalize_heading(heading):
    return re.sub(r'[^\w\s-]', '', heading).strip().replace(' - ', ' ')


# Create a mapping of normalized headings to allowed headings
normalized_to_allowed = {normalize_heading(h): h for h in allowed_headings}


def extract_expected_value_for_attribute(xml_data):
    content_data = get_all_the_values_from_document(xml_data)
    namespace = {
        'pr': 'http://www.docugami.com/2021/dgml/project',
        'docset': 'http://www.docugami.com/2021/dgml/Takeda(TEST)/FinalTest',
        'dg': 'http://www.docugami.com/2021/dgml',
        'dgm': 'http://www.docugami.com/2021/dgml/docugami/medical',
        'dgc': 'http://www.docugami.com/2021/dgml/docugami/contracts',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xhtml': 'http://www.w3.org/1999/xhtml'
    }
    entries_xpath = "//pr:Entries/pr:Entry"
    entries = xml_data.xpath(entries_xpath, namespaces=namespace)

    # Create an empty dictionary to store the data
    entry_data = {heading: "N/A" for heading in allowed_headings}

    # Default values for entries not found in XML
    default_values = [
        ("Informed Consent Type", "Main Study"),
        ("Duration", "15"),
        ("Based On Date", "Study Closure Date"),
        ("Program", "Program Under Study Only")
    ]

    docugami_values = [(attribute, "") for attribute, _ in default_values]

    # Iterate over the entries
    for entry in entries:
        heading_element = entry.find('pr:Heading', namespaces=namespace)
        value_element = entry.find('pr:Value/*', namespaces=namespace)
        heading = heading_element.text if heading_element is not None else None

        # Normalize heading for comparison
        normalized_heading = normalize_heading(heading) if heading is not None else None

        # extract the value for the heading
        value = ''.join(value_element.itertext()).strip()
        value = None if value == '' else value

        # store the data for Docugami excel
        docugami_values.append((heading, value))
        # Check if normalized heading is in the allowed list

        if normalized_heading in normalized_to_allowed:
            allowed_heading = normalized_to_allowed[normalized_heading]
            expected_value = check_attribute_value_with_regex(normalized_heading, value)
            entry_data[allowed_heading] = expected_value
        else:
            if heading in ["Data Storage Duration Main Study", "Data Storage Duration Future Research"]:
                normalised_heading = "Data Storage Duration"
                expected_value = check_attribute_value_with_regex(normalised_heading, value)
                entry_data[normalised_heading] = expected_value
            else:
                heading = "Copy of ICF"
                expected_value = "Attached"
                entry_data[heading] = expected_value

    main_samples = []

    for attribute, default_value in default_values:
        entry_data[attribute] = default_value

    for heading in allowed_headings:
        result_value = entry_data[heading]
        main_samples.append(create_entry(content_data, heading, result_value))

    return main_samples, docugami_values
