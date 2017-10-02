import json
from unittest import TestCase, mock

import yaml

import app


class AddValidateTransactionTestCase(TestCase):
    def setUp(self):
        app.application.testing = True
        self.app_client = app.application.test_client()
        self.schema = yaml.load(
            """
                    agencyCode:
                        is_empty: False
                        maxlength: 5
                    siteNumber:
                        maxlength: 15
                        is_empty: False
            """
            )
        self.location = {
            "agencyCode": "USGS ",
            "siteNumber": "123456789012345",
            "stationName": "This station name "
        }

        self.bad_location = {
            "agencyCode": "USGS ",
            "siteNumber": " ",
            "stationName": "This station name "
        }

        self.warning_location = {
            "agencyCode": "USGS ",
            "siteNumber": "123456789012345",
            "stationName": "This station name '"
        }

    def test_valid_single_field_transaction(self):
        valid_result = {'validation_passed_message': 'Validations Passed'}
        with mock.patch('mlrvalidator.services.sitefile_single_field_validator.validate', return_value=True):
            response = self.app_client.post('/validators',
                                        content_type='application/json',
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertEqual({'validation_passed_message': 'Validations Passed'}, resp_data)

    def test_single_field_error_transaction(self):
        with mock.patch('mlrvalidator.services.sitefile_single_field_validator.validate', return_value=False):
            response = self.app_client.post('/validators',
                                        content_type='application/json',
                                        data=json.dumps(self.bad_location))
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertEqual({'fatal_error_message': "Fatal Errors: {'siteNumber': ['Mandatory Field Missing']}"}, resp_data)

    def test_valid_reference_transaction(self):
        valid_result = {'validation_passed_message': 'Validations Passed'}
        with mock.patch('mlrvalidator.services.sitefile_reference_validator.validate', return_value=True):
            response = self.app_client.post('/validators',
                                        content_type='application/json',
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertEqual({'validation_passed_message': 'Validations Passed'}, resp_data)

    def test_reference_error_transaction(self):
        with mock.patch('mlrvalidator.services.sitefile_reference_validator.validate', return_value=False):
            response = self.app_client.post('/validators',
                                        content_type='application/json',
                                        data=json.dumps(self.bad_location))
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertEqual({'fatal_error_message': "Fatal Errors: {'siteNumber': ['Mandatory Field Missing']}"}, resp_data)

    def test_warning_transaction(self):
        with mock.patch('mlrvalidator.services.sitefile_warning_validator.validate', return_value=False):
            response = self.app_client.post('/validators',
                                        content_type='application/json',
                                        data=json.dumps(self.warning_location))
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertEqual({'warning_message': 'Validation Warnings: {}'}, resp_data)

