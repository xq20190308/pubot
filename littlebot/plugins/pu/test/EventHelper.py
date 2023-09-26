import grequests

import parseConfig

event_list = [grequests.get(
    parseConfig.url_eventList() + f"&oauth_token={parseConfig.token_oauth_token()}&oauth_token_secret={parseConfig.token_oauth_token_secret()}&version={parseConfig.version()}&page={i + 1}")
              for i in range(1)]
res_event_lists = grequests.map(event_list)
all_event_list = ""
for res_event_list in res_event_lists:

    print(type(res_event_list.ok))