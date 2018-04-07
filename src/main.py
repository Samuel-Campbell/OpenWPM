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
        "https-everywhere": True,
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
        "https-everywhere": True,
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

def fetch_data(database):
    dictionary = {
        'javascript': JavascriptTdg(database).select(),
        'profile_cookies': ProfileCookiesTdg(database).select(),
        'http_redirects': HttpRedirectsTdg(database).select(),
        'http_requests': HttpRequestsTdg(database).select(),
        'http_responses': HttpResponsesTdg(database).select()
    }
    return dictionary


def pprint(dictionary):
    for key in dictionary:
        print('--------------------\nHotspot: {}\n--------------------'.format(key))
        for k in dictionary[key]:
            print('{}: {}'.format(k, len(dictionary[key][k])))
        print()



data_dict = {
    'home': fetch_data(DatabaseEnum.HOME),
    'concordia': fetch_data(DatabaseEnum.CONCORDIA),
    'tim_hortons': fetch_data(DatabaseEnum.TIM_HORTONS)
}

pprint(data_dict)
