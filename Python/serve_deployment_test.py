from serve_deployment import *
import time

def test_deplyments():

    deployYaml = """import_path: hello:graph
runtime_env: {}
host: 0.0.0.0
port: 8000
deployments:
- name: Doubler
- name: HelloDeployment
"""

    deployJSON = {"import_path": "hello:graph", "runtime_env": {}, "host": "0.0.0.0", "port": "8000",
                  "deployments": [{"name": "Doubler"}, {"name": "HelloDeployment"}]}

    manager = ServeManagemenAPIs()
    reply = manager.deployYaml(deployYaml)
    assert reply == 200
    print(f"Deployed serve using Yaml, reply {reply}")

    reply = manager.waitDeploymentComplete()
    assert reply[0] == 200
    print(f"Deployment status {reply[1]}")

    reply = manager.deployJSON(deployJSON)
    assert reply == 200
    print(f"Deployed serve using JSON, reply {reply}")

    reply = manager.getDeploymentStatus()
    assert reply[0] == 200
    print(f"Deployment status {reply[1]}")

    reply = manager.getDeployments()
    assert reply[0] == 200
    print(f"Deployments are {reply[1]}")

    reply = manager.deleteDeployments()
    assert reply == 200
    print(f"Deleting deplyments, reply {reply}")

    time.sleep(5)

def test_applications():

    deployYaml = """proxy_location: EveryNode

http_options:

  host: 0.0.0.0

  port: 8000

applications:

- name: fruit

  route_prefix: /fruit

  import_path: fruit_url:graph

  runtime_env: {}

  deployments:

  - name: MangoStand
    user_config:
      price: 3

  - name: OrangeStand
    user_config:
      price: 2

  - name: PearStand
    user_config:
      price: 4

  - name: FruitMarket
    num_replicas: 2

  - name: DAGDriver

- name: greet

  route_prefix: /greet

  import_path: hello_url:graph

  runtime_env: {}

  deployments:

  - name: Doubler

  - name: HelloDeployment

  - name: DAGDriver
"""

    deployJSON = {"proxy_location": "EveryNode", "http_options": {"host": "0.0.0.0", "port": 8000},
                  "applications": [{"name": "fruit", "route_prefix": "/fruit", "import_path": "fruit_url:graph",
                                    "runtime_env": {},
                                    "deployments": [{"name": "MangoStand", "user_config": {"price": 3}},
                                                    {"name": "OrangeStand", "user_config": {"price": 2}},
                                                    {"name": "PearStand", "user_config": {"price": 4}},
                                                    {"name": "FruitMarket", "num_replicas": 2},
                                                    {"name": "DAGDriver"}]},
                                    {"name": "greet", "route_prefix": "/greet", "import_path": "hello_url:graph",
                                     "runtime_env": {},
                                     "deployments": [{"name": "Doubler"},
                                                     {"name": "HelloDeployment"},
                                                     {"name": "DAGDriver"}]}]}

    manager = ServeManagemenAPIs()

    reply = manager.deployApplicationsYaml(deployYaml)
    assert reply == 200
    print(f"Deployed serve applications using Yaml, reply {reply}")

    reply = manager.waitApplicationsDeploymentComplete()
    assert reply[0] == 200
    print(f"Get applications deployment complete, reply {reply[1]}")

    reply = manager.deleteApplications()
    assert reply == 200
    print(f"Deleting applications, reply {reply}")

    time.sleep(5)

    reply = manager.deployApplicationJSON(deployJSON)
    assert reply == 200
    print(f"Deployed serve applications using JSON, reply {reply}")

    time.sleep(5)

    reply = manager.getApplicationDeployments()
    assert reply[0] == 200
    print(f"Get applications deployment, reply {reply[1]}")

    reply = manager.deleteApplications()
    assert reply == 200
    print(f"Deleting applications, reply {reply}")



