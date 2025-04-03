from flask import Flask, request 
from datos_dummy import books # Importar la lista de libros

app = Flask(__name__) # Crear una instancia de Flask
app.config["DEBUG"] = True # Debug mode

# http://127.0.0.1:5000/
@app.route('/', methods=['GET'])
def home():
    return "<h1>My second API</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

# 1.Ruta para obtener todos los libros
# http://127.0.0.1:5000/v0/books
@app.route('/v0/books', methods=['GET'])
def all_books():
    return books
    
# 2.Ruta para obtener un libro concreto mediante su id como parámetro en la llamada
# http://127.0.0.1:5000/v0/book_id?id=1
@app.route('/v0/book_id', methods=['GET']) 
def book_id():
    id = int(request.args['id'])
    results = [book for book in books if book["id"]==id]
    return results

# 3.Ruta para obtener un libro mediante su id como parámetro en la llamada de otra forma
# Parámetro de ruta variable
# GET http://
@app.route('/v0/book_id/<int:id>', methods=["GET"])
def book_id_v2(id):
    results = [book for book in books if book["id"]==id]
    return results



# 4.Ruta para obtener un libro concreto mediante su título como parámetro en la llamada de otra forma
# Parámetro de ruta variable
# GET http://127.0.0.1:5000/v0/book/The Ones Who Walk Away From Omelas
@app.route('/v0/book/<string:title>', methods=["GET"])
def book_title(title):
    results = [book for book in books if book["title"].lower()==title.lower()]
    return results


# 5.Ruta para obtener un libro concreto mediante su titulo dentro del cuerpo de la llamada  
# GET http://127.0.0.1:5000/v1/book
# Body: {"title": "The Ones Who Walk Away From Omelas"}
@app.route('/v1/book', methods=["GET"])
def book_title_body():
    title = request.get_json().get('title', None)
    if not title:
        return "Not a valid title in the request", 400
    else:
        results = [book for book in books if book["title"].lower()==title.lower()]
        if results == []:
            return "Book not found", 400
        else:
            return results

# 6.Ruta para añadir un libro mediante un json en la llamada
@app.route('/v1/add_book', methods=["POST"])
def post_books():
    data = request.get_json()
    books.append(data)
    return books


# 7.Ruta para añadir un libro mediante parámetros
# POST http://127.0.0.1:5000/v2/add_book?id=4&title=The Ones Who Walk Away From Omelas&author=Ursula K. Le Guin&first_sentence=With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.&published=1973
@app.route('/v2/add_book', methods=["POST"])
def post_books_v2():
    book = {}
    book['id'] = int(request.args['id'])
    book['title'] = request.args['title']
    book['author'] = request.args['author']
    book['first_sentence'] = request.args['first_sentence']
    book['published'] = request.args['published']
    books.append(book)
    return books

# 8.Ruta para modificar un libro
# PUT http://127.0.0.1:5000/v3/books?id=1&title=The Ones Who Walk Away From Omelas&author=Ursula K. Le Guin
@app.route("/v3/books", methods=["PUT"])
def put_book():
    id = int(request.args['id'])

    title = request.args.get('title', None)
    author = request.args.get('author', None)

    for book in books:
        if book["id"] == id:
            if title:
                book['title'] = title
            if author:
                book['author'] = author
    return books

# 9.Ruta para eliminar un libro
# DELETE http://127.0.0.1:5000/v4/books?id=1
@app.route("/v4/books", methods=["DELETE"])
def del_book():
    id = int(request.args['id'])
    # id = int(id)
    for book in books:
        if book["id"] == id:
            books.remove(book)
    return books


app.run() # Ejecutar la aplicación. Va en último lugar del script