def is_value_in_list(value, lst):
    value = value.strip()  # Remove leading and trailing spaces
    for item in lst:
        if value == item.strip():  # Check if the stripped value matches the stripped item
            return True
    return False

# Define the output value and the input list
output_value = "The blood samples for PK and immunogenicity will be stored at Takeda Development Center Americas, Inc., its agents or its affiliated companies for up to 15 years from when the study results are reported or if less, the maximum period permitted under applicable law or until your consent is withdrawn. After that time, the samples will be destroyed       2.5"
input_list = ['Your blood samples collected for PK and immunogenicity will be stored at TDC Americas, Inc., its agents, or its affiliated companies for up to 15 years from when the study results are reported or, if less than 15 years, the maximum amount of time allowed under applicable laws or until your consent is withdrawn (removed). After that time, the samples will be destroyed.', 'The blood samples for PK and immunogenicity will be stored at Takeda Development Centre Americas, Inc., its agents or its affiliated companies for up to 15 years from when the study results are reported or if less, the maximum period permitted under applicable law or until your consent is withdrawn. After that time, the samples will be destroyed 2.5.', 'However, the blood samples for PK and immunogenicity will be stored at Takeda Development Center Americas, Inc.( 95 Hayden Avenue, Lexington, MA 02421,USA), its agents or its affiliated companies for up to 15 years from when the study results are reported or if less, the maximum period permitted under applicable law or until your consent is withdrawn. After that time, the samples will be destroyed.', 'The Sponsor will keep your samples for up to 15 years from the end of the study, unless there are local laws which require a shorter storage period, or you withdraw consent. After that time, the samples will be destroyed.', 'However, the blood, cheek swab, and tumor tissue samples collected for the biomarker research part of this study will be stored at the Sponsor’s designated location or its affiliated companies, for up to 15 years from when the study results are reported or if less, the maximum period permitted under applicable law. After that time, the samples will be destroyed.', 'However, the blood and CSF sample(s) collected for the biomarker research part of this study will be stored at Takeda Development Center Americas, Inc., its agents or its affiliated companies for up to 15 years from when the study results are reported or if less, the maximum period permitted under applicable law or until consent is withdrawn.', 'Your blood samples will be held for up to 15 years after the end of the research study.']

# Check if the value is in the list
if is_value_in_list(output_value, input_list):
    print("Value found in the list.")
else:
    print("Value not found in the list.")