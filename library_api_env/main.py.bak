from api import app, db
from api import models

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify


from api.queries import resolve_available, \
    resolve_get_book_by_name, \
    resolve_get_books_by_author, \
    resolve_get_all_authors, \
    resolve_get_all_books, \
    resolve_get_user_details,  \
    resolve_get_books_hold_by_user_id, \
    resolve_get_books_hold_by_user_name

from api.mutations import resolve_add_user,\
    resolve_update_user, \
    resolve_add_author, \
    resolve_add_book, \
    resolve_borrow_book, \
    resolve_return_book

query = ObjectType("Query")

query.set_field("available", resolve_available)
query.set_field("getBookByName", resolve_get_book_by_name)
query.set_field("getBooksByAuthor", resolve_get_books_by_author)
query.set_field("getAllAuthors", resolve_get_all_authors)
query.set_field("getAllBooks", resolve_get_all_books)
query.set_field("getUserDetails", resolve_get_user_details)
query.set_field("getBooksHoldByUserId", resolve_get_books_hold_by_user_id)
query.set_field("getBooksHoldByUserName", resolve_get_books_hold_by_user_name)

mutation = ObjectType("Mutation")
mutation.set_field("addUser", resolve_add_user)
mutation.set_field("updateUser", resolve_update_user)
mutation.set_field("addAuthor", resolve_add_author)
mutation.set_field("addBook", resolve_add_book)
mutation.set_field("borrowBook", resolve_borrow_book)
mutation.set_field("returnBook", resolve_return_book)


type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code

def main():
	pass
	
if __name__ == "__main__":
	main()