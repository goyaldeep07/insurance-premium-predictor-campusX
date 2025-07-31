from pydantic import Field, BaseModel, computed_field, field_validator
from typing import Literal, Annotated
from config.city_tier import tier_1_cities, tier_2_cities


# pydantic model to validate input data
class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, description="Age of the User")]
    weight: Annotated[float, Field(..., gt=0, description="weight in Kgs")]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description="height in mts")]
    income_lpa: Annotated[float, Field(..., gt=0, description="Annual salary in LPA")]
    smoker: Annotated[bool, Field(..., description="Is a smoker?")]
    city: Annotated[str, Field(..., description="city user belongs to")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
                                  'business_owner', 'unemployed', 'private_job'], Field(...,
                                                                                        description="occupation of the user")]

    @field_validator('city')
    def validate_city(cls, v):
        v = v.strip().title()  # Normalize city name
        return v
    

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker and self.bmi > 27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle-aged"
        else:
            return "Senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3