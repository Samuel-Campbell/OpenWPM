from tdg.javascript_tdg import JavascriptTdg
from tdg.profile_cookies_tdg import ProfileCookiesTdg
from tdg.http_redirects_tdg import HttpRedirectsTdg
from tdg.http_requests_tdg import HttpRequestsTdg
from tdg.http_responses_tdg import HttpResponsesTdg
from tdg.abstract_tdg import DatabaseEnum


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
        "tp_cookies": "always",
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

http_redirects = get_analytics(data_dict['unsecure']['home']['http_redirects'], data_dict['unsecure']['tim_hortons']['http_redirects'])
http_requests = get_analytics(data_dict['unsecure']['home']['http_requests'], data_dict['unsecure']['tim_hortons']['http_requests'])
http_responses = get_analytics(data_dict['unsecure']['home']['http_responses'], data_dict['unsecure']['tim_hortons']['http_responses'])
javascript = get_analytics(data_dict['unsecure']['home']['javascript'], data_dict['unsecure']['tim_hortons']['javascript'])

analytic_dict = {
    'set_difference': {
        'http_responses': http_responses[0],
        'http_requests': http_requests[0],
        'http_redirects': http_redirects[0],
        'javascript': javascript[0]
    },
    'set_intersection': {
        'http_responses': http_responses[1],
        'http_requests': http_requests[1],
        'http_redirects': http_redirects[1],
        'javascript': javascript[1]
    }
}

for key in analytic_dict:
    print('**{} between Tim Hortons and Home (unsecure)**'.format(key.upper()))
    for k1 in analytic_dict[key]:
        print('{}: {}'.format(k1, len(analytic_dict[key][k1])))
    print()


collection_dict = {
    'home':{

    },
    'tim_hortons':{

    }
}
diff_list = analytic_dict['set_difference']['http_requests']
intersection_list = analytic_dict['set_intersection']['http_requests']

for element in diff_list:
    e = str(element).split(': ')
    if e[0] not in collection_dict['tim_hortons']:
        collection_dict['tim_hortons'][e[0]] = []
    collection_dict['tim_hortons'][e[0]].append(e[1])

for element in intersection_list:
    e = str(element).split(': ')
    if e[0] not in collection_dict['home']:
        collection_dict['home'][e[0]] = []
    collection_dict['home'][e[0]].append(e[1])

for key in collection_dict:
    print('**Data collection from {}**'.format(key))
    for k1 in collection_dict[key]:
        print('{} has performed {} requests'.format(k1, len(collection_dict[key][k1])))
    print()

