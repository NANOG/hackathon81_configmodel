# hackathon81_configmodel
NANOG 81 Hackathon - Configuration Modeling

This is a sample project to serve as a basic configuration modeling and software design tutorial.

The code is intended for educational purposes only and is in no way intended for production use.

## What's in this directory
This is the `hack` directory, which contains a skeleton to get you started.

If you're looking for a basic, working system to expand upon, you probably want to be looking at the [basic-working](../basic-working) directory.

## Getting started with your environment
1. Git
   1. Click the `Fork` button at https://github.com/NANOG/hackathon81_configmodel
   2. On your machine:
      ```shell
      git clone https://github.com:{YOUR_GITHUB_ACCOUNT_NAME}/hackathon81_configmodel.git
      ```
2. Python virtual environments (see Cheatsheet selection below)

## Getting started with the code
Once you have your environment set up (see the Cheatsheet section below) it's time to consider the basic directory layout
```text
hack/
├── run.py <- run the app (no need to change this)
├── tests/ <- your unit tests
└── configmodel/
    ├── schemas <- your json schemas
    ├── templates <- your mako templates
    ├── logic/ <- your business logic
    ├── database/ <- your database models
    └── api/   
        └── namespaces/
            ├── __init__.py <- add your namespaces here (otherwise no need to change this)
            ├── hello.py <- example namespace
            └── ... <- your namespaces
```

## Creating a basic system
1. Create interface and BGP peer configuration schemas
2. Create templates for interface and BGP peer configuration rendering for two vendors
3. Create a RESTful API
4. Add logic to create backbone link and PNI services
5. Add a database

## Ideas for extending the basic system
1. Add more schemas and templates
2. Add more services (e.g., iBGP mesh, management)
3. Push configs to devices
4. Integrate with PeeringDB for PNI or IXP peering
5. Add logging to the system
6. Instrument the system (i.e., generate and send metrics on system utilization)
7. Add a gRPC API
8. Convert the JSON Schema models to OpenConfig
9. Add timestamp, version, user-attribution to the API and database
10. Add authentication to the service
 
## Cheatsheet
Here's a shortcut for making virtual environments (put this in, say, `~/bin/mkvenv`)
```shell
#!/bin/bash

if [ -e ./venv ]
then
    echo "venv already exists"
else
    echo "creating ./venv..."
    cwd=`basename \`pwd\``
    virtualenv venv --prompt "($cwd) " --python=python3.8
fi
```

Then create a virtual environment and activate it
```shell
mkvenv
source venv/bin/activate
````

And deactivate it later with
```shell
deactivate
```

Install Python dependencies
```shell
pip3 install -r requirements-dev.txt
```

Before committing code
```shell
tox
```
