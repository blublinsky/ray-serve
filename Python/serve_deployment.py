# This implementation is based on serve Rest APIs described at
# https://docs.ray.io/en/latest/serve/api/index.html#serve-rest-api

import requests
import yaml
import json

class ServeManagemenAPIs(object):
    def __init__(self, base: str = "http://localhost:52365", timeout: int = 120) -> None:
        self.base = base
        self.tmout = timeout
        self.api_base = "/api/serve/"

    def deployYaml(self, yamls: str) -> int:
        # Execute HTTP request
        url = self.base + self.api_base + "deployments/"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        depl = json.dumps(yaml.safe_load(yamls))
        try:
            response = requests.put(url=url, headers=headers, data=depl, timeout=self.tmout)
        except Exception as e:
            print(f"Exception during deploying {e}")
            return 500
        # Check execution status
        if response.status_code // 100 != 2:
            print(f'Failed to submit deployment - {response.content.decode("utf-8")}')
        return response.status_code

    def deployJSON(self, yamld: dict) -> int:
        # Execute HTTP request
        url = self.base + self.api_base + "deployments/"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        try:
            response = requests.put(url=url, headers=headers, json=yamld, timeout=self.tmout)
        except Exception as e:
            print(f"Exception during deploying {e}")
            return 500
        # Check execution status
        if response.status_code // 100 != 2:
            print(f'Failed to submit deployment - {response.content.decode("utf-8")}')
        return response.status_code

    def getDeploymentStatus(self) -> tuple[int, dict]:
        # Execute HTTP request
        url = self.base + self.api_base + "deployments/status"
        headers = {"Accept": "application/json"}
        try:
            response = requests.get(url=url, headers=headers, timeout=self.tmout)
        except Exception as e:
            print(f"Exception during getting status {e}")
            return 500, None
        # Check execution status
        if response.status_code // 100 != 2:
            print(f'Failed to list clusters - {response.content.decode("utf-8")}')
            return response.status_code, None
        return response.status_code, response.json()

    def getDeployments(self) -> tuple[int, dict]:
        # Execute HTTP request
        url = self.base + self.api_base + "deployments/"
        headers = {"Accept": "application/json"}
        try:
            response = requests.get(url=url, headers=headers, timeout=self.tmout)
        except Exception as e:
            print(f"Exception during getting deployments {e}")
            return 500, None
        # Check execution status
        if response.status_code // 100 != 2:
            print(f'Failed to list clusters - {response.content.decode("utf-8")}')
            return response.status_code, None
        return response.status_code, response.json()

    # Note that this is deleting all deployment and stop serve.
    def deleteDeployments(self) -> int:
        # Execute HTTP request
        url = self.base + self.api_base + "deployments/"
        headers = {"Accept": "application/json"}
        try:
            response = requests.delete(url=url, headers=headers, timeout=self.tmout)
        except Exception as e:
            print(f"Exception during deleting deployments {e}")
            return 500

        # Check execution status
        if response.status_code // 100 != 2:
            print(f'Failed to submit deployment - {response.content.decode("utf-8")}')
        return response.status_code

    def deployApplicationsYaml(self, yamls: str) -> int:
        # Execute HTTP request
        url = self.base + self.api_base + "applications/"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        depl = json.dumps(yaml.safe_load(yamls))
        try:
            response = requests.put(url=url, headers=headers, data=depl, timeout=self.tmout)
        except Exception as e:
            print(f"Exception deploying applications {e}")
            return 500
        # Check execution status
        if response.status_code // 100 != 2:
            print(f'Failed to submit deployment - {response.content.decode("utf-8")}')
        return response.status_code

    def deployApplicationJSON(self, yamld: dict) -> int:
        # Execute HTTP request
        url = self.base + self.api_base + "applications/"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        try:
            response = requests.put(url=url, headers=headers, json=yamld, timeout=self.tmout)
        except Exception as e:
            print(f"Exception deploying applications {e}")
            return 500
        # Check execution status
        if response.status_code // 100 != 2:
            print(f'Failed to submit deployment - {response.content.decode("utf-8")}')
        return response.status_code

    # The reply schema is here
    # https://docs.ray.io/en/latest/serve/api/doc/ray.serve.schema.ServeDeploySchema.html#ray.serve.schema.ServeDeploySchema
    def getApplicationDeployments(self) -> tuple[int, dict]:
        # Execute HTTP request
        url = self.base + self.api_base + "applications/"
        headers = {"Accept": "application/json"}
        try:
            response = requests.get(url=url, headers=headers, timeout=self.tmout)
        except Exception as e:
            print(f"Exception getting applications {e}")
            return 500, None
        # Check execution status
        if response.status_code // 100 != 2:
            print(f'Failed to list clusters - {response.content.decode("utf-8")}')
            return response.status_code, None
        return response.status_code, response.json()

    # Note that this is deleting all applications and stop serve.
    def deleteApplications(self) -> int:
        # Execute HTTP request
        url = self.base + self.api_base + "applications/"
        headers = {"Accept": "application/json"}
        try:
            response = requests.delete(url=url, headers=headers, timeout=self.tmout)
        except Exception as e:
            print(f"Exception deleting applications {e}")
            return 500
        # Check execution status
        if response.status_code // 100 != 2:
            print(f'Failed to submit deployment - {response.content.decode("utf-8")}')
        return response.status_code