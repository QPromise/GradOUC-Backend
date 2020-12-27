str = '\xe9\xaa\xa8\xe7\xb2\xbe\xe7\x81\xb5\xe7\x9a\x84\xe5\xb0\x8f\xe5\x8f\xaf\xe7\x88\xb1'
res = str.encode('raw_unicode_escape').decode('utf-8')
print(res)
import time
import datetime
print( time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()))
# pre_course_name = ""
# pre_course_room = ""
# begin = 0
# end = 0
# cur_course_info = dict()
# while end < 12:
#     if courses_info[end] == '':
#         # 现在这个没课，如果之前有课程
#         if pre_course_name != "":
#             cur_course_info["name"] = pre_course_name
#             cur_course_info["room"] = pre_course_room
#             if begin == end - 1:
#                 cur_course_info["span"] = "%s" % begin
#             else:
#                 cur_course_info["span"] = "%s-%s" % (begin, end - 1)
#             begin = end
#             day_courses.append(cur_course_info)
#             cur_course_info = dict()
#             pre_course_name = ""
#             pre_course_room = ""
#         # 现在这个没课，如果之前也没有课程
#         else:
#             begin = end
#     else:
#         cur_course_split = courses_info[end].split()
#         # 如果之前没课，现在有课
#         if pre_course_name == "":
#             pre_course_name = cur_course_split[0]
#             pre_course_room = cur_course_split[-1]
#             begin = end
#         # 如果之前有课，现在也有课
#         else:
#             if pre_course_name != cur_course_split[0]:
#                 cur_course_info["name"] = pre_course_name
#                 cur_course_info["room"] = pre_course_room
#                 if begin == end - 1:
#                     cur_course_info["span"] = "%s" % begin
#                 else:
#                     cur_course_info["span"] = "%s-%s" % (begin, end - 1)
#                 pre_course_name = cur_course_split[0]
#                 pre_course_room = cur_course_split[-1]
#                 begin = end
#                 day_courses.append(cur_course_info)
#                 cur_course_info = dict()
#             else:
#                 cur_course_info["name"] = pre_course_name
#                 cur_course_info["room"] = pre_course_room
#                 if begin == end - 1:
#                     cur_course_info["span"] = "%s" % begin
#                 else:
#                     cur_course_info["span"] = "%s-%s" % (begin, end - 1)
#     end += 1
# # if cur_course_info.get("name", None) is not None:
# #     if len(day_courses) != 0 and cur_course_info["name"] != day_courses[-1]["name"]:
# day_courses.append(cur_course_info)
# print(day_courses)
# exit()