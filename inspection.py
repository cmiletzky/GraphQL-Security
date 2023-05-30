from enum import Enum

NUMBER_OF_REJECT = 1
NUMBER_OF_ACCEPT = 10
RULE_TYPE = Enum('RULE_TYPE', ['FUNCTION', 'IP', 'USER_AGENT'])
ACTION = Enum('ACTION', ['ACCEPT', 'REJECT'])

LIST_OF_SUSPICIOUS_USER_AGENT = [
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64)",
    "AppleWebKit/537.36 (KHTML, like Gecko)",
    "Chrome/58.0.3029.110",
    "Safari/537.36 SE 2.X",
    "MetaSr 1.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "AppleWebKit/537.36 (KHTML, like Gecko)",
    "Chrome/42.0.2311.135",
    "Safari/537.36",
    "Edge/12.246",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0)",
    "Gecko/20100101",
    "Firefox/52.0",
    "Mozilla/5.0 (compatible; MJ12bot/v1.4.8; http://mj12bot.com/)",
    "Mozilla/5.0 (compatible; SemrushBot/7~bl; +http://www.semrush.com/bot.html)",
    "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0)"
]


class RawRequest:
    def __init__(self, request):
        self.body = request.split("\n\n")[1]
        self.ip = request.split("X-Forwarded-For: ")[1].split("\n")[0]
        self.user_agent = request.split("User-Agent: ")[1].split("\n")[0]

    def get_body(self):
        return self.body

    def get_ip(self):
        return self.ip

    def get_user_agent(self):
        return self.user_agent


class Rule:
    def __init__(self, action, rule_type, data):
        self.action = action
        self.rule_type = rule_type
        self.data = data


class Function:
    def __init__(self, func_name, params):
        self.func_name = func_name
        self.params = params


class Request:
    def __init__(self, query, ip):
        self.func_name = get_func_name(query)
        try:
            self.params = []
            params = query.split("{")[1].split("(")[1].replace(")", "").replace(" ", "").split(",")
            for param in params:
                self.params.append(param.split(":")[0])
        except:
            self.params = None
        self.total_counter = 1
        self.ip_dict = {ip: 1}

    def add_appearance(self, ip):
        self.total_counter += 1
        if ip in self.ip_dict:
            self.ip_dict[ip] += 1
        else:
            self.ip_dict[ip] = 1

    def get_func_name(self):
        return self.func_name

    def get_params(self):
        return self.params

    def get_ip_dict(self):
        return self.ip_dict


def get_func_name(query):
    return query.split("{")[1].split("(")[0].replace(" ", "").replace("\n", "")


def organize(lst):
    dict_of_requests = {}
    for raw_request in lst:
        request = RawRequest(raw_request)
        if request.get_user_agent() in LIST_OF_SUSPICIOUS_USER_AGENT:
            continue
        func_name = get_func_name(request.get_body())
        if func_name in dict_of_requests:
            dict_of_requests[func_name].add_appearance(request.get_ip())
        else:
            dict_of_requests[func_name] = Request(request.get_body(), request.get_ip())
    return dict_of_requests


def create_rules(dict_of_requests):
    rules = []
    suspicious_ip = {}
    for agent in LIST_OF_SUSPICIOUS_USER_AGENT:
        rules.append(Rule(ACTION['REJECT'], RULE_TYPE['USER_AGENT'], agent))
    for request in dict_of_requests.values():
        if len(request.get_ip_dict()) <= NUMBER_OF_REJECT:
            for ip in request.get_ip_dict():
                if ip in suspicious_ip and suspicious_ip[ip] == 1:
                    suspicious_ip[ip] += 1
                    rules.append(Rule(ACTION['REJECT'], RULE_TYPE['IP'], ip))
                elif ip not in suspicious_ip:
                    suspicious_ip[ip] = 1
    for request in dict_of_requests.values():
        if len(request.get_ip_dict()) >= NUMBER_OF_ACCEPT:
            function = Function(request.get_func_name(), request.get_params())
            rules.append(Rule(ACTION['ACCEPT'], RULE_TYPE['FUNCTION'], function))
    return rules


def main():
    lst = []
    with open('requests.txt') as f:
        lines = "".join(f.readlines()).split("*****")
        for line in lines:
            if line:
                lst.append(line.replace("\n", "", 1))

    dict_of_requests = organize(lst)
    rules = create_rules(dict_of_requests)

    with open('rules.txt', 'w') as f:
        for rule in rules:
            if rule.rule_type == RULE_TYPE['FUNCTION']:
                str_rule = str(rule.rule_type)+" "+str(rule.action)+" "+rule.data.func_name+" "+str(rule.data.params)
            else:
                str_rule = str(rule.rule_type) + " " + str(rule.action) + " " + rule.data
            f.write(str_rule + '\n')


if __name__ == "__main__":
    main()
