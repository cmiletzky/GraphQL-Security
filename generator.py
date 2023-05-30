import random
import string

# List of malicious ip
malicious_ip = ['193.43.21.65', '245.43.63.86', '43.234.67.32', '32.77.32.123', '211.43.23.253']

prepositions = ['OfMine', 'OfYours', 'OfOurs', 'OfTheirs', 'OfMyFriend']

# List of User-agent
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "AppleWebKit/537.36 (KHTML, like Gecko)",
    "Chrome/92.0.4515.131",
    "Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64)",
    "AppleWebKit/537.36 (KHTML, like Gecko)",
    "Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "AppleWebKit/537.36 (KHTML, like Gecko)",
    "Edge/92.0.902.73",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0)",
    "Gecko/20100101",
    "Firefox/91.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "AppleWebKit/537.36 (KHTML, like Gecko)",
    "Chrome/91.0.4472.101",
    "Safari/537.36",
    "Edge/91.0.864.48",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "AppleWebKit/537.36 (KHTML, like Gecko)",
    "Chrome/93.0.4577.63",
    "Safari/537.36"
]

# List of GraphQL queries
queries = [
    '''query{
      getAllBooks{
        id
        name
        author
        borrowBy
        dueDate
      }
    }
    ''',
    '''query second{
      available(bookId:1)
    }
    ''',
    '''query third {
      getBooksByAuthor(authorId:1){
        name
      }
    }
    ''',
    '''query four {
      getBookByName(bookName:"Book 4"){
        name
        dueDate
      }
    }
    ''',
    '''query five {
      getAllAuthors{
        name
        id
      }
    }
    ''',
    '''query six{
      getUserDetails(userId:1){
        name
        email
        phone
      }
    }
    ''',
    '''query seven {
      getBooksHoldByUserId(userId:1){
        name
      }
    }
    ''',
    '''query eight {
      getBooksHoldByUserName(userName:"ariel"){
        name
      }
    }
    ''',
    '''
    mutation one{
      addUser(name: "misho", email:"misho@gmail.com", phone:"021", address:"baba"){
        name
        id
      }
    }
    ''',
    '''
    mutation two{
      updateUser(userId:104, name:"misho2", email:null, phone:null, address:null){
        name
        id
      }
    }
    ''',
    '''
    mutation three {
      addAuthor(name:"moshe"){
        id
        name
      }
    }
    ''',
    '''
    mutation four {
      addBook(name:"what's up", author:67){
        name
        id
        author
        borrowBy
        dueDate
      }
    }
    ''',
    '''
    mutation five {
      borrowBook(bookId:1, userId:67)
    }
    ''',
    '''
    mutation six {
      returnBook(bookId:1)
    }
    '''
]


# Generate a random IP address for the X-Forwarded-For field
def random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))


def get_malicious_ip(i):
    return malicious_ip[i % 5]

def get_preposition(i):
    return prepositions[i%5]


# Generate a random User-Agent string
def random_user_agent():
    return "MyUserAgent/" + "".join(random.choices(string.ascii_letters + string.digits, k=8))


def generate_POST():
    # Generate a list of 1000 POST requests
    requests = []
    for i in range(1000):
        ip = random_ip()
        user_agent = random.choice(user_agents)
        query = random.choice(queries)
        request = """POST /graphql HTTP/1.1
        Host: 127.0.0.1
        Content-Type: application/json
        Content-Length: """ + str(len(query)) + """
        User-Agent: """ + user_agent + """
        X-Forwarded-For: """ + ip + '\n\n' \
                  + query + "\n *****"

        requests.append(request)

    for i in range(300):
        ip = get_malicious_ip(i)
        user_agent = random.choice(user_agents)
        query = random.choice(queries)
        preposition = get_preposition(i)
        func_name = query.split("{")[1].replace(" ", "").replace("\n", "")
        query = query.replace(func_name, func_name+preposition)
        request = """POST /graphql HTTP/1.1
        Host: 127.0.0.1
        Content-Type: application/json
        Content-Length: """ + str(len(query)) + """
        User-Agent: """ + user_agent + """
        X-Forwarded-For: """ + ip + '\n\n' \
                  + query + "\n *****"
        requests.append(request)

    return requests


def main():
    requests = generate_POST()
    # Print the list of requests
    with open('requests.txt', 'w') as f:
        for request in requests:
            f.write(request + '\n')


if __name__ == '__main__':
    main()
