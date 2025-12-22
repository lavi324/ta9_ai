# Intro
Logs enable us to investigate issues when something is wrong with our system or we would like to trace our system behavior. It's very important to log as much as possible so that we have as much information as possible when coming to deal with an issue on an environment.
_Asp.net core_ has built-in mechanism for logging. That built-in mechanism alongside with _Serilog_ & _NLog_ are the top options when choosing a logging framework for an _aspnet core_ project.

# Serilog
On _Albert .net core_ microservices we chose to use [Serilog](https://serilog.net/) as the logging framework.
Serilog integrates into asp.net core's logging infrastructure and adds some other useful features such as: _Scoped Logging, Structured Logging, Enrichments_ and more.

## Sinks
On _Serilog_, log targets (aka '_Appenders_') are called "sinks". _Serilog_ has many extensions to various [sinks](https://github.com/serilog/serilog/wiki/Provided-Sinks).
The ones that currently are relevant for us are _Console/ColoredConsole, RollingFile, Event Viewer, Debug, Syslog & Graylog_


## Scoped Logging
Scoped logging means, well, to log messages under a specific scope. For example, we'd like that all of the log messages written as part of a web request will all have the requests' unique id (let's say some Request-id) and URL.
This feature is very usefull in regular applications, but crucial on a microservices architecture as it allows us search for logs of a specific relevant scope across many logs.


## Structured Logging
Structured logging means that we can write dynamic properties to a log message rather than only a message. 
Structured logging has no meaning when writing to a flat sink such as _Console/File_, but has a lot of power when writing to a _NoSQL_ sink (such as _Graylog_) as it allow us to add as many relevant properties to a log message.
For example, mind the following log message:
`Log.Warning("Disk quota {Quota} MB exceeded by {User}", 1024, "userX");`
On a **file sink**, it will be simply translated to:
`"Disk quota 1024 MB exceeded by userX"`

However, on a _NoSQL_ sink (such as _Graylog_), it will add `Quota=1024, User=userX` to the log record so that we'll be able to query the log-repository by these values. awesome :)


## Enrichments
Serilog supports logging enrichments as extensions to the framework. Enrichments are extensions that can be used to add some information to each log message. 
For example:
`WithProcessId()` adds process-id property to each log message

## Configuration
Logging framework should be configured from outside the compiled code.
Basic configuration should allow us to do 2 important things:
1. Configure sinks (aka _'Appenders'/'Log Targets'_)
1. Configure levels to log to each target (or all together)
**NOTE:** _Serilog_ allows us to also configure minimum level per category

_Serilog_ allows us to configure from both within the code and a config file (ie `appsettings.json`). For example:

```
"Serilog": {
    "Using":  [ "Serilog.Sinks.Console", "Serilog.Sinks.File" ],
    "MinimumLevel": "Debug",
    "WriteTo": [
      { "Name": "Console" },
      { "Name": "File", "Args": { "path": "Logs/log.txt" } }
    ]
 }
```

This :top: will define 2 sinks for the logger with minimum level of _Debug_ for both.
Overview of Serilog configuration is available [here](https://github.com/serilog/serilog-settings-configuration)


# What should we log?
## Infrastructure Job
By infrastructure we should log:
1. Incoming/outgoing requests
1. Unhandled exceptions
1. Adding request scope (context)

## User Code
When developing, log everything that might be useful to you or to any other operator trying to understand the flow without debugging. Imagine that you're debugging a service without an IDE. So, log anything your code is doing (BL wise).

## Performance
!!TBD!!

# Log Levels
Log levels are the way of classifying a log message. Each log message contains its level.
Levels are super important as they allow us 2 basic capabilities:
1. Configure a sink to log messages of a specific level. For example, I don't want _Graylog_ to store `DEBUG` messages, but only WARNING & above.
1. Filter logs by log level/s. eg - when investigating a problem, the first thing I search for are logs with level > `WARNING`



|Level	| Usage|
|--|--|
| Verbose	| Verbose is the noisiest level, rarely (if ever) enabled for a production app.|
| Debug	| Debug is used for internal system events that are not necessarily observable from the outside, but useful when determining how something happened.|
|Information	|Information events describe things happening in the system that correspond to its responsibilities and functions. Generally these are the observable actions the system can perform.|
| Warning	|When service is degraded, endangered, or may be behaving outside of its expected parameters, Warning level events are used.|
|Error	|When functionality is unavailable or expectations broken, an Error event is used.|
|Fatal	|The most critical level, Fatal events demand immediate attention.|



# Developer Guide
Most of the log initialization & bootstrapping is done by infrastructure project `Infra.Logging.Serilog` so that on consumer projects (microservices) you can focus on just writing logs.

## When starting a new project
When starting a new project, first you need to setup logging and then you can log in various ways.
1. Add project-reference to infra project `Infra.Logging.Serilog`
1. On your Program.cs, right below `Host.CreateDefaultBuilder(args)` add `.UseTaSerilog()` so it will look like this:
![image.png](/.attachments/image-620d21f5-1108-4f90-b3c6-d40bc8d84eed.png)
1. On `Startup`'s `Configure` method (`Startup.cs`), add as first line:
            `app.UseTaSerilog();`
1. Delete auto-generated '`Logging`' section on `appsettings.json` (both prod/dev/staging if exist)
1. Add a new file `serilog.json` (can be copied from `SampleMicroService.API`)

After this setup, we can log simply in our app. The simple configuration will log to the following targets:
**Console** (console window or docker logs)
**File** (located at project root `/logs/`)
**Debug** (when debugging from VS - output window)

## Logging in the application
Now logging can be done in 2 ways:
1. Using _Dependency Injection_ (preferred in classes heavily logging)
1.1 Inject `ILogger<YourClass>` to `YourClass`'s ctor
1.2 Keep a reference to it on a private member
1.3 Use it to log across the class
1.4 Example:

![image.png](/.attachments/image-87014b41-03ec-449d-b0a9-9189057604eb.png)
1. Use the Logger object directly
2.1 Example

![image.png](/.attachments/image-f13acf9b-3f74-4e99-9df6-f90485d450ae.png)



**NOTE:** adding a context to the logger (via _generics_ on method \#1 or using `ForContext` on method \#2) will attach each log message to the context so it's easier to find out who emitted that message.
to the context so it's easier to find out who emitted that message.



## Important Instructions
1. Pay attention to LogLevel on each message logging
2. Use Structured Logging as possible
3. Don't log things already done by infra (such as `'Entering 'PostNewSensor' on controller 'SensorsController'`)
4. Don't log super-repeatable code so the log won't get trashed (e.g `'Get GeneralDal'`)
5. If `/logs` directory appears while debugging, right-click on it -> Exclude from project
6. Full Serilog sample file with various log types is available at `SampleMicroService.API/serilog.full.json`