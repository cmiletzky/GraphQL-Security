import random
import string

# List of User-agent
user_agents = ["""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36""",
"""Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36""",
"""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/92.0.902.73""",
"""Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0""",
"""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48""",
"""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36""",
"""Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36""",
"""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36""",
"""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 YaBrowser/21.5.3.742 Yowser/2.5 Safari/537.36""",
"""Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36""",
"""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36""",
"""Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36""",
"""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36""",
"""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36""",
"""Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0""",
"""Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472"""]

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
        request = "POST /graphql HTTP/1.1\r\n" + \
                  "Host: 127.0.0.1\r\n" + \
                  "Content-Type: application/json\r\n" + \
                  "Content-Length: " + str(len(query)) + "\r\n" + \
                  "User-Agent: " + user_agent + "\r\n" + \
                  "X-Forwarded-For: " + ip + "\r\n" + \
                  "\r\n" + \
                  query + "\r\n" + \
                  "\r\n"+ "\r\n" + \
                  "\r\n"
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