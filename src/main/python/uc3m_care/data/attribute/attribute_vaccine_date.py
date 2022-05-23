"""Class for the attribute Vaccine Date"""
from datetime import datetime
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

# pylint: disable=too-few-public-methods
class VaccineDate(Attribute):
    """Classs for the attribute PhoneNumber"""

    _validation_pattern = r"[0-9]{4}-[0-9]{2}-[0-9]{2}$"
    _validation_error_message = "Vaccine date has an invalid format"

    def _validate(self, attr_value: str) -> float:
        """Validates the age according to the requirements"""
        # Check with regex the dashes
        super()._validate(attr_value)

        # Check the years, months and days
        try:
            vaccine_date = datetime.fromisoformat(attr_value)
        except ValueError as err:
            raise VaccineManagementException(self._validation_error_message) from err

        vaccine_date_timestamp = vaccine_date.timestamp()

        if vaccine_date_timestamp < datetime.now().timestamp():
            raise VaccineManagementException("Vaccine date is outdated")

        return vaccine_date_timestamp
