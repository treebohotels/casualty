# from casualty.django_corelation_middleware import DjangoCorelationMiddleware
# from mock import Mock
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
#     DjangoCorelationMiddleware().process_request(request)
#
#     print(123)
