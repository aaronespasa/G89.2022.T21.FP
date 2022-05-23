"""Subclass of JsonParer for parsing inputs of get_vaccine_date"""
from uc3m_care.parser.json_parser import JsonParser
from uc3m_care.data.attribute.attribute_date_signature import DateSignature
from uc3m_care.data.attribute.attribute_cancellation_type import CancellationType
from uc3m_care.data.attribute.attribute_reason import Reason
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class CancellationJsonParser(JsonParser):
    """Subclass of JsonParer for parsing inputs of get_vaccine_date"""

    BAD_REASON_LABEL_ERROR = "The key of the JSON file is wrong."
    BAD_REASON_VALUE_ERROR = "The value of the JSON file is wrong."
    BAD_CANCELLATION_TYPE_LABEL_ERROR = "The key of the JSON file is wrong."
    BAD_CANCELLATION_TYPE_VALUE_ERROR = "The value of the JSON file is wrong."
    BAD_DATE_SIGNATURE_LABEL_ERROR = "The key of the JSON file is wrong."
    BAD_DATE_SIGNATURE_VALUE_ERROR = "The value of the JSON file is wrong."
    DATE_SIGNATURE_KEY = "date_signature"
    CANCELLATION_TYPE_KEY = "cancellation_type"
    REASON_KEY = "reason"

    _JSON_KEYS = [DATE_SIGNATURE_KEY, CANCELLATION_TYPE_KEY, REASON_KEY]

    _ERROR_MESSAGES = [
        BAD_DATE_SIGNATURE_LABEL_ERROR,
        BAD_CANCELLATION_TYPE_LABEL_ERROR,
        BAD_REASON_LABEL_ERROR,
    ]

    def __init__(self, input_file):
        super().__init__(input_file)
        self.validate_date_signature()
        self.validate_cancellation_type()
        self.validate_reason()

    def validate_date_signature(self):
        """validate that the key date_signature from the JSON is correct"""
        date_signature = self._json_content[self.DATE_SIGNATURE_KEY]

        try:
            DateSignature(date_signature)
        except Exception as exception:
            raise VaccineManagementException(
                self.BAD_DATE_SIGNATURE_VALUE_ERROR
            ) from exception

    def validate_cancellation_type(self):
        """validate that the key cancellation_type from the JSON is correct"""
        cancellation_type = self._json_content[self.CANCELLATION_TYPE_KEY]

        try:
            CancellationType(cancellation_type)
        except Exception as exception:
            raise VaccineManagementException(
                self.BAD_CANCELLATION_TYPE_VALUE_ERROR
            ) from exception

    def validate_reason(self):
        """validate that the key reason from the JSON is correct"""
        reason = self._json_content[self.REASON_KEY]

        try:
            Reason(reason)
        except Exception as exception:
            raise VaccineManagementException(self.BAD_REASON_VALUE_ERROR) from exception
