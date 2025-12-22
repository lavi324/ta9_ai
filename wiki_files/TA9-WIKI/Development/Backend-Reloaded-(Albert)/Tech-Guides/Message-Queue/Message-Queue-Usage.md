[[_TOC_]]

# Intro
On Albert microservices we can use a message queue for various usages. 
In this document we'll see how to integrate and use this capability in practice.

# MassTransit
[MassTransit](https://masstransit-project.com/) is framework we're using to abstract/hide the actual queue usage. 
It supports many queue implementations and allows us to do almost nothing but the initial configuration when replacing a queue.
MassTransit contains a very comprehensive and easy to use [documentation](https://masstransit-project.com/understand/), however, we will list here all the common usages by our platform.

## Messaging Objects
In order to _send/publish/receive_ messages we have to define/use a _message_ object.
MassTransit platform wraps all the actual dealing with the qeue giving us easy use with _objects & classes_.
The big downside of that approach is that every message one side (e.g _send_) must have **exactly** the same type as on the other side (e.g consume). Same type means **exactly same namespace and type name**.

### Message Contracts
In _Albert_ we have a new class library `Messaging.Contracts` that is containing all the messages types that our queue deals with. _Messages_ should be organized in folders (`namespaces`) by topic and message type (eg _Reponses_)

### Message Types Conventions
In order to keep it organized, here are some conventions:
1. All _message_ objects are _interface_ types
1. A _message_ object name that is sent to the queue, should begin with the **verb** hinting the message responsibility, e.g. `**Submit**ScheduledTask`
1.  A _message_ object name that is a response or indicate an operation that was done should contain the **verb** at the end past simple, e.g. `ScheduledTask**Submitted**`

## Consumers
_Consumers_ are the way MassTransit enables us to receive & handle messages. All that we need to do is implement a specific _interface_ with the _message_ type we're interested in and the framework _registers_ us to that _message_ behind the scenes.

## Queues behind the Scenes
Behind the scenes,  as we can see on the _RabbitMQ_ (for example) management console, MassTransit creates for us a _queue_ for each message type we're _sending/consuming_. This behavior can be altered/configured as we desire (see ahead).

# Usage Guide
Here's an actual step-by-step guide on how to use a Message queue within _Albert_ microservices ecosystem:
1. Add reference to _Infra_ project: `Infra.Queue.MassTransit`
1. Add reference to Messaging project: `Messaging.Contract`
1. Add configuration on _appsettings_:
 
```
"ServiceQueue": {
    "RabbitMq": {
      "HostAddress": "localhost",
      "VirtualHost": "/",
      "Username": "guest",
      "Password": "guest"
    }
  }
```

4. Add on `ConfigureServices`:
			
```
//Adding Service Bus handlers
var queueConfig = Configuration.GetSection("ServiceQueue").Get<ServiceQueueConfig>();

services.AddMassTransit(cfg =>
{
  cfg.SetKebabCaseEndpointNameFormatter();

  //Adding various "interesting" messages
  cfg.AddConsumer<SubmitScheduledTaskConsumer>();

  cfg.UseTaQueue(queueConfig);

});
services.AddMassTransitHostedService();
```

5. **Consuming Messages**
5.1 In order to consume a message, we should add a new class that has to implement a specific interface `IConsumer<**REQUIRED_MESSAGE_TYPE**>`
5.2 Convention: Consumers should be placed on a dedicated folder on project: Messaging/Consumers
5.3 Consume method implementation 
5.3.1 a single method has to be implemented as part of the interface. In this method you're getting the context, which contains the message that was consumed alongside many other indications (less important for now)
5.3.2 The context object can be also used to respond to that message that just was consumed
5.3.3 The context object can be also used to publish/send other messages to the queuue as well
5.4 Once we have the consume class handler, we have to register it as part of the initial configuration
5.4.1 regular register
  `cfg.AddConsumer<SubmitScheduledTaskConsumer>();`
5.4.2 Specific queue name registration - As described earlier, this kind of register will register to a qeuee named 'submit-scheduled-task', but sometimes we might want to register to a qeueu name that is different from the consumed object's class name. This can be done in the following manner:
`cfg.AddConsumer<ExecuteScheuledTaskConsumer>().Endpoint(ep=>ep.Name = "execute-scheduled-task-job-sample");`


6. **Sending Messages** - to send a message to the queue (to be handled by a single consumer), here are our options:
6.1 _Inject_ `IBus` and use it - this is useful when we're **initiating** the communication (rather than responding to other events)
        
```
IBus _serviceBus;
public SchedulerConsumerController(IBus serviceBus)
{
  _serviceBus = serviceBus;
}
```

Use it:

```
var sendEndpoint = await _serviceBus.GetSendEndpoint(new Uri($"queue:execute-scheduled-task-job{targetQueue}"));
await sendEndpoint.Send<ExecuteScheduledTaskJob>(_mapper.Map<ExecuteScheduledTaskJob>(request.TaskToProcess));
```

    6.1.1 `_serviceBus.GetSendEndpoint` - can be used with a generic message type **or** by specifying the _queue_ name (as done above). Behavior is quite the same as described previously here

7. **Request Response**
7.1 If our operation is a request-response model, we have to deal with 2 issues:
    7.1.1 Responding - on our consumer handler we must repond to the message with the context object received, eg.:
                    `await context.RespondAsync<ScheduledTaskSubmitted>(new { TaskId = taskId });`
7.1.2 Requesting - the operation client can request a response for the message he is sending in the following way:
            
```
           var ep =  _serviceBus.CreateRequestClient<SubmitScheduledTask>(); //Here's the request message
           var result = await ep.GetResponse<ScheduledTaskSubmitted>(new { //Here's the response message type
                Weekdays = new int[] { 0, 1,2,3, 4,5,6},
                TimeOfDayHour = 26,
                TimeOfDayMinute = 17,
                Topic = "sample",
                Payload = "my lovely payload!",
                Timezone = "Asia/Jerusalem"

            });
```

   **NOTE:** execution will wait for the message to be responded, so make sure you're calling this method only on messages that are responded!


7.2 Multiple Response Types
Most of the times, our responder may return more than one message type (ie - success operation vs failure message type). In this case we call the 'GetResponse' with 2 generic arguments indicating the possible message responds. After the message is responded, we have to check each to see actual response:
  
```
var result = await ep.GetResponse<ScheduledTaskSubmitted, OperationFailed>(new {
                Weekdays = new int[] { 0, 1,2,3, 4,5,6},
                TimeOfDayHour = 26,
                TimeOfDayMinute = 17,
                Topic = "sample",
                Payload = "my lovely payload!",
                Timezone = "Asia/Jerusalem"

            });

string resultMessage = string.Empty;
if(result.Is<ScheduledTaskSubmitted>(out var response)) 
    resultMessage = response.Message.TaskId;
else if(result.Is<OperationFailed>(out var failedResponse) 
    resultMessage =  string.Join(Environment.NewLine, failedResponse.Message.Messages);
```


8. Finally, you MUST document the relevant queue messages for you microservice so that other developers will be able to know (same as we have for Rest API's swagger/OpenAPI). For now we're documenting in the project README file, however soon it will be transformed to a standard.
See sample for documentation on https://dev.azure.com/ta-9/_git/Argus?path=%2FNetCore%2FAlbert.Services%2Fsrc%2FServices%2FScheduler%2FSchedulerService.API&version=GBlod_39626_schedule_ms&_a=contents

9. Before running, make sure the queue is up & running, see https://dev.azure.com/ta-9/_git/Argus?path=%2FNetCore%2FAlbert.Services%2Fsrc%2FServices%2FScheduler%2FSchedulerService.API&version=GBlod_39626_schedule_ms&_a=contents
