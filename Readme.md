# Casualty - Logging with request identifiers
[![image](https://img.shields.io/pypi/v/casualty.svg)](https://pypi.org/project/casualty/)
[![image](https://img.shields.io/pypi/l/casualty.svg)](https://pypi.org/project/casualty/)
[![image](https://img.shields.io/pypi/pyversions/casualty.svg)](https://pypi.org/project/casualty/)
[![image](https://img.shields.io/github/contributors/treebohotels/casualty.svg)](https://github.com/treebohotels/casualty/graphs/contributors)
[![codecov.io](https://codecov.io/github/treebohotels/casualty/coverage.svg?branch=master)](https://codecov.io/github/treebohotels/casualty)



Tracing a request from start to end is critical for diagnosing issues quickly. This becomes hard when you have a highly
concurrent system because logs are interspersed with each other. It becomes even harder when you are in the microservices
architecture where a request may travel through multiple services before being complete. 

In order to diagnose in such an environment, we need to have a unique identifier to tie up all the logs through different
services. Casualty helps you do exactly that. It generates a unique X_CO_REQUEST_ID for every request and logs it whenever
you log something from your python code base. It also propagates the id to outbound requests. If a request already has 
a X_CO_REQUEST_ID set in its headers, it reuses it. Hence, using Casualty, you can stitch together requests from start 
to end through multiple services.

##### Library support
Django, Flask, Requests, Celery & Kombu. 

##### How it works
Three simple steps
-   Use the provided framework specific middlewares to add the request_id (X_CO_REQUEST_ID) header to all incoming request if it is not already there
-   Use [structlog](https://github.com/hynek/structlog) to bind the request_id to the logger so that the request_id is present in each log record
-   Patch functions at runtime to add request_id header to all outgoing requests (celery, kombu, request)



##### Examples:
For configure a Flask application, add the middleware and patch outgoing request modules.
```python
import Flask
from casualty.flask_corelation_middleware import FlaskCorelationMiddleWare
from casualty.patcher import patch


app = Flask(__name__)
app.wsgi_app = FlaskCorelationMiddleWare(app.wsgi_app)
patch(['requests'])

######
Add below filter 
```casualty.filter.RequestIDFilter```
to your loggers which will add requets id to all your requests.
Something like this.
```
    logging_conf = {
        "version": 1,
        "filters": {
            "request_id": {"()": "casualty.filter.RequestIDFilter"}
        },
        ... Your code
```
Do the same where the request is received if you want to log the request id except the patching part.
This will automatically start adding request_id to your logs and to the HTTP headers to all outbound requests.

For Kombu consumers, patch Kombu and use structlog as below

```python
from casualty.patcher import patch 
patch(['requests','kombu']) 
```

```python
import logging
from casualty import casualty_logger

logger =logging.getLogger()

def process_message(body, message):
  logger.info("The body is {}".format(body))
  logger.info('message')
  message.ack()
```

For Celery consumer, note that we will need to initialize structlog as well as bind the request_id 

```python
from casualty.patcher import patch 

patch(['requests','kombu']) 
```

```python
from casualty import casualty_logger
import logging
from casualty.constants import REQUEST_HEADER

logger = logging.getLogger()

@app.task(bind=True) # bind the task
def add(self,x, y):
    global logger
    logger = logger.bind(request_id=self.request.__dict__[REQUEST_HEADER])
    return x,y
```



