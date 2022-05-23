from uc3m_care.storage.json_store import JsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class CancellationJsonStore:
    """Implements the singleton pattern"""

    # pylint: disable=invalid-name
    class __CancellationJsonStore(JsonStore):
        """Subclass of JsonStore for managing the VaccinationLog"""

        _FILE_PATH = JSON_FILES_PATH + "store_cancellations.json"
        _ID_FIELD = "date_signature"
        ERROR_INVALID_CANCELLATION_OBJECT = (
            "The Cancellation couldn't been created. It already exists."
        )

        def add_item(self, item):
            """Adds a new item received as a dictionary"""
            existing_item = self.find_item(item[self._ID_FIELD])

            if existing_item is None:
                self.load()
                self._data_list.append(item)
                self.save()
            else:
                raise VaccineManagementException(self.ERROR_INVALID_CANCELLATION_OBJECT)

    instance = None

    def __new__(cls):
        if not CancellationJsonStore.instance:
            CancellationJsonStore.instance = (
                CancellationJsonStore.__CancellationJsonStore()
            )
        return CancellationJsonStore.instance

    def __getattr__(self, nombre):
        return getattr(self.instance, nombre)

    def __setattr__(self, nombre, valor):
        return setattr(self.instance, nombre, valor)
