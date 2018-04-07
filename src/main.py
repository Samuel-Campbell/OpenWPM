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


def pprint(dictionary):
    for key in dictionary:
        print('**{}**'.format(key.upper()))
        for k1 in dictionary[key]:
            print('--------------------\nHotspot: {}\n--------------------'.format(k1))
            for k2 in dictionary[key][k1]:
                print('{}: {}'.format(k2, len(dictionary[key][k1][k2])))
        print()



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
    }
}

pprint(data_dict)
