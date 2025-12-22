[[_TOC_]]

# Intro
When coming to plan a new microservice we need to think of a few factors that are relevant.
Here we'll list the steps that have to be taken in order to think how to design the new microservice.

# Steps
1. List all requirements of the service
Write all the requirements, on each requirement list important relevant issues (e.g "attention to permissions")
1.1 While listing requirements, write down open issues
1. Design database tables. Attention to:
2.1 Keys
2.2 Indexes
2.3 Types & Sizes
2.4 Foreign Keys
1. Design API tier - Controllers & Operations 
e.g POST /api/sensors/
4. Get back to product with open-issues for more information
5. When having most of the requiremetns, endpoints & tables, we should mind service's complexity and decide:
5.1 Simple CRUD service - not too many process & flows
5.2 CQRS & DDD - when the service is quite complicated with more than 1-2 controllers affecting other system's components
6. Once decided, we have to think of more detailed design:
6.1 ApiModels (input/output)
6.2 Validators
6.3 Entities (goes together with ORM) (& AutoMappers)
6.4 Services required
6.4.1 May it be a service to call some other service (maybe should go to some common place for reuse?)
6.4.2 May it be some logic that's reasonable to wrap it on a dedicated service class
6.5 If on CQRS - design queries & commands
6.6 Design data flows in the microservice
