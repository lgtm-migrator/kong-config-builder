from unittest import TestCase
from unittest.mock import Mock, call
from kong_config_builder.parameter import ParameterStoreAPI

PARAMETERS = {
    "/fake-namespace/first-parameter": "first-parameter-value",
    "/fake-namespace/second-parameter": "second-parameter-value"
}


class TestParameterAPI(TestCase):
    def setUp(self):
        self.client = Mock()

    def test_should_initialize_parameter_object(self):
        parameter = ParameterStoreAPI(client=self.client)
        self.assertIsInstance(parameter, ParameterStoreAPI)

    def test_should_populate_with_available_stored_parameters(self):
        parameter = ParameterStoreAPI(client=self.client)
        parameter._get_parameters_by = Mock(return_value=PARAMETERS.keys())
        parameter._get_value_by = Mock(
            side_effect=lambda key: {key: PARAMETERS[key]})

        parameter.populate("fake-namespace")

        parameter._get_parameters_by.assert_called_once()
        parameter._get_value_by.assert_has_calls([
            call("/fake-namespace/first-parameter"),
            call("/fake-namespace/second-parameter"),
        ])
        self.assertEqual(parameter.available_parameters, PARAMETERS)

    def test_should_paginate_through_parameters(self):
        pass

    def test_should_get_parameter(self):
        parameter = ParameterStoreAPI(client=self.client)
        parameter.put = Mock()
        parameter.available_parameters = PARAMETERS
        value = parameter.get("/fake-namespace/first-parameter")

        parameter.put.assert_not_called()
        self.assertEqual(value, "first-parameter-value")

    def test_should_get_parameter_empty(self):
        parameter = ParameterStoreAPI(client=self.client)
        parameter.put = Mock()
        parameter.available_parameters = PARAMETERS
        value = parameter.get("/fake-namespace/empty-parameter")

        parameter.put.assert_not_called()
        self.assertEqual(value, None)

    def test_shoudl_get_parameter_generating_password(self):
        parameter = ParameterStoreAPI(client=self.client)
        parameter.put = Mock(return_value=True)
        parameter.available_parameters = PARAMETERS
        value = parameter.get("/fake-namespace/password-parameter", True)

        parameter.put.assert_called_once()
        self.assertEqual(len(value), 50)

    def test_should_put_parameter(self):
        parameter = ParameterStoreAPI(client=self.client)
        self.client.put_parameter = Mock(return_value=True)

        parameter = ParameterStoreAPI(client=self.client)
        response = parameter.put(
            name="/fake-namespace/development/fake-application/fake-password",
            value="qwertyuiop",
            tags=[{"team": "fake-team"}],
            encrypt=True
        )

        self.client.put_parameter.assert_called_once_with(
            Name="/fake-namespace/development/fake-application/fake-password",
            Value="qwertyuiop",
            Tags=[{"team": "fake-team"}],
            Type="SecureString",
            Overwrite=False
        )
        self.assertEqual(response, True)

    def test_should_get_parameters_by_namespace(self):
        parameter = ParameterStoreAPI(client=self.client)
        self.client.get_paginator = Mock()

        paginate = Mock()
        self.client.get_paginator.return_value = paginate
        paginate.paginate = Mock(return_value=[
            {"Parameters": [{"Name": "foo"}, {"Name": "bar"}]}])

        parameters = parameter._get_parameters_by("fake-namespace")

        self.client.get_paginator.assert_called_once_with(
            "describe_parameters")
        paginate.paginate.assert_called_once_with(ParameterFilters=[{
            "Key": "Name",
            "Values": ["fake-namespace"],
            "Option": "BeginsWith"
        }])
        self.assertEqual(parameters.sort(), ["foo", "bar"].sort())

    def test_should_get_parameter_by_key(self):
        parameter = ParameterStoreAPI(client=self.client)
        self.client.get_parameters = Mock(return_value={"Parameters": [
            {"Name": "foo", "Value": "bar"}]})

        param = parameter._get_value_by("foo")

        self.client.get_parameters.assert_called_once_with(
            Names=["foo"], WithDecryption=True)
        self.assertEqual(param, {"foo": "bar"})
