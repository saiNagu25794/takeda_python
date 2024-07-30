import re

import pandas as pd

from output_data.paths import excel_path


def read_excel(excel_path):
    product_list = []
    disease_list = []
    xls = pd.ExcelFile(excel_path)
    product = pd.read_excel(xls, sheet_name='product')
    if "Drug Names" in product.columns:
        product_list = product['Drug Names'].unique().tolist()

    medical_conditions = pd.read_excel(xls, sheet_name="medical-conditions")
    if 'Medical Condition' in medical_conditions.columns:
        disease_list = medical_conditions["Medical Condition"].unique().tolist()

    return product_list, disease_list


# Reading the Excel file and generating the lists
product_list, disease_list = read_excel(excel_path)


class KeywordLists:
    MedicalConditions = disease_list
    Locations = ["Location1", "Location2"]


def generate_medical_conditions_pattern():
    return "|".join(map(re.escape, KeywordLists.MedicalConditions))


def generate_therapeutic_areas_pattern():
    year_expression_pattern = r"\b\d+\s*years?\b"
    cancer_pattern = r"\bcancer\b|" + "|".join(
        map(re.escape, [mc for mc in KeywordLists.MedicalConditions if "cancer" in mc]))
    return cancer_pattern + "|" + year_expression_pattern


content_expressions = {
    'study_name_pattern': re.compile(r'(TAK-\d{3,}-\d{4}|MLN\d{4}[A-Z]*-\d{4})'),
    'country_pattern': re.compile(r'(Germany|Israel|China|Taiwan|Hungary|Korea|Russia|Poland|Japan|France)'),
    'site_pattern': re.compile(r'\d{5}'),
    'consent_type_pattern': re.compile(r'^Main$|^Study$'),
    'effective_start_date_pattern': re.compile(r'\d{4}\.\d{2}\.\d{2}')
}

