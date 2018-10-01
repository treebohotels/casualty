# Corelated logs
In microservices world we need a common request id to tie all log events together so that we can retrieve nessesary information from logs ,this libraray help to set and log request-id on  for requests and propgat it to all other outbound request (celery,kombu ,other http request)

##### Lets see how it works
It works in three step
-   Use middleware to add request id header to all incoming request if it is not there
-   Use structlog https://github.com/hynek/structlog to bind the request_id to logger ,so that request_id is present in each log record
-   Patch functions at runtime to add request_id header  to all outgoing request (celery,kombu,request)



##### Examples:
Add Corelation middleware and patch outgoing request modules
For Flask
```
app = Flask(__name__)
app.wsgi_app = FlaskCorelationMiddleWare(app.wsgi_app)
patch(['requests','kombu'])  #for celery patch kombu
```

###### See structlog documentation if you want ot customize your logger
Replace you logger with structlog :
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

This will automaticaly start adding request_id to your logs and and header to all outbounf request.

For celery consumer, bind request_id like this
```
logger = structlog.wrap_logger(logger=logger)
@app.task(bind=True) # bind the task
def add(self,x, y):
    logger = logger.bind(request_id=self.request.X_CO_REQUEST_ID)

    return x,y
```

For kombu consumer tie request_id like this
```
logger = structlog.wrap_logger(logger=logger)
def process_message(body, message):
  print("The body is {}".format(body))
  logger = logger.bind(request_id=message.headers['X_CO_REQUEST_ID'])
  message.ack()

```



