# Corelated logs
In microservices world we need a common request id to tie all log events together so that we can retrieve nessesary information from logs ,this libraray help to set and log request-id on  for requests and propgat it to all other outbound request (celery,kombu ,other http request)

##### Lets see how it works
It works in three step
-   Use middleware to add request id header to all incoming request if it is not there
-   Use structlog https://github.com/hynek/structlog to bind the request_id to logger ,so that request_id is present in each log record
-   Patch functions at runtime to add request_id header  to all outgoing request (celery,kombu,request)



##### Examples:
###### Flask