# Incidents Generator



The Incidents Generator is a tool that can be used to create simulated incidents for testing situation awareness feature . It generates random incidents based on a set of predefined parameters, such as the type of incident, severity, location, and time.



## Getting Started

- Copy the net6.0 folder from from  Z:\utils\net6.0
- Open appsetings.json for config the service:
`MessageBrokerUri Url of message Broker service - this service is running under wildfly.`
`eventsToCreatePerMinute - mount of messages that will generated per minute`
`totalEvents - total events that will be sent to the system`
`midPoint - a point within a radius from which events will be generated. The first value is latitude and the second is longitude. for choosing a point you can use map services such as Google maps`



## Riniing the service 

Dotnet core 6.0 requires [Dotnet Core](https://dotnet.microsoft.com/en-us/download/dotnet/6.0) v6 to run.

```sh
dotnet IncidentsGenerator.CLI.dll
```

