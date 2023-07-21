# Caveats of using KubeRay cluster for Ray Serve

Here we describe the main caveats of using KubeRay for deploying and running Ray Serve. It is mostly based on this
[documentation](https://docs.ray.io/en/latest/serve/production-guide/index.html)

## Configuration of the cluster itself

Unfortunately usage of Ray serve requires a bit of specific cluster configuration. The example of of such configuration
is [here](example.yaml). The most important Serve specific things there are:
* Line 20 - defining `dashboard-agent-listen-port`, that determines the port for serve management APIs
* Lines 51-52 defining ports for dashboard agent.


With this in place, we can use `dashboard-agent-listen-port` for accessing serve APIs. We can either 
`port-forward` or create additional route for accessing it.

## Implementing Serve code

We have here to serve examples - [hello](hello.py) and [fruit](fruit.py) borrowed from Ray documentation

# Deploying code

Once the code is created, we need to:
* Package it to the [docker image](Dockerfile)
* Create deployment [config file](https://docs.ray.io/en/latest/serve/production-guide/index.html) using `serve build` 
command

For our example the commands look like follows: 
````
serve build hello:graph -o hello.yaml
serve build fruit:deployment_graph -o fruit.yaml
````
These 2 commands will produce yaml files [here](hello.yaml) and [here](fruit.yaml)
The base yaml files presented here can be further enchanced based on 
[documentation](https://docs.ray.io/en/latest/serve/production-guide/config.html). Most common overrides include number
of replicas, and deployment parameters.

## Deploying to Ray cluster

Once yaml files are in place we can use [serve deploy](https://docs.ray.io/en/latest/serve/production-guide/index.html)
to deploy them. Serve deploy is a thin wrapper over HTTP APIs, that can be used directly. Definitions of the Rest
APIs can be found [here](https://docs.ray.io/en/latest/serve/api/index.html#serve-rest-api)

For our example we first do port-forward:

````
kubectl port-forward svc/raycluster-heterogeneous-head-svc 52365 -n max
````

And then use the following commands:
````
serve deploy hello.yaml
serve deploy fruit.yaml
````

The newer Rest APIs allow for supporting [serve applications](https://docs.ray.io/en/latest/serve/multi-app.html) and
Allow to deploy both serve applications

Once the application is installed you can also see configuration in the Ray dashboard

## Accessing applications

Following [this](https://docs.ray.io/en/latest/serve/production-guide/index.html), do port-forward:

````
kubectl port-forward svc/raycluster-heterogeneous-head-svc 8000 -n max
````

And then use this command:

````
curl -H "Content-Type: application/json" -d '["PEAR", 2]' "http://localhost:8000/"
curl "http://localhost:8000/?name=Ray"
````

## Undeploying 

The only command is:

````
serve shutdown
````

## Deploying multiple applications

Following [documentation](https://docs.ray.io/en/latest/serve/multi-app.html) Ray now supports deploying multiple 
independent Serve applications.

To try this, we first need to modify [fruit](fruit.py) and [hello](hello.py) to ensure that they are listening on 
different URLs [fruit_url](fruit_url.py) and [hello_url](hello_url.py)

Once this is done, the following command generates deployment yaml:
````
serve build --multi-app fruit_url:graph hello_url:graph -o multi_app.yaml
````
The auto-generated application names default to `app1`, `app2`, so I changed them in [generated yaml](multi_app.yaml).
Finally we need to add newly created python files [fruit_url](fruit_url.py) and [hello_url](hello_url.py) to the [docker
file](Dockerfile) and rebuild our image.

When this is done and cluster is restarted, we can deploy our applications as follows:
````
serve deploy multi_app.yaml
````
Once deployment is completed, you can port forward:

````
kubectl port-forward svc/raycluster-heterogeneous-head-svc 8000 -n max
````

and run:

````
curl "http://localhost:8000/greet/?name=Ray"
curl -H "Content-Type: application/json" -d '["PEAR", 2]' "http://localhost:8000/fruit/"
````
In addition to port-forward, you can create a route exposing port 8000 and using it for invocation.