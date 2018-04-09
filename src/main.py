from tdg.javascript_tdg import JavascriptTdg
from tdg.profile_cookies_tdg import ProfileCookiesTdg
from tdg.http_redirects_tdg import HttpRedirectsTdg
from tdg.http_requests_tdg import HttpRequestsTdg
from tdg.http_responses_tdg import HttpResponsesTdg
from tdg.abstract_tdg import DatabaseEnum
import numpy


class ProtectionPolicyEnum:
    HIGH = {
        "save_all_content": False,
        "cp_instrument": False,
        "js_instrument": True,
        "cookie_instrument": False,
        "disconnect": False,
        "bot_mitigation": False,
        "https-everywhere": False,
        "ghostery": True,
        "http_instrument": True,
        "prefs": {},
        "donottrack": False,
        "save_javascript": False,
        "random_attributes": False,
        "profile_archive_dir": None,
        "ublock-origin": False,
        "extension_enabled": True,
        "adblock-plus": False,
        "tracking-protection": False,
        "disable_flash": False,
        "profile_tar": None,
        "tp_cookies": "never",
        "headless": False,
        "browser": "firefox"
    }

    LOW = {
        "save_all_content": False,
        "cp_instrument": False,
        "js_instrument": True,
        "cookie_instrument": False,
        "disconnect": False,
        "bot_mitigation": False,
        "https-everywhere": False,
        "ghostery": False,
        "http_instrument": True,
        "prefs": {},
        "donottrack": False,
        "save_javascript": False,
        "random_attributes": False,
        "profile_archive_dir": None,
        "ublock-origin": False,
        "extension_enabled": True,
        "adblock-plus": False,
        "tracking-protection": False,
        "disable_flash": False,
        "profile_tar": None,
        "tp_cookies": "always",
        "headless": False,
        "browser": "firefox"
    }


def fetch_data(database, protection_policy):
    javascript_list = JavascriptTdg(database).select()
    javascript_list = [x for x in javascript_list if x.crawl_id == protection_policy]

    profile_cookies_list = ProfileCookiesTdg(database).select()
    profile_cookies_list = [x for x in profile_cookies_list if x.crawl_id == protection_policy]

    http_redirect_list = HttpRedirectsTdg(database).select()
    http_redirect_list = [x for x in http_redirect_list if x.crawl_id == protection_policy]

    http_request_list = HttpRequestsTdg(database).select()
    http_request_list = [x for x in http_request_list if x.crawl_id == protection_policy]

    http_response_list = HttpResponsesTdg(database).select()
    http_response_list = [x for x in http_response_list if x.crawl_id == protection_policy]

    dictionary = {
        'javascript': javascript_list,
        'profile_cookies': profile_cookies_list,
        'http_redirects': http_redirect_list,
        'http_requests': http_request_list,
        'http_responses': http_response_list
    }
    return dictionary


def get_analytics(lst1, lst2):
    a = set(lst1)
    b = set(lst2)
    return b.difference(a), a.intersection(b)


"""

RAW DATA

"""


data_dict = {
    'unsecure':{
        'home': fetch_data(DatabaseEnum.HOME, ProtectionPolicyEnum.LOW),
        'concordia': fetch_data(DatabaseEnum.CONCORDIA, ProtectionPolicyEnum.LOW),
        'tim_hortons': fetch_data(DatabaseEnum.TIM_HORTONS, ProtectionPolicyEnum.LOW)
        },
    'secure':{
        'home': fetch_data(DatabaseEnum.HOME, ProtectionPolicyEnum.HIGH),
        'concordia': fetch_data(DatabaseEnum.CONCORDIA, ProtectionPolicyEnum.HIGH),
        'tim_hortons': fetch_data(DatabaseEnum.TIM_HORTONS, ProtectionPolicyEnum.HIGH)
    },
}

for key in data_dict:
    print('**{}**'.format(key.upper()))
    for k1 in data_dict[key]:
        print('--------------------\nHotspot: {}\n--------------------'.format(k1))
        for k2 in data_dict[key][k1]:
            print('{}: {}'.format(k2, len(data_dict[key][k1][k2])))
    print()


"""

DIFFERENCE AND INTERSECTION

"""


http_requests = get_analytics(data_dict['unsecure']['home']['http_requests'], data_dict['unsecure']['tim_hortons']['http_requests'])
http_responses = get_analytics(data_dict['unsecure']['home']['http_responses'], data_dict['unsecure']['tim_hortons']['http_responses'])
javascript = get_analytics(data_dict['unsecure']['home']['javascript'], data_dict['unsecure']['tim_hortons']['javascript'])

analytic_dict = {
    'set_difference': {
        'http_responses': http_responses[0],
        'http_requests': http_requests[0],
        'javascript': javascript[0]
    },
    'set_intersection': {
        'http_responses': http_responses[1],
        'http_requests': http_requests[1],
        'javascript': javascript[1]
    }
}

