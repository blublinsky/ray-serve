from ray import serve
from ray.serve.drivers import DAGDriver
from ray.serve.deployment_graph import InputNode
import starlette.requests

def query_params(request: starlette.requests.Request) -> dict[str,str]:
    """Returns request query parameters"""
    return request.query_params

@serve.deployment
class Doubler:
    def double(self, s: str):
        return s + " " + s


@serve.deployment
class HelloDeployment:
    def __init__(self, doubler):
        self.doubler = doubler

    async def say_hello_twice(self, name: str):
        ref = await self.doubler.double.remote(f"Hello, {name}!")
        return await ref

with InputNode() as req:
    name = req["name"]
    doubler = Doubler.bind()
    hello = HelloDeployment.bind(doubler)
    greeter = hello.say_hello_twice.bind(name)

graph = DAGDriver.options(route_prefix="/greet").bind(greeter, http_adapter=query_params)