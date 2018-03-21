from __future__ import absolute_import
from automation import TaskManager, CommandSequence
from six.moves import range
import itertools


class OpenWpm:
    parameters = {
        'http_instrument': {
            'combinations': [True],
            'index': -1
        },
        'js_instrument': {
            'combinations': [True],
            'index': -1
        },
        'disable_flash': {
            'combinations': [False],
            'index': -1
        },
        'tp_cookies': {
            'combinations': ['always', 'never', 'from_visited'],
            'index': -1
        },
        'ghostery': {
            'combinations': [True, False],
            'index': -1
        },
        'https-everywhere': {
            'combinations': [True, False],
            'index': -1
        },
    }
    sites = ['http://www.concordia.ca/',
             'http://www.reddit.com/',
             'http://www.amazon.ca/',
             'http://www.ebay.com/',
             'http://www.facebook.com/',
             'http://www.businessinsider.com/',
             'http://montrealgazette.com/',
             'http://www.theweathernetwork.com/ca/weather/quebec/montreal',
             'http://www.aircanada.com/ca/en/aco/home.html',
             'http://gmail.com',
             'http://youtube.com',
             'http://en.wikipedia.org/wiki/Wikipedia',
             'http://twitter.com/',
             'http://www.twitch.tv/',
             'https://www.xnxx.com',
             'http://www.instagram.com/',
             'http://www.linkedin.com/',
             'http://www.netflix.com',
             'http://www.microsoft.com/en-ca/',
             'http://thepiratebay.org/browse',
             'http://news.ycombinator.com/',
             'http://thehackernews.com/',
             'http://www.securityforum.org/events/webinars/network-security-and-hacking-2/',
             'http://www.deepdotweb.com/marketplace-directory/listing/gobotal-black-market/',
             'http://myspace.com/',
             'http://crohasit.com/dragon-ball-xenoverse-free-download/?',
             'http://www.batmanstream.net/other-live-streaming-video-8.html',
             'http://www.purevpn.com/blog/ufc-live-streaming/',
             'http://www.blizzard.com/en-us/',
             'http://games.torrentsnack.com/assassins-creed-pc/',
             'http://crotorrents.com/assassins-creed-2-torrent-download/',
             'http://pornhub.com',
             'http://www.montrealracing.com/wp/',
             'http://aliexpress.com',
             'http://www.stealmylogin.com/',
             'http://www.facebok.com/'
             ]

    def __init__(self):
        self.manager = None
        param_list = []
        index = 0
        for key in self.parameters:
            param_list.append(self.parameters[key]['combinations'])
            self.parameters[key]['index'] = index
            index += 1
        combinations = [p for p in itertools.product(*param_list)]
        manager_params, browser_params = TaskManager.load_default_params(len(combinations))
        self.setup(combinations, manager_params, browser_params)

    def setup(self, combinations, manager_params, browser_params):
        manager_params['data_directory'] = '~/Documents/openWpmDb/'
        manager_params['log_directory'] = '~/Desktop/'
        for i in range(len(combinations)):
            browser_params[i]['http_instrument'] = combinations[i][self.parameters['http_instrument']['index']]
            browser_params[i]['js_instrument'] = combinations[i][self.parameters['js_instrument']['index']]
            browser_params[i]['disable_flash'] = combinations[i][self.parameters['disable_flash']['index']]
            browser_params[i]['tp_cookies'] = combinations[i][self.parameters['tp_cookies']['index']]
            browser_params[i]['ghostery'] = combinations[i][self.parameters['ghostery']['index']]
            browser_params[i]['https-everywhere'] = combinations[i][self.parameters['https-everywhere']['index']]
        self.manager = TaskManager.TaskManager(manager_params, browser_params)

    def browse(self):
        # stateful crawl
        for site in self.sites:
            command_sequence = CommandSequence.CommandSequence(site)
            command_sequence.get(sleep=0, timeout=60)
            command_sequence.dump_profile_cookies(120)
            self.manager.execute_command_sequence(command_sequence, index='**')

        # stateless crawl
        for site in self.sites:
            command_sequence = CommandSequence.CommandSequence(site, reset=True)
            command_sequence.get(sleep=10, timeout=15)
            command_sequence.dump_profile_cookies(120)
            self.manager.execute_command_sequence(command_sequence, index='**')
        self.manager.close()


if __name__ == "__main__":
    openwpm = OpenWpm()
    openwpm.browse()
