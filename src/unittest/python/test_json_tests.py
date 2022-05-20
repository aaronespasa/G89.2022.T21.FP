"""# HSBGKJBAFNLAKM"""
import unittest
from pathlib import Path
import json
from freezegun import freeze_time
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care import JSON_FILES_PATH, \
                      JSON_FILES_RF2_PATH, \
                      JSON_FILES_CANCELLATION_PATH
from uc3m_care import CancellationJsonStore, PatientsJsonStore

DATE = "2022-03-08"

# parameter of the non-right tests
param_list_nok = [('Case_NV_02',
  'test_dup_node1.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_03', 'test_del_node1.json', 'The JSON file is empty'),
 ('Case_NV_04', 'test_del_node3.json', 'The JSON file is empty'),
 ('Case_NV_05',
  'test_dup_node3.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_06',
  'test_del_node2.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_07',
  'test_mod_node2.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_08',
  'test_dup_node2.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_09',
  'test_del_node6.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_10',
  'test_dup_node6.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_11',
  'test_del_node4.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_12',
  'test_dup_node4.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_13',
  'test_mod_node4.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_14',
  'test_del_node12.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_15',
  'test_dup_node12.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_16',
  'test_del_node14.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_17',
  'test_dup_node14.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_18',
  'test_del_node16.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_19',
  'test_dup_node16.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_20',
  'test_del_node18.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_21',
  'test_dup_node18.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_22',
  'test_del_node20.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_23',
  'test_dup_node20.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_24',
  'test_del_node22.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_25',
  'test_dup_node22.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_26',
  'test_del_quote.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_27',
  'test_dup_quote.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_28',
  'test_mod_quote.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_29',
  'test_del_commaseparator.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_30',
  'test_dup_commaseparator.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_31',
  'test_mod_commaseparator.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_32',
  'test_del_colonseparator.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_33',
  'test_dup_colonseparator.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_34',
  'test_mod_colonseparator.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_35', 'test_del_node24.json', 'The key of the JSON file is wrong.'),
 ('Case_NV_36', 'test_dup_node24.json', 'The key of the JSON file is wrong.'),
 ('Case_NV_37', 'test_mod_node24.json', 'The key of the JSON file is wrong.'),
 ('Case_NV_38',
  'test_del_node28.json',
  'The value of the JSON file is wrong.'),
 ('Case_NV_39',
  'test_dup_node28.json',
  'The value of the JSON file is wrong.'),
 ('Case_NV_40',
  'test_del_node8.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_41',
  'test_dup_node8.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_42',
  'test_mod_node28.json',
  'The value of the JSON file is wrong.'),
 ('Case_NV_43', 'test_del_node31.json', 'The key of the JSON file is wrong.'),
 ('Case_NV_44', 'test_dup_node31.json', 'The key of the JSON file is wrong.'),
 ('Case_NV_45', 'test_mod_node31.json', 'The key of the JSON file is wrong.'),
 ('Case_NV_46',
  'test_del_node35.json',
  'The value of the JSON file is wrong.'),
 ('Case_NV_47',
  'test_dup_node35.json',
  'The value of the JSON file is wrong.'),
 ('Case_NV_48',
  'test_mod_node35.json',
  'The value of the JSON file is wrong.'),
 ('Case_NV_49',
  'test_del_node10.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_50',
  'test_dup_node10.json',
  'The format of the JSON file is not valid.'),
 ('Case_NV_51', 'test_del_node38.json', 'The key of the JSON file is wrong.'),
 ('Case_NV_52', 'test_dup_node38.json', 'The key of the JSON file is wrong.'),
 ('Case_NV_53', 'test_mod_node38.json', 'The key of the JSON file is wrong.'),
 ('Case_NV_54',
  'test_del_node42.json',
  'The value of the JSON file is wrong.'),
 ('Case_NV_55',
  'test_dup_node42.json',
  'The value of the JSON file is wrong.'),
 ('Case_NV_56',
  'test_mod_node42.json',
  'The value of the JSON file is wrong.')]

class TestJsons(unittest.TestCase):
    """Test the JSONs from the cancellation of appointments tree"""

    def setUp(self) -> None:
        """setUp IS EXECUTED ONCE BEFORE EACH TEST"""
        ...

    @freeze_time(DATE)
    def test_Case_Valid(self):    # Existing file and correct content
        """
        This test checks if the valid json file is recognized with no error
        """
        PatientsJsonStore().empty_json_file()
        cancellation_json_storage = CancellationJsonStore()
        cancellation_json_storage.empty_json_file()

        # Generate a valid json file
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()
        my_manager.request_vaccination_id(
            "78924cb0-075a-4099-a3ee-f3b562e805b9", "minombre tienelalongitudmaxima", "Regular",
            "+34123456789", "6")
        my_manager.get_vaccine_date(file_test, DATE)

        valid_json = JSON_FILES_CANCELLATION_PATH + "test_right.json"

        expected_date_signature = "ced0953d112ab693b83d1ced965fcc670b558235361b9d1bd62536769a1efa3b"
        date_signature = my_manager.cancel_appointment(valid_json)
        self.assertEqual(date_signature, expected_date_signature)
        self.assertIsNotNone(cancellation_json_storage.find_item(date_signature))

    @freeze_time(DATE)
    def test_Case_NV(self):
        """Invalid syntax, node 1 duplicated"""
        PatientsJsonStore().empty_json_file()
        cancellation_json_storage = CancellationJsonStore()
        cancellation_json_storage.empty_json_file()

        # Generate a valid json file
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()
        my_manager.request_vaccination_id(
         "78924cb0-075a-4099-a3ee-f3b562e805b9", "minombre tienelalongitudmaxima", "Regular",
         "+34123456789", "6")
        my_manager.get_vaccine_date(file_test, DATE)
        
        for case_name, node_name, exception_name in param_list_nok:
            with self.subTest(test=case_name):
                with self.assertRaises(VaccineManagementException) as context:
                    cancellation_json = JSON_FILES_CANCELLATION_PATH + node_name
                    date_signature = my_manager.cancel_appointment(cancellation_json)
                self.assertEqual(exception_name, context.exception.message)
                self.assertIsNone(cancellation_json_storage.find_item(date_signature))
