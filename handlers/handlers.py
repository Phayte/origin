# class Handler(object):
#     DB_HANDLER_NAME = "handler"
#
#     def __init__(self, obj):
#         self.obj = obj
#         self.db_dict = obj.attributes.get(self.DB_HANDLER_NAME, {})
#
#     def __getattr__(self, item):
#         if item in self.db_dict:
#             return self.db_dict(item)
#         return None
#
#     def __setattr__(self, key, value):
#         self.db_dict[key] = value
#
#     def __delattr__(self, item):
#         del self.db_dict[item]
