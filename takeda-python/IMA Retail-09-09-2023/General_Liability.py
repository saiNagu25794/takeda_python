import pandas as pd


general_liability_dict = {
    "Carrier": "",
    "Named Insured": "Insured Name",
    "General Aggregate": "",
    "Products Aggregate": "",
    "Each Occurrence": "",
    "Personal and Advertising Injury": "",
    "Damage to Premises Rented To You": "",
    "Medical Expense,  Any One Person": "Medical Expense Any One Person",
    "Employee Benefits Liability Each Wrongful Act or Series of Acts": "",
    "Employee Benefits Liability Each Annual Aggregate": "",
    "Liquor Liability Each Common Cause": "",
    "Liquor Liability General Aggregate": "",
    "Policy Deductible": "",
    "Employee Benefits Liability Deductible": "",
    "Liquor Liability Deductible": "",
    "Additional Insured - Designated Person or Organization": "",
    "Aggregate Limit Applies Per": "",
    "Bodily Injury Includes Mental Anguish": "",
    "Fellow Employee Exclusion Deleted": "",
    "Additional Insured - Users of Golfmobiles": "",
    "Waiver of Subrogation": "",
    "Broad Form Named Insured": "",
    "Knowledge of Occurrence": "",
    "Unintentional E&O": "Unintentional E and O",
    "Extended BI and PD - Reasonable Force": "",
    "Pollution Exclusion": "",
    "Pollution Enhancement for Hospitality": "",
    "Exclusion - Mechanical Rides & Slides": "Exclusion - Mechanical Rides and Slides",
    "Primary Non-Contributory For Additional Insureds": "",
    "Notice of Cancellation to Third Parties - 30 Days": "",
    "Employee Benefits Retro Date": "",
    "Annual Premium": "",
    "Limits": "",
    "Additional Insured": "Additional Insured Value",
    "Total Revenue - Flour Milling": "",
    "General Liability Deductible": "",
    "Terrorism": "",
    "Policy Form": "",
    "Medical Payments": "",
    "Sexual Abuse & Molestation": "Sexual Abuse and Molestation Text",
    "Professional Liability": "",
    "Employment Related Practices": "",
    "Intellectual Property": "",
    "Communicable Disease": "",
    "Auditable": "",
    "Notice of cancellation or non-renewal 90 days except 10 days non-payment": "",
    "HVAC Carveback": "",
    "SAM - Claims-Made Coverage": "",
    "Sexual Abuse and Molestation Aggregate Limit": "",
    "Sexual Abuse and Molestation Deductible Each Claim": ""

}
def read_excel(input_file):
    df = pd.DataFrame(general_liability_dict.keys(), columns = ['General Liability Report Items'])







if __name__ == "__main__":
    input_file = r"C:\Users\rrguest.RR-ITS\Documents\IMA Retail-09-09-2023\IMA Retail\Input Excels\General Liability_preview.xlsx"
    output_file = ""
    read_excel(input_file)