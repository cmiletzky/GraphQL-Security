
import requests

# the URL of the server
url = 'http://localhost:40000'

# the list of names to send to the server
#names = ['Alice', 'Bob', 'Charlie']
query1 = '''
query{
  getAllBooks{
    id
    name
    author
    borrowBy
    dueDate
  }
}
'''
query2 = '''query second{
  available(bookId:1)
}'''
query3 = '''query third {
  getBooksByAuthor(authorId:1){
    name
  }
}'''
query4 = '''query four {
  getBookByName(bookName:"Book 4"){
    name
    dueDate
  }
}'''
query5 = '''query five {
  getAllAuthors{
    name
    id
  }
}'''
query6 = '''query six{
  getUserDetails(userId:1){
    name
    email
    phone
  }
}'''
query7 = '''query seven {
  getBooksHoldByUserId(userId:1){
    name
  }
}
'''
query8 = '''query eight {
  getBooksHoldByUserName(userName:"ariel"){
    name
  }
}'''
mut1 = '''mutation one{
  addUser(name: "misho", email:"misho@gmail.com", phone:"021", address:"baba"){
    name
    id
  }
}
'''
 
mut2 = '''mutation two{
  updateUser(userId:104, name:"misho2", email:null, phone:null, address:null){
    name
    id
  }
}
'''
mut3 = '''mutation three {
  addAuthor(name:"moshe"){
    id
    name
  }
}
''' 
mut4 = '''mutation four {
  addBook(name:"what's up", author:67){
    name
    id
    author
    borrowBy
    dueDate
  }
}
''' 
mut5 = '''mutation five {
  borrowBook(bookId:1, userId:67)
}
''' 
mut6 = '''mutation six {
  returnBook(bookId:1)
}
'''

queries = [query7]
# send a POST request to the server with the list of names as the request body
headers = {
    'User-Agent': 'CustomUserAgent/1.0',
    'X-Forwarded-For': '192.0.2.1'
}
response = []
for query in queries:
    response.append(requests.post(url, json=query, headers=headers))
    

# print the response from the server
for resp in response:
    print(resp.text)

