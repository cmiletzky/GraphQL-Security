import requests
from graphql import GraphQLError, build_ast_schema, parse, print_ast

# Define the GraphQL query
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

queries = [query8]
print("check")
# Define the GraphQL endpoint URL
url = 'http://127.0.0.1:5000/graphql'

# Define the headers (optional)
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer <YOUR_ACCESS_TOKEN>'
}
result = []
for query in queries:
    # Define the request payload
    data = {
    'query': query
    }
    
    # Send the GraphQL request
    response = requests.post(url, json=data, headers=headers)
    
    # Parse the response JSON
    pre_result = list(response.json()['data'].values())[0]
    result.append(pre_result)

# Check for errors
if 'errors' in result:
  errors = [GraphQLError(error['message']) for error in result['errors']]
  #raise GraphQLError(errors)

# Print the response data
print(result)
