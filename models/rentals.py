from pydantic import BaseModel, field_validator, model_validator


class RentalOutcome(BaseModel):
    bike_id: int
    user_id: int
    bike_battery: int

    @field_validator("bike_battery")
    @classmethod
    def battery_must_be_sufficient(cls, v: int) -> int:
        if v < 20:
            raise ValueError("Cannot create rental: bike has less than 20% battery.")
        return v


class RentalProcessing(BaseModel):
    bike_id: int
    bike_battery: int
    user_id: int

    @model_validator(mode="after")
    def check_battery_level(self):
        if self.bike_battery < 20:
            raise ValueError("Bike battery too low for rental.")
        return self
