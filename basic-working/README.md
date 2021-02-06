# hackathon81_configmodel
NANOG 81 Hackathon - Configuration Modeling

This is a sample project to serve as a basic configuration modeling and software design tutorial.

The code is intended for educational purposes only and is in no way intended for production use.

## What's in this directory
This is the `basic-working` directory, which contains a basic, working system.  You can expand on this, though you may which to copy this directory in your own project directory next to `hack` and `basic-working`.

If you're trying to get to a basic, working system from scratch (well, from a skeleton), you probably want to be looking at the [hack](../hack) directory. 

## What this basic, working system does
1. Implements interface and BGP peer configuration schemas
2. Implements templates for interface and BGP peer configuration rendering for two vendors
3. Contains a RESTful API
4. Contains logic for backbone link and PNI services
5. Persists configs and services to a database

## Ideas for extending the basic system
1. Add more schemas and templates
2. Add more services (e.g., iBGP mesh, management)
3. Push configs to devices
4. Integrate with PeeringDB for PNI or IXP peering
5. Add logging to the system
6. Instrument the system (i.e., generate and send metrics on system utilization)
7. Add a gRPC API
8. Convert the JSON Schema models to OpenConfig
9. Add timestamp, versioning, and user-attribution to the API and database
10. Add authentication to the service
