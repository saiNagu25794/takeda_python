import pandas as pd

def read_excel_file_and_group_by_attribute(excel_path):
    grouped_values = {}

    df = pd.read_excel(excel_path)
    data = df.to_dict()

    for key, value in data['Attribute'].items():
        attribute = value
        actual_mapped_value = data['Actual Mapped Value'][key]
        expected_value = data['Expected Values'][key]
        if attribute in grouped_values:
            grouped_values[attribute]['Actual Mapped Value'].append(actual_mapped_value)
            grouped_values[attribute]['Expected Values'].append(expected_value)
        else:
            grouped_values[attribute] = {'Actual Mapped Value': [actual_mapped_value], 'Expected Values': [expected_value]}
    return grouped_values


if __name__ == "__main__":
    excel_path = "Takeda-mappings-24 May.xlsx"
    data = read_excel_file_and_group_by_attribute(excel_path)
    print(data)
