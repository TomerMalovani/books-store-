from bottle import route, run, template, static_file, get, post, delete, request, response
from sys import argv
import json
import pymysql


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    db="bookshop",
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


@post("/category")
def add_category():
    with connection.cursor() as cursor:
        try:
            name = request.forms.get("name")
            if name == "":
                error = {"STATUS": "ERROR", "MSG": "400 - bad request"}
                return json.dumps(error)
            check_if_input_exists = f"select * from categories where name = '{name}' "
            cursor.execute(check_if_input_exists)
            result = cursor.fetchone()
            if result != None:
                error = {"STATUS": "ERROR",
                         "MSG": "200 - category already exists"}
                return json.dumps(error)

            sql = f"INSERT INTO categories (name) VALUES('{name}')"
            cursor.execute(sql)
            connection.commit()
            error = {"STATUS": "SUCCESS",
                     "MSG": "201 - category created successfully"}
            return json.dumps(error)
        except:
            print(
                f"there was a error with adding a new category, error ::() ")


@post("/product")
def add_edit_product():
    with connection.cursor() as cursor:
        try:
            title = json.forms.get("title")
            desc = json.forms.get("desc")
            price = json.forms.get("price")
            img_url = json.forms.get("img_url")
            category = json.forms.get("category")
            favorite = json.forms.get("favorite")
            sql = "INSERT INTO books(title, desc, price, img_url, category, 0)VALUE('{}', '{}', '{}', '{}', '{}', '{}',0)".format(
                title, desc, price, img_url, category, favorite)
            cursor.execute(sql)
            connection.commit()
            error = {"STATUS": "SUCCESS",
                     "MSG": "201 - category created successfully"}
            return json.dumps(error)
        except:
            raise Exception


@get("/categories")
def get_categories():
    with connection.cursor() as cursor:
        try:
            sql = "select * from categories"
            cursor.execute(sql)
            result = {"CATEGORIES": cursor.fetchall()}
            return json.dumps(result)
        except:
            pass


@get("/category/<id>/products")
def get_category(id):
    with connection.cursor() as cursor:
        try:
            sql = f"select * from books as b inner join categories as c on c.id = b.id where c.id ={id}"
            cursor.execute(sql)
            books = cursor.fetchall()
            result = {"PRODUCTS": books}
            print(result)
            return json.dumps(result)
        except:
            pass


@delete("/category/<id>")
def delete_category(id):
    with connection.cursor() as cursor:
        try:
            sql = f"DELETE FROM categories WHERE id = {id}"
            cursor.execute(sql)
            connection.commit()
            error = {"STATUS": "SUCCESS",
                     "MSG": "200 - category deleted successfully"}
            return json.dumps(error)
        except:
            pass


@delete("/product/<id>")
def delete_product(id):
    with connection.cursor() as cursor:
        try:
            sql = f"DELETE FROM books WHERE id = {id}"
            cursor.execute(sql)
            connection.commit()
            error = {"STATUS": "SUCCESS",
                     "MSG": "200 - category deleted successfully"}
            return json.dumps(error)
        except:
            pass


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


run(host='localhost', port=4000, reloader=True)
