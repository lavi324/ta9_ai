# Intro
Currently, on Albert, we're using Rabbit MQ as our message queue implementation.
Rabbit MQ is a modern queue containing all the features required for our needs currently.

RabbitMQ is an Open-source message broker software that implements the advance message queuing protocol(AMPQ).
Written in Erlang programming language and its build on the open Telecom platform framework for clustering and failover.
Producer – a program that sends messages.
Consumer – a program that mostly waits to receive messages.
Queue- a large message buffer that bound by the host memory & disk. Many Producers/Consumers can send/receive data from the queue.

![rabbitmqpq.png](/.attachments/rabbitmqpq-4c715b83-1cc8-43d1-b46f-c96538f513e1.png)

# Launching RabbitMQ
## Docker Image
To start Rabbit MQ as a docker container, we're using [official docker image/s](https://hub.docker.com/_/rabbitmq)
Here's a basic docker image launch command:
`$ docker run -d --hostname my-rabbit --name some-rabbit -e RABBITMQ_DEFAULT_USER=rabbit -e RABBITMQ_DEFAULT_PASS=rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management`
(15672 - This port must be configured to use management)

This will trigger a container running RabbitMQ with a management console (web-based). 
Once the container is up & running, we can:
1. **Access its management console** by browsing the http://DOCKER_HOST:15672
![RabbitMQUI.png](/.attachments/RabbitMQUI-7dd6d3bf-6d3f-45fd-b50e-7b77e663bbea.png)
1. **Connect to the queue** and start publishing/consuming messages

## Windows Machine (no docker)
1. install Erlang latest stable 64bit version from [here](https://erlang.org/download/otp_win64_23.1.5.exe)
1. Download & Install RabbitMQ server from [here](https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.8.9/rabbitmq-server-3.8.9.exe)
2.1 Open elevated command line and `cd` to `$RABBIT_HOME$/sbin` and run:
`rabbitmq-plugins enable rabbitmq_management`
2.2 Restart **RabbitMQ** _Windows Service_ 

Now RabbitMQ can be accessed as described above.

# Important Commands and tips
- Store data on “Node Name” which defaults to the host name . we should specify -h/--hostname explicitly for each daemon so that we don’t get a random hostname and can keep track of the data.
`$ docker run -d --hostname my-rabbit --name some-rabbit rabbitmq:3`


