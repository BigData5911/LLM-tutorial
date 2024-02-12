
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_experimental.tabular_synthetic_data.openai import (
  OPENAI_TEMPLATE,
  create_openai_data_generator
)

from langchain_experimental.tabular_synthetic_data.prompts import (
  SYNTHETIC_FEW_SHOT_PREFIX,
  SYNTHETIC_FEW_SHOT_SUFFIX
)

from langchain_openai import ChatOpenAI

class MedicalBilling:
  patient_id: int
  patient_name: str
  diagnosis_code: str
  procedure_code: str
  total_charge: float
  insurance_clain_amount: float

examples = [
    {
        "example": """Patient ID: 123456, Patient Name: John Doe, Diagnosis Code: 
        J20.9, Procedure Code: 99203, Total Charge: $500, Insurance Claim Amount: $350"""
    },
    {
        "example": """Patient ID: 789012, Patient Name: Johnson Smith, Diagnosis 
        Code: M54.5, Procedure Code: 99213, Total Charge: $150, Insurance Claim Amount: $120"""
    },
    {
        "example": """Patient ID: 345678, Patient Name: Emily Stone, Diagnosis Code: 
        E11.9, Procedure Code: 99214, Total Charge: $300, Insurance Claim Amount: $250"""
    },
]

OPENAI_TEMPLATE = PromptTemplate(input_variables=["example"], template="{example}")

prompt_template = FewShotPromptTemplate(
  examples=examples,
  suffix=SYNTHETIC_FEW_SHOT_SUFFIX,
  prefix=SYNTHETIC_FEW_SHOT_PREFIX,
  input_variables=["subject", "extra"],
  example_prompt=OPENAI_TEMPLATE
)

synthetic_data_generator = create_openai_data_generator(
  output_schema=MedicalBilling,
  llm=ChatOpenAI("gpt-3.5-turbo", temperature=1),
  prompt=prompt_template
)

synthetic_results = synthetic_data_generator(
  subject="medical_billing",
  extra="the name must be chosen at random. Make it something you wouldn't normally choose.",
  runs=10,
)