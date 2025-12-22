[[_TOC_]]


# Intro
A message queue is a component that enables to send/publish messages between backend component with or without getting a response.
There are some clear advantages of using a message queue to communicate between microservices, such as message persist, tracking of messages, retries and many more.

# Types of Communications
Some services may use the queue for consuming messages while others for publishing/sending messages. Others may use the queue for both consuming and publishing messages. 
Let's go over the possible communication types on the queue:
1. Request/Response - The messages queue can be used to communicate between services using a request/response mechanism, ie - instead of calling a service's API, we can communicate with a microservice using the queue transport to earn all the mentioned advantages
1. Send - send a message to the queue to be handled by one consumer, ie - once the message is collected by a consumer (to be handled) it removed from the qeueu (upon successfull handling)
1. Publish - publishes (broadcast) a message to the queue to be handled by as many consumers registered to this kind of message

 
# Additional queue documentation
Good walkthrough to get know message queues' main topics [here](https://www.cloudamqp.com/blog/2015-05-18-part1-rabbitmq-for-beginners-what-is-rabbitmq.html) (focusing on RabbitMQ)

# Current Status
Currently on Albert we're using Rabbit MQ as our message queue implementation.
More queues implementation support is to be added, such as Kafka (though for other purposes), ActiveMQ, Azure Service Bus
