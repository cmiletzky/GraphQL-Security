from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from enum import Enum
import binascii
import requests
from graphql import GraphQLError, build_ast_schema, parse, print_ast

# address of real Graphql server
Graphql_server = 'http://127.0.0.1:5000/graphql'

# Enum for the types of rules
RULE_TYPE = Enum('RULE_TYPE', ['FUNCTION', 'IP', 'USER_AGENT'])

# Enum for the actions (accept or reject)
ACTION = Enum('ACTION', ['ACCEPT', 'REJECT'])


class Rule:
    """
    Represents a rule for accepting or rejecting requests.
    """
    def __init__(self, action, rule_type, data):
        self.action = action
        self.rule_type = rule_type
        self.data = data


class Function:
    """
    Represents a function being called in a request.
    """
    def __init__(self, func_name, params):
        self.func_name = func_name
        self.params = params




# the port to listen on
PORT = 40000
# one func for testing rules
func = Function('getallBooks', None)
func1 = Function('available', ['bookId'])
func2 = Function('getBooksByAuthor', ['authorId'])
func3 = Function('getBookByName', ['bookName'])
func4 = Function('getAllAuthors', None)
func5 = Function('getUserDetails', ['userId'])
func6 = Function('getBooksHoldByUserId', ['userId'])
func7 = Function('getBooksHoldByUserName', ['userName'])
# MUTATIONS
mut1 = Function('addUser', ['name', 'email', 'phone', 'address'])
mut2 = Function('updateUser', ['userId', 'name', 'email', 'phone', 'address'])
mut3 = Function('addAuthor', ['name'])
mut4 = Function('addBook', ['name', 'author'])
mut5 = Function('borrowBook', ['bookId', 'userId'])
mut6 = Function('returnBook', ['bookId'])

rule1 = Rule('REJECT', 'IP', '1.1.1.1')
rule2 = Rule('REJECT', 'USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0')
rule3 = Rule('ACCEPT', 'FUNCTION', mut6)
rules = [rule1, rule2, rule3]


def inspect(src_ip, user_agent, func):
    for rule in rules:
        if rule.rule_type == 'IP' and rule.data == src_ip:
            if rule.action == 'REJECT':
                return False
            else:
                return True
        elif rule.rule_type == 'USER-AGENT' and rule.data == user_agent:
            if rule.action == 'REJECT':
                return False
            else:
                return True
            # I had to separate the comparion because we cant compare to Function object as is
            # TODO also need to solve the comparision of param as string because we
            # cont. extract it from the query, to the params sitting in Function object that represented as
            # cont. list
        elif rule.rule_type == 'FUNCTION' and rule.data.params == func.params and rule.data.func_name == func.func_name:
            if rule.action == 'REJECT':
                return False
            else:
                return True


def get_func_name(query):
    return query['data'].split("{")[1].split("(")[0].replace(" ", "").replace('\n', '')

def extract_func(query):
    func_name = get_func_name(query)
    try:
        params = []
        print(query.split("{")[1])
        params1 = query.split("{")[1].split("(")[1].replace(")", "").replace(" ", "").split(",")
        for param in params1:
            params.append(param.split(":")[0])
    except:
        params = None
    func = Function(func_name, params)
    return func

# the HTTP request handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # read the request body
        content_length = int(self.headers['Content-Length'])

        post_data = self.rfile.read(content_length)
        print(post_data)

        # extract X-Forwarded-For field from headers
        src_ip = self.headers.get('X-Forwarded-For')
        # print X-Forwarded-For field
        print(f'X-Forwarded-For: {src_ip}')

        user_agent = self.headers.get('User-Agent', '')
        print(f"User-Agent: {user_agent}")
        # parse the JSON data

        query = json.loads(post_data)
        print(query)
        func = extract_func(query)
        # binary = binascii.hexlify(queries.encode('utf-8'))
        # print(binary)
        print(json.dumps(query).replace('\\\"', '\"'))

        accept = inspect(src_ip, user_agent, func)
        # create the response message
        if accept:
            # Send the query to GraphQL server
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer <YOUR_ACCESS_TOKEN>'  # optional
            }
            data = {
                'query': query
            }

            # Send the GraphQL request
            response = requests.post(Graphql_server, json=data, headers=headers)
            # Parse the response JSON
            response_data = response.json()

            # send the response headers
            self.send_response(response.status_code)
            for key, value in response.headers.items():
                if key == 'Content-Length':
                    # my edition
                    cont_len = len(json.dumps(response_data))
                    self.send_header('Content-Length', cont_len)
                    print('Content-Length', cont_len)
                    continue

                self.send_header(key, value)
            self.end_headers()

            # send the response body
            self.wfile.write(json.dumps(response_data).encode())
            print(json.dumps(response_data))
            print(len(json.dumps(response_data)))
        # if the request should be rejected
        else:
            self.send_response(403)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('Access Denied'.encode())

    # OPTIONAL------------ for supporting GRT request
    '''
    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body><h1>Hello, world!</h1></body></html>')
'''

    def do_GET(self):
        # extract X-Forwarded-For field from headers
        src_ip = self.headers.get('X-Forwarded-For')
        # print X-Forwarded-For field
        print(f'X-Forwarded-For: {src_ip}')

        user_agent = self.headers.get('User-Agent', '')
        print(f"User-Agent: {user_agent}")

        # Send the GraphQL request
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer <YOUR_ACCESS_TOKEN>'  # optional
        }
        response = requests.get(Graphql_server, headers=headers)

        # Parse the response JSON
        response_data = response.json()

        # send the response headers
        self.send_response(response.status_code)
        for key, value in response.headers.items():
            self.send_header(key, value)
        self.end_headers()

        # send the response body
        self.wfile.write(json.dumps(response_data).encode())


def main():
    # create the HTTP server
    httpd = HTTPServer(('', PORT), RequestHandler)
    print(f"Listening on port {PORT}")
    # start the server
    httpd.serve_forever()


if __name__ == '__main__':
    main()