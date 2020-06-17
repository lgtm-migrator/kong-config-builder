import boto3
import logging

from os import environ
from typing import List, Dict, Optional
from functools import reduce
from kong_config_builder.password import PasswordManager


KCB_PASSWORD_GENERATOR_SIZE = int(environ.get(
    "KCB_PASSWORD_GENERATOR_SIZE", 50))


class ParameterStoreAPI:
    def __init__(self, client=boto3.client("ssm"), password=PasswordManager):
        self.logger = logging.getLogger(__name__)
        self._client = client
        self._password_manager = password

        self.available_parameters = {}

    def get(self, name: str, is_password: bool = False) -> Optional[str]:
        value = self.available_parameters.get(name, None)
        if not value and is_password:
            password = self._password_manager.generate(
                KCB_PASSWORD_GENERATOR_SIZE)
            self.put(name, password, encrypt=False)
            value = password

        return value

    def put(
        self,
        name: str,
        value: str,
        tags: List[Dict[str, str]] = [],
        encrypt: bool = True
    ) -> bool:
        parameter_type = "SecureString" if encrypt else "String"
        try:
            self._client.put_parameter(
                Name=name,
                Value=value,
                Tags=tags,
                Type=parameter_type,
                Overwrite=False
            )
            return True
        except Exception as err:
            self.logger.error(f"The parameter {err} already exists.")
            return False

    def populate(self, namespace: str) -> None:
        parameters_list = self._get_parameters_by(namespace)

        for parameter in parameters_list:
            values = self._get_value_by(parameter)
            self.available_parameters[parameter] = values[parameter]

    def _get_parameters_by(self, namespace: str) -> List:
        paginate = self._client.get_paginator("describe_parameters")
        ParameterFilters = [{
            "Key": "Name",
            "Values": [namespace],
            "Option": "BeginsWith"
        }]
        iterator = paginate.paginate(ParameterFilters=ParameterFilters)
        params = set()
        for page in iterator:
            for parameter in page["Parameters"]:
                params.add(parameter["Name"])

        return list(params)

    def _get_value_by(self, key: str):
        def objecter(current, next):
            current[next["Name"]] = next["Value"]
            return current
        parameters = self._client.get_parameters(
            Names=[key],
            WithDecryption=True
        )

        return reduce(objecter, parameters["Parameters"], {})
