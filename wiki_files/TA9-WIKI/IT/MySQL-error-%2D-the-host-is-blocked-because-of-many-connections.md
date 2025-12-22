[[_TOC_]]

#The problem
The client have a problem to log in to the system (intc2), the error occurred is : cannot connect to server
the event viewer error logs - 'host is blocked because of many connection errors'  

When, for whatever reason, MySQL cannot connect a client host for a configurable number of times (the default is 100), the client host is blocked from connecting the MySQL and must be unblocked manually.
To avoid the issue in the future (in intc2), the number of max connections increased from 100 to 1000000.

#The Solution
If the problem happens again, use mysqladmin flush-hosts, as stated in the error message, enter the root password upon the prompt:

mysqladmin flush-hosts -uroot -p