for key in analytic_dict:
    print('**{} between Tim Hortons and Home (unsecure)**'.format(key.upper()))
    for k1 in analytic_dict[key]:
        print('{}: {}'.format(k1, len(analytic_dict[key][k1])))
    print()


"""

REQUESTS

"""


collection_dict = {
    'home':{

    },
    'tim_hortons':{

    }
}
tim_list = data_dict['unsecure']['tim_hortons']['http_requests']
home_list = data_dict['unsecure']['home']['http_requests']

for element in tim_list:
    e = str(element).split(': ')
    if e[0] not in collection_dict['tim_hortons']:
        collection_dict['tim_hortons'][e[0]] = []
    collection_dict['tim_hortons'][e[0]].append(e[1])

for element in home_list:
    e = str(element).split(': ')
    if e[0] not in collection_dict['home']:
        collection_dict['home'][e[0]] = []
    collection_dict['home'][e[0]].append(e[1])

ordered_home_list = []
ordered_tims_list = []

for key in collection_dict['home']:
    tpl = [key, len(collection_dict['home'][key])]
    ordered_home_list.append(tpl)

for key in collection_dict['tim_hortons']:
    tpl = [key, len(collection_dict['tim_hortons'][key])]
    ordered_tims_list.append(tpl)

ordered_home_list.sort(key=lambda x: x[1], reverse=True)
ordered_tims_list.sort(key=lambda x: x[1], reverse=True)
avg_home = numpy.average([x[1] for x  in ordered_home_list])
avg_tims = numpy.average([x[1] for x  in ordered_tims_list])

final_home_list = [x for x in ordered_home_list if x[1] >= avg_home]
final_tims_list = [x for x in ordered_home_list if x[1] >= avg_tims]

other_home = 0
for e in ordered_home_list:
    if e[1] < avg_home:
        other_home += e[1]

other_tims = 0
for e in ordered_tims_list:
    if e[1] < avg_tims:
        other_tims += e[1]

final_home_list.append(['other', other_home])
final_tims_list.append(['other', other_tims])

print('Home requests')
for e in final_home_list:
    print(e[0] + '\t' + str(e[1]))
print()

print('Time Hortons requests')
for e in final_tims_list:
    print(e[0] + '\t' + str(e[1]))
print()

"""

REDIRECTION

"""

redirect_dict = {
    'home':{

    },
    'tim_hortons':{

    }
}

tim_list = data_dict['unsecure']['tim_hortons']['http_redirects']
home_list = data_dict['unsecure']['home']['http_redirects']

for element in tim_list:
    e = str(element).split(': ')
    if e[1] not in redirect_dict['tim_hortons']:
        redirect_dict['tim_hortons'][e[1]] = []
    redirect_dict['tim_hortons'][e[1]].append(e[0])

for element in home_list:
    e = str(element).split(': ')
    if e[1] not in redirect_dict['home']:
        redirect_dict['home'][e[1]] = []
    redirect_dict['home'][e[1]].append(e[0])

ordered_home_list = []
ordered_tims_list = []

for key in redirect_dict['home']:
    tpl = [key, len(redirect_dict['home'][key])]
    ordered_home_list.append(tpl)

for key in redirect_dict['tim_hortons']:
    tpl = [key, len(redirect_dict['tim_hortons'][key])]
    ordered_tims_list.append(tpl)

ordered_home_list.sort(key=lambda x: x[1], reverse=True)
ordered_tims_list.sort(key=lambda x: x[1], reverse=True)
avg_home = numpy.average([x[1] for x in ordered_home_list])
avg_tims = numpy.average([x[1] for x in ordered_tims_list])

final_home_list = [x for x in ordered_home_list if x[1] >= avg_home]
final_tims_list = [x for x in ordered_home_list if x[1] >= avg_tims]

other_home = 0
for e in ordered_home_list:
    if e[1] < avg_home:
        other_home += e[1]

other_tims = 0
for e in ordered_tims_list:
    if e[1] < avg_tims:
        other_tims += e[1]

final_home_list.append(['other', other_home])
final_tims_list.append(['other', other_tims])


print('Home redirects')
for e in final_home_list:
    print(e[0] + '\t' + str(e[1]))
print()

print('Tim Hortons redirects')
for e in final_tims_list:
    print(e[0] + '\t' + str(e[1]))
print()


"""

THIRD PARTY CHANNELS


"""


tim_list = data_dict['unsecure']['tim_hortons']['http_requests']
home_list = data_dict['unsecure']['home']['http_requests']

third_party = 0
for i in tim_list:
    if i.is_third_party_channel == 1:
        third_party += 1
print("Third party requests on Tim Hortons hotspot: {}%".format(100 * third_party / len(tim_list)))

third_party = 0
for i in home_list:
    if i.is_third_party_channel == 1:
        third_party += 1
print("Third party requests on Home hotspot: {}%".format(100 * third_party / len(home_list)))