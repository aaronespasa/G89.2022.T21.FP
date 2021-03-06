"""Contains the class Vaccination Appointment"""
from datetime import datetime
import hashlib
from freezegun import freeze_time
from uc3m_care.storage.cancellation_json_store import CancellationJsonStore
from uc3m_care.data.attribute.attribute_phone_number import PhoneNumber
from uc3m_care.data.attribute.attribute_patient_system_id import PatientSystemId
from uc3m_care.data.attribute.attribute_date_signature import DateSignature
from uc3m_care.data.vaccination_log import VaccinationLog
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage.appointments_json_store import AppointmentsJsonStore
from uc3m_care.parser.appointment_json_parser import AppointmentJsonParser
from uc3m_care.parser.cancellation_json_parser import CancellationJsonParser
from uc3m_care.data.attribute.attribute_vaccine_date import VaccineDate


# pylint: disable=too-many-instance-attributes
class VaccinationAppointment:
    """Class representing an appointment  for the vaccination of a patient"""

    def __init__(self, patient_sys_id, patient_phone_number, vaccine_date: str):
        self.__alg = "SHA-256"
        self.__type = "DS"
        self.__patient_sys_id = PatientSystemId(patient_sys_id).value
        patient = VaccinePatientRegister.create_patient_from_patient_system_id(
            self.__patient_sys_id
        )
        self.__patient_id = patient.patient_id
        self.__phone_number = PhoneNumber(patient_phone_number).value
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        self.__appointment_date = VaccineDate(vaccine_date).value
        self.__date_signature = self.vaccination_signature

    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return (
            "{alg:"
            + self.__alg
            + ",typ:"
            + self.__type
            + ",patient_sys_id:"
            + self.__patient_sys_id
            + ",issuedate:"
            + self.__issued_at.__str__()
            + ",vaccinationtiondate:"
            + self.__appointment_date.__str__()
            + "}"
        )

    @property
    def patient_id(self):
        """Property that represents the guid of the patient"""
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, value):
        self.__patient_id = value

    @property
    def patient_sys_id(self):
        """Property that represents the patient_sys_id of the patient"""
        return self.__patient_sys_id

    @patient_sys_id.setter
    def patient_sys_id(self, value):
        self.__patient_sys_id = value

    @property
    def phone_number(self):
        """Property that represents the phone number of the patient"""
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = PhoneNumber(value).value

    @property
    def vaccination_signature(self):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @property
    def issued_at(self):
        """Returns the issued at value"""
        return self.__issued_at

    @issued_at.setter
    def issued_at(self, value):
        self.__issued_at = value

    @property
    def appointment_date(self):
        """Returns the vaccination date"""
        return self.__appointment_date

    @property
    def date_signature(self):
        """Returns the SHA256"""
        return self.__date_signature

    def save_appointment(self):
        """saves the appointment in the appointments store"""
        appointments_store = AppointmentsJsonStore()
        appointments_store.add_item(self)

    @classmethod
    def get_appointment_from_date_signature(cls, date_signature):
        """returns the vaccination appointment object for the date_signature received"""
        appointments_store = AppointmentsJsonStore()
        appointment_record = appointments_store.find_item(
            DateSignature(date_signature).value
        )
        if appointment_record is None:
            raise VaccineManagementException("date_signature is not found")
        freezer = freeze_time(
            datetime.fromtimestamp(
                appointment_record["_VaccinationAppointment__issued_at"]
            )
        )
        freezer.start()
        appointment = cls(
            appointment_record["_VaccinationAppointment__patient_sys_id"],
            appointment_record["_VaccinationAppointment__phone_number"],
            datetime.fromtimestamp(
                appointment_record["_VaccinationAppointment__appointment_date"]
            )
            .date()
            .isoformat()[:10],
        )
        freezer.stop()
        return appointment

    @classmethod
    def create_appointment_from_json_file(cls, json_file, date_appointment: str):
        """returns the vaccination appointment for the received input json file"""
        appointment_parser = AppointmentJsonParser(json_file)
        new_appointment = cls(
            appointment_parser.json_content[appointment_parser.PATIENT_SYSTEM_ID_KEY],
            appointment_parser.json_content[
                appointment_parser.CONTACT_PHONE_NUMBER_KEY
            ],
            date_appointment,
        )
        return new_appointment

    @staticmethod
    def create_cancellation_from_json_file(json_file):
        """Creates the Cancellation and returns its date_signature"""
        # Add the cancellation to the Cancellation Store
        cancellation_parser = CancellationJsonParser(json_file)
        json_date_signature = cancellation_parser.json_content[
            cancellation_parser.DATE_SIGNATURE_KEY
        ]

        try:
            appointment_to_be_cancelled = (
                VaccinationAppointment.get_appointment_from_date_signature(
                    json_date_signature
                )
            )
        except VaccineManagementException as exception:
            raise VaccineManagementException(
                "The appointment with the given date_signature does not exist"
            ) from exception

        # check if the date signature of the appointment is outdated
        if appointment_to_be_cancelled.issued_at < datetime.timestamp(datetime.now()):
            raise VaccineManagementException(
                "The appointment with the given date_signature is outdated"
            )

        cancellations_store = CancellationJsonStore()
        cancellations_store.add_item(cancellation_parser.json_content)

        # return the data signature of the cancellation
        return cancellation_parser.json_content[cancellation_parser.DATE_SIGNATURE_KEY]

    def is_valid_today(self):
        """returns true if today is the appointment's date"""
        today = datetime.today().date()
        date_patient = datetime.fromtimestamp(self.appointment_date).date()
        if date_patient != today:
            raise VaccineManagementException("Today is not the date")
        return True

    def is_active(self):
        """Returns true if the appointment is not cancelled"""
        cancellations_store = CancellationJsonStore()
        cancellation_record = cancellations_store.find_item(self.date_signature)
        if cancellation_record is not None:
            raise VaccineManagementException(
                "The appointment is not active, it has been already cancelled."
            )
        return True

    def register_vaccination(self):
        """register the vaccine administration"""
        if self.is_valid_today() and self.is_active():
            vaccination_log_entry = VaccinationLog(self.date_signature)
            vaccination_log_entry.save_log_entry()
        return True
