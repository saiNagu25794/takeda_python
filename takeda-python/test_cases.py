
from regex import get_disease_value_with_regex, get_drug_study_value_with_regex


def check_attribute_value_with_regex(drug_names_list: list, medical_Conditions_list : list, Attribute_value : str, Actual_mapped_value : str):

    if Attribute_value == "Disease":
        get_disease_value_with_regex(drug_names_list, medical_Conditions_list, Actual_mapped_value)
    elif Attribute_value == "Drug Study":
        response = get_drug_study_value_with_regex(drug_names_list, medical_Conditions_list, Actual_mapped_value)
        return response