regex_expressions = {

    "Disease": {
        "Therapeutic Area Restricted": re.compile(r"\b(?:" + generate_therapeutic_areas_pattern() + r")\b",
                                                  re.IGNORECASE),
        "All Diseases Allowed": "",
        "Disease Under Study Restricted": re.compile(r"\b(?:" + generate_medical_conditions_pattern() + r")\b",
                                                     re.IGNORECASE),
        "No Disease Related Research": "",
        "Other - free text": "",
        "Silent": ""
    },

    "Informed Consent Type": {
        "Main Study": re.compile(r'\b(?:main study|main consent)\b', re.IGNORECASE),
        "Mn Stdy Parent Guardian": re.compile(r'\b(?:parent guardian|minor study)\b', re.IGNORECASE),
        "Optional Tissue": re.compile(r'\b(?:optional tissue|optional samples)\b', re.IGNORECASE),
        "Future Research - Samples": re.compile(r'\b(?:future research samples|future sample use)\b', re.IGNORECASE),
        "Future Research - Data": re.compile(r'\b(?:future research data|future data use)\b', re.IGNORECASE),
        "Genomics": re.compile(r'\b(?:genomics|genomic study)\b', re.IGNORECASE),
        "Informed Consent Assent": re.compile(r'\b(?:assent|child assent)\b', re.IGNORECASE)
    },

    "Duration": {
        "15.0": re.compile(r'\b(?:15 years|15.0)\b', re.IGNORECASE),
        "0.0": re.compile(r'\b(?:no duration|0.0)\b', re.IGNORECASE),
        "5.0": re.compile(r'\b(?:5 years|5.0)\b', re.IGNORECASE),
        "10.0": re.compile(r'\b(?:10 years|10.0)\b', re.IGNORECASE)

    },

    "Based On Date": {
        "Study Closure Date": re.compile(r'\b(?:study closure date|end of study)\b', re.IGNORECASE),
        "Collection Date": re.compile(r'\b(?:collection date|date of collection)\b', re.IGNORECASE),
        "Last Subject Last Visit": re.compile(r'\b(?:last subject last visit|last visit)\b', re.IGNORECASE)

    },

    "Drug Study": {
        "Drug Under Study Only": re.compile(
            r'\b(?:study medicine|investigational medication|investigational drug|study drug|study treatment|randomization|subcutaneous \(SC\) injection)\b',
            re.IGNORECASE),
        "Drug Under Study, Combination Drug, or Active Comparator": re.compile(
            r'\b(?:other drugs|combination|apremilast|type of cancer|standard treatment|no longer effective|combination with a drug|study medications|radiation treatment|pembrolizumab)\b',
            re.IGNORECASE),
        "No Drug Related Research": re.compile(r'\b(?:no drug related research)\b', re.IGNORECASE),
        "Other - free text": re.compile(r'\b(?:other)\b', re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE)
    },

    "Program": {
        "Protocol Under Study Only": re.compile(r'\b(?:protocol under study only|current protocol)\b', re.IGNORECASE),
        "All Programs Allowed": re.compile(r'\b(?:all programs allowed|all protocols)\b', re.IGNORECASE),
        "Program Under Study Only": re.compile(r'\b(?:program under study only)\b', re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE)
    },

    "Long Term Sample Storage": {
        "No": re.compile(r'\b(?:no)\b', re.IGNORECASE),
        "Yes": re.compile(r'\b(?:yes)\b', re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE)
    },

    "Future Research for Samples": {
        "Disclosed": re.compile(r'\b(?:disclosed|future study)\b', re.IGNORECASE),
        "Specific Consent Checkbox or Signature": re.compile(r'\b(?:specific consent|checkbox|signature|I agree)\b',
                                                             re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE),
        "Restricted": re.compile(r'\b(?:restricted)\b', re.IGNORECASE)
    },

    "Future Research for Samples Allowable Use": {
        "Disease Related Only": re.compile(r'\b(?:disease related only)\b', re.IGNORECASE),
        "Disease and Study Drug Related Only": re.compile(
            r'\b(?:future research related to|related diseases|study drug|diseases related to this study|effects of the study drug)\b',
            re.IGNORECASE),
        "Unrestricted": re.compile(
            r'\b(?:advance medical science|improve patient care|future scientific research|diseases, conditions or drugs|not be included in this study)\b',
            re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE)
    },

    "Genetic Studies Explanation": {
        "WGS Disclosed": re.compile(
            r'\b(?:whole genome sequencing|genetic sequencing|entire genetic makeup|ordering of genes|very thorough way to learn about genes)\b',
            re.IGNORECASE),
        "Specific Mutation(s) Disclosed": re.compile(
            r'\b(?:specific mutations|identify and confirm biomarkers|blood sample for genetic \(DNA\)|deoxyribonucleic acid, or DNA|genes are pieces of DNA|The genetic testing is done)\b',
            re.IGNORECASE),
        "Disclosed": re.compile(
            r'\b(?:genetic analysis|research purposes only|not a medical test|medical importance of the results|tests will be performed in a research laboratory|not applicable to your medical care|research tests|minimize the possibility for the results from this research being linked to you)\b',
            re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE),
        "Not Applicable": re.compile(r'\b(?:not applicable)\b', re.IGNORECASE),
    },

    "Genetic or Genomic Studies Explanation": {
        "WGS Disclosed": re.compile(
            r'\b(?:whole genome sequencing|genetic sequencing|entire genetic makeup|ordering of genes|very thorough way to learn about genes)\b',
            re.IGNORECASE),
        "Specific Mutation(s) Disclosed": re.compile(
            r'\b(?:specific mutations|identify and confirm biomarkers|blood sample for genetic \(DNA\)|deoxyribonucleic acid, or DNA|genes are pieces of DNA|The genetic testing is done)\b',
            re.IGNORECASE),
        "Disclosed": re.compile(
            r'\b(?:genetic analysis|research purposes only|not a medical test|medical importance of the results|tests will be performed in a research laboratory|not applicable to your medical care|research tests|minimize the possibility for the results from this research being linked to you)\b',
            re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE),
        "Not Applicable": re.compile(r'\b(?:not applicable)\b', re.IGNORECASE)

    },

    "Genetic or Genomic Research Risk": {
        "Genetic Risk Disclosed": re.compile(
            r'\b(?:risk of the genetic test|sharing genetic information|identifying genetic changes|risk that information gained from genetic research|re-identification of the information|genetic study may influence insurance companies|negative impact or unintended consequences on family or other relationships|genetic traits might come to be associated with a particular race, ethnicity, sex or gender)\b',
            re.IGNORECASE),
        "Whole Genome Sequencing Risk Disclosed": re.compile(
            r'\b(?:genetic information|genetic material purified from your blood|genetic test results from this study are confidential|an reveal personal things about you)\b',
            re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE),
        "Not Applicable": re.compile(r'\b(?:not applicable)\b', re.IGNORECASE)

    },

    "Genetic Research Risk": {
        "Genetic Risk Disclosed": re.compile(
            r'\b(?:risk of the genetic test|sharing genetic information|identifying genetic changes|risk that information gained from genetic research|re-identification of the information|genetic study may influence insurance companies|negative impact or unintended consequences on family or other relationships|genetic traits might come to be associated with a particular race, ethnicity, sex or gender)\b',
            re.IGNORECASE),
        "Whole Genome Sequencing Risk Disclosed": re.compile(
            r'\b(?:genetic information|genetic material purified from your blood|genetic test results from this study are confidential|an reveal personal things about you)\b',
            re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE),
        "Not Applicable": re.compile(r'\b(?:not applicable)\b', re.IGNORECASE)
    },

    "Specimen Storage Duration Main Study": {
        "Up to 15 Years after end of study": re.compile(r'\b(?:up to 15 years)\b', re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE),
        "End of Study": re.compile(r'\b(?:end of study)\b', re.IGNORECASE),
        "Other - free text": re.compile(r'\b(?:other)\b', re.IGNORECASE)
    },

    "Specimen Storage Duration Future Research": {
        "Up to 15 Years after end of study": re.compile(r'\b(?:up to 15 years)\b', re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE),
        "End of Study": re.compile(r'\b(?:end of study)\b', re.IGNORECASE),
        "Other - free text": re.compile(r'\b(?:other)\b', re.IGNORECASE)
    },

    "Specimen Storage Location Main Study": {
        "Restricted to Country of Collection": "",
        "Free text ( Capture exact name of LTS or central lab storage location)": "",
        "Silent": ""
    },

    "Specimen Storage Location Future Research": {
        "Restricted to Country of Collection": "",
        "Free text ( Capture exact name of LTS or central lab storage location)": "",
        "Silent": ""
    },

    "Specimen Sharing Future Research": {
        "Sponsor and External Collaborators": re.compile(
            r'\b(?:sponsor and external collaborators|agents|affiliated companies|laboratories listed below)\b',
            re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent|may share)\b', re.IGNORECASE),
        "Sponsor Only": re.compile(r'\b(?:sponsor only|sponsor)\b', re.IGNORECASE)

    },

    "Specimen Anonymization": {
        "Anonymized": re.compile(r'\b(?:anonymized)\b', re.IGNORECASE),
        "Coded/Pseudonymized": re.compile(r'\b(?:coded|pseudonymized|labeled with a code|labeled with a unique)\b',
                                          re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE)
    },

    "Specimen Sharing Main Study": {
        "Sponsor and External Collaborators": re.compile(
            r'\b(?:sponsor and external collaborators|agents|affiliated companies|laboratories listed below)\b',
            re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE),
        "Sponsor Only": re.compile(r'\b(?:sponsor only|sponsor)\b', re.IGNORECASE)
    },
    "Code Key Retention Period": {

    },

    "Data Usage": {
        "Sponsor and Study Site Only": re.compile(r'\b(?:sponsor and study site only)\b', re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE),
        "Sponsor, Study Site, External Collaborators": re.compile(
            r'\b(?:sponsor, study site, external collaborators)\b', re.IGNORECASE),
        "Restricted to Country of Collection": re.compile(r'\b(?:restricted to country of collection)\b', re.IGNORECASE)
    },

    "Data Storage Duration": {
        "10 years": re.compile(r'\b(?:10 years)\b', re.IGNORECASE),
        "15 years": re.compile(r'\b(?:15 years)\b', re.IGNORECASE),
        "20 years": re.compile(r'\b(?:20 years)\b', re.IGNORECASE),
        "25 years": re.compile(r'\b(?:25 years)\b', re.IGNORECASE),
        "Other - free text": re.compile(r'\b(?:other)\b', re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE)
    },

    "Data Anonymization": {
        "Anonymized": re.compile(r'\b(?:anonymized)\b', re.IGNORECASE),
        "Coded/Pseudonymized": re.compile(r'\b(?:coded|pseudonymized|code|unique)\b', re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE)
    },

    'Data Sharing Main Study': {
        "Sponsor and External Collaborators": re.compile(
            r'\b(?:sponsor and other companies|authorized representatives|other parties|other companies|business partners|researchers, companies|organization\(s\) outside of the study site|research sponsor|contract research organization\(s\)|independent data and safety monitoring boards|Takeda and other companies)\b',
            re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE),
        "Sponsor Only": re.compile(r'\b(?:sponsor only|sponsor)\b', re.IGNORECASE)
    },

    "Date Storage Duration Future Research": {

    },

    "Sharing of Study Results with Patient Main Study": {
        "Not Allowed": re.compile(
            r'\b(?:not intended to make determinations|no test results will be provided|not put into your medical record)\b',
            re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE),
        "Shared with Study Doctor Only": re.compile(
            r'\b(?:shared with your doctor|provided to your doctor|your study doctor|doctor only|doctor will review)\b',
            re.IGNORECASE),
        "Clinically Relevant Results": re.compile(
            r'\b(?:clinically relevant results|relevant medical information|results important for your health|information related to your health|important for your treatment)\b',
            re.IGNORECASE)
    },

    "Sharing of Study Results with Patient Future Research": {
        "Not Allowed": re.compile(r'\b(?:not allowed|any future research)\b', re.IGNORECASE),
        "Shared with Study Doctor Only": re.compile(r'\b(?:shared with study doctor only)\b', re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE),
        "Clinically Relevant Results": re.compile(r'\b(?:clinically relevant results)\b', re.IGNORECASE)

    },

    "At Consent Withdrawal Samples": {
        "Destroyed, if linked and not used": re.compile(
            r'\b(?:be destroyed|destroyed at any time|destroyed to prevent further analyses|destroyed to prevent further testing|your samples can still be destroyed)\b',
            re.IGNORECASE),
        "Returned, if linked and not used": re.compile(
            r'\b(?:returned|returned to you|returned if not used|returned if linked and not used)\b', re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE)

    },

    "At Consent Withdrawal Data": {
        "No new data from subject will be added to study data but subject data created before withdrawal can still be used": re.compile(
            r'\b(?:no new data|data created before withdrawal|study results or information|keep and use any study results|data prior to your request|not able to have the results removed|may continue to use )\b',
            re.IGNORECASE),
        "Link to patient is removed": re.compile(
            r'\b(?:link to patient is removed|unlink patient data|patient\'s data will be anonymized|de-identified|remove patient link)\b',
            re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE)
    },

    "Pharmacokinetics Collection": {

    },
    "PK Sample Retention": {
        "See Main Study Codification": re.compile(
            r'\b(?:sponsor|sponsor\'s|store the sample\(s\)|stored at|its agents or its affiliated companies|years|leftover blood samples for future research)\b',
            re.IGNORECASE),
        "See PK Codification": re.compile(
            r'\b(?:PK will be destroyed|end of the study|has been analysed|standard clinical tests|standard testing|information has been analyzed|standard clinical tests)\b',
            re.IGNORECASE),
        "Silent": re.compile(r'\b(?:silent)\b', re.IGNORECASE)
    },

    "Copy of ICF": {

    }

}
