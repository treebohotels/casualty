# Corelated logs
In microservices world we need a common request id to tie all log events together so that we can retrieve nessesary information from logs ,this libraray help to set and log request-id on  for requests and propgat it to all other outbound request (celery,kombu ,other http request)

##### Lets see how it works
It works in three step
-   Use middleware to add request_id(X_CO_REQUEST_ID) header to all incoming request if it is not there
-   Use structlog https://github.com/hynek/structlog to bind the request_id to logger ,so that request_id is present in each log record
-   Patch functions at runtime to add request_id header  to all outgoing request (celery,kombu,request)



##### Examples:
Add Corelation middleware and patch outgoing request modules
For Flask
```
app = Flask(__name__)
app.wsgi_app = FlaskCorelationMiddleWare(app.wsgi_app)
patch(['requests','kombu'])  #patch kombu if you are using celery 
```

###### See structlog documentation if you want ot customize your logger
Replace you logger with structlog logger:
Previously:
```
logger = logging.getLogger()
logger.setLevel(INFO)
logger.addHandler(StreamHandler())
```
Now:
```
logger = logging.getLogger()
logger.setLevel(INFO)
logger.addHandler(StreamHandler())
logger = structlog.wrap_logger(logger=logger)
```

This will automaticaly start adding request_id to your logs and and header to all outbound request.

For kombu consumer patch kombu and use structlog as below
```
from corelated_logs.patcher import patch 
patch(['requests','kombu']) 
```

```
logger=logging.getLogger()
logger = structlog.wrap_logger(logger=logger)
def process_message(body, message):
  print("The body is {}".format(body))
  logger = logger.info('message')
  message.ack()

```



For celery consumer,note that we need to initailize structlog as well,and  bind request_id 

```
from corelated_logs.patcher import patch 
patch(['requests','kombu']) 
```

```
structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="ISO"),
            structlog.processors.JSONRenderer(),
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    

logger=logging.getLogger()
logger = structlog.wrap_logger(logger=logger)
@app.task(bind=True) # bind the task
def add(self,x, y):
    global logger
    logger = logger.bind(request_id=self.request.__dict__[REQUEST_HEADER])

    return x,y
```




