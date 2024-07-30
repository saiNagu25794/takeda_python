import os
import pandas as pd

from excel_formatting import apply_conditional_formatting

import warnings
warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)
warnings.filterwarnings("ignore", message="Data Validation extension is not supported and will be removed")

attribute_dict = {

    'At Consent Withdrawal - Data': 'At Consent Withdrawal Data',
    'At Consent Withdrawal - Samples': 'At Consent Withdrawal Samples',
    'Data Storage Duration': 'Data Storage Duration Main Study',
    'Sharing of Study Results with Patient - Main Study': 'Sharing of Study Results with Patient Future Research',
    'Sharing of Study Results with Patient - Future Research': 'Sharing of Study Results with Patient Future Research'
}


def read_excel(file_path, sheet_name):
    excel_output = pd.read_excel(file_path, sheet_name=sheet_name)
    return excel_output




def create_new_excel(output_file_path, input_folder_path, reference_folder_path):
    consolidated_df = pd.DataFrame(columns=['Attribute'])

    attributes_added = False

    for file in os.listdir(input_folder_path):
        print(f"Processing file: {file}")
        if file.endswith('.xlsx'):
            try:
                file_path = os.path.join(input_folder_path, file)

                main_samples = read_excel(file_path, sheet_name='Main samples')
                docugami_attr = read_excel(file_path, sheet_name='Docugami Attributes and Answers')

                docugami_col = f'Docugami Value - {file}'
                reference_col = f"Reference Value - {file.replace('.pdf', '').replace('.docx', '')}"
                redrock_col = f'RedRock Value - {file}'

                consolidated_df[docugami_col] = ""
                consolidated_df[reference_col] = ""
                consolidated_df[redrock_col] = ""

                if not attributes_added:
                    consolidated_df['Attribute'] = main_samples['Attribute']
                    attributes_added = True

                for i, row in consolidated_df.iterrows():
                    attribute = row["Attribute"]
                    if attribute in attribute_dict.keys():
                        mapped_attribute = attribute_dict[attribute]
                    else:
                        mapped_attribute = attribute

                    # docugami values
                    matched_value = docugami_attr.loc[docugami_attr["Attribute"] == mapped_attribute, "DocugamiValue"]
                    if not matched_value.empty:
                        consolidated_df.at[i, docugami_col] = matched_value.values[0]

                    # reference values
                    # reference_file_name = file.replace('.pdf', '').replace('.docx', '')

                    reference_file_path = os.path.join(reference_folder_path, file)

                    if os.path.exists(reference_file_path):
                        reference_values = read_excel(reference_file_path, sheet_name="Main samples")

                        matched_reference_value = reference_values.loc[
                            reference_values["Attribute"] == attribute, "Value"]
                        if not matched_reference_value.empty:
                            consolidated_df.at[i, reference_col] = str(matched_reference_value.values[0])

                    # redrock_values
                    redrock_values = main_samples.loc[main_samples["Attribute"] == attribute, "Value"]
                    if not redrock_values.empty:
                        consolidated_df.at[i, redrock_col] = str(redrock_values.values[0])

            except Exception as e:
                print(f"Error processing file {file}: {str(e)}")

    consolidated_df.to_excel(output_file_path, index=False, sheet_name='Output')
    apply_conditional_formatting(output_file_path, consolidated_df)


if __name__ == '__main__':
    input_folder = r"C:\Users\sparchuri\PycharmProjects\python_code\takeda-comparsion-code\06-27-2024-output-files 1"
    output_file = r"C:\Users\sparchuri\PycharmProjects\python_code\takeda-comparsion-code\output.xlsx"
    reference_folder = r"C:\Users\sparchuri\PycharmProjects\python_code\takeda-comparsion-code\codified-sheets"

    create_new_excel(output_file, input_folder, reference_folder)
