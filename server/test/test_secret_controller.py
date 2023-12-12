from server.test import BaseTestCase

urlencoded = 'application/x-www-form-urlencoded'
json = 'application/json'
xml = 'application/xml'
test_data = dict(secret='secret_example',
                 expire_after_views=56,
                 expire_after=56)


class TestSecretController(BaseTestCase):

    def test_add_secret_with_json_return_type(self):
        headers = {'Content-Type': urlencoded, 'Accept': json}
        response = self.client.open(
            '/v1/secret',
            method='POST',
            data=test_data,
            content_type=urlencoded,
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_secret_with_xml_return_type(self):
        data = dict(secret='secret_example',
                    expire_after_views=56,
                    expire_after=56)
        headers = {'Content-Type': urlencoded, 'Accept': xml}
        response = self.client.open(
            '/v1/secret',
            method='POST',
            data=data,
            content_type=urlencoded,
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_secret_with_unsupported_content_type(self):
        headers = {'Content-Type': json, 'Accept': json}
        response = self.client.open(
            '/v1/secret',
            method='POST',
            data=test_data,
            content_type=json,
            headers=headers)
        self.assertStatus(response, 415)

    def test_get_secret_by_hash_not_found(self):
        headers = {'Accept': json}
        response = self.client.open(
            '/v1/secret/{hash}'.format(hash='hash_example'),
            method='GET',
            headers=headers)
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
