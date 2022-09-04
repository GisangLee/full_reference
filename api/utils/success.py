from re import L


class Success(object):
    def __set_response(self, cls_name, req_method, msg, code):

        self.__response = {
            "action": cls_name,
            "method": req_method,
            "message": msg,
            "code": code,
        }

    @classmethod
    def response(cls, cls_name, req_method, msg, code):

        Success.__set_response(cls, cls_name, req_method, msg, code)

        return Success.__response
