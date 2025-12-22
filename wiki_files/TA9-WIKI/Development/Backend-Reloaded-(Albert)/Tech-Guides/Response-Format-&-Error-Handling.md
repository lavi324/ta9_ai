[[_TOC_]]


# Intro
Response Format & Error Handling are somehow related to each other because we want to know **which** value shall we return from our microservice's controllers and **how**. We'd also like to know how to behave on a success scenario as well as on faulty scenario.
In this document we'll try to address all the relevant formats, guides and behaviors related to formatting our microservices' responses.

# Reference
Our inspiration and master guide with this topic is the [JSON:API v1.1](https://jsonapi.org/format/1.1/) specification. While we're not fully comply with it now we should always strive to reach there.

# Infrastructure
On _Albert's_ infrastructure there's a middleware/filter that catches our actual controller's response/exceptions and reformat them into a consistent structure.

## JSON:API
All of our backend API will be compliant with _JSON:API_ specification. 
We'll be using a quite cool framework for that [JsonApiDotNetCore](https://www.jsonapi.net/), see #39944.

# Response Structure
The structure of the response will be as follows:
## On Success


```
HTTP Response Code 20X

{
  "meta": { //METADATA RELEVANT TO API REQUEST (not ready yet!)
    "totalResources": 1
  },
  "links": { //LINKS RELEVANT TO API REQUEST (not ready yet!)
    "self": "/articles?filter=contains(summary,'web')&sort=-lastModifiedAt&fields=title,summary&include=author",
    "first": "/articles?filter=contains(summary,'web')&sort=-lastModifiedAt&fields=title,summary&include=author",
    "last": "/articles?filter=contains(summary,'web')&sort=-lastModifiedAt&fields=title,summary&include=author"
  },

  "data": ... //ACTUAL RESOURCE RESPONSE
}
```

## On Error
```
HTTP Response Code 40X / 50X

{
  "errors": [{        //ARRAY OF ERRORS
    "status": 500,    //HTTP Status Code (same as returned by header)
    "code": 1044,     //Application error code
    "title": "CantConnectToAuditService",    //Error title
    "detail": ""      //On DEV will return error details (such as StackTrace)
  }]
}
```

# What should I return from my Controllers?
## On Success
- 	Return resource as is (will be wrapped as `200 OK`)
-	Return resource wrapped in `IStatusCodeActionResult` (such as `Ok()/Created()/NoContent()`)
## On Error/s
-	Validations of incoming requests - automatically will return `BadRequest` (no need further)
-	General exceptions - will be caught and wrapped in 500 (details on 'errors' array) - will put '`GeneralError`' as ResultCode - Should be used for TECHNICAL exceptions
-	`TAException` - will return 500 with details from `TAException` - Should be used for LOGIC exceptions


# Error Handling
While an operation is being executed in our microservice, it's quite common that exceptions are _thrown/caught_. Here we'll detail the guide of how to interpret this topic on _Albert_

##TAException
`TAException` is the exception class used by _Albert's_ infrastructure to convert a system failure into an API response.
It is consisted of the following structure:
- `error-code` (int value of `ResultCode` Enum)
- `error-name` (??? desired: `ResultCode` Enum value name)
- `error-info[]` (additional error information - NOT localized. May contain some helpful information regarding the error)

## ResultCode
Result/Error codes are integer codes to indicate a specific result/error of an operation.
Differently from Legacy codebase, on _Albert_ each service will maintain its own Enum of ResultCode.
Each microservice will start it from a new hundred (e.g: 1700)

## Specific Exceptions
Create your custom exception class when needed for better error specification.
1. Can use CLR exception classes
1. Can use custom exception classes
2.1 Inherit CLR exception OR `TAException` when they're related to the same error-code.
2.2 Always persist the inner exception (real cause)
		

## General notes regarding exceptions handling:
1. `Try-Catch` wherever you'd want to **handle** the exception (ie - NOT just for logging)
1.1 Handle - also refers to wrap and rethrow an exception with `TAException` (to use a specific code)
1. While developing our microservice, we should always try to make our controllers throw only `TAException` (NOT by wrapping generally...)















