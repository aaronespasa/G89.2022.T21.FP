"""Classs for the attribute Reason"""
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


# pylint: disable=too-few-public-methods
class Reason(Attribute):
    """Classs for the attribute Reason"""
    _validation_error_message = "reason format is not valid"

    def _validate(self, attr_value: str) -> str:
        """Validate the attribute value"""
        if len(attr_value) < 2 or len(attr_value) > 100:
            raise VaccineManagementException(self._validation_error_message)
