# from mock import Mock
#
# from casualty.flask_corelation_middleware import FlaskCorelationMiddleWare
#
#
# def test_flask_corelation_middleware(self):
#
#     request = Mock()
#     request.headers={}
#     request.META = {
#         "HTTP_PROFILE_ID": self.profileId,
#         "REQUEST_METHOD": "POST",
#         "HTTP_OPERATING_SYSTEM_VERSION": "ICE CREAM",
#         "HTTP_PLATFORM": "ANDROID",
#         "HTTP_APP_VERSION": "1.0.0",
#         "HTTP_USER_AGENT": "AUTOMATED TEST"
#     }
#     request.path = '/testURL/'
#     request.session = {}
#
#     FlaskCorelationMiddleWare()
#
#     print(123)
