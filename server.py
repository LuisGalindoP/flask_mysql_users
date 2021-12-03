from flask import Flask, render_template, request, redirect
# import the class from friend.py
from users import User

app = Flask(__name__)

@app.route("/users")
def index():
    # call the get all classmethod to get all friends
    users = User.get_all()
    print(users)
    return render_template("users.html", users = users)

@app.route('/create_user', methods=["POST"])
def create_user():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    data = {
        "fname": request.form["fname"],
        "lname" : request.form["lname"],
        "email" : request.form["email"]
    }
    # We pass the data dictionary into the save method from the Friend class.
    User.save(data)
    # Don't forget to redirect after saving to the database.
    return redirect("/read_one_new")

@app.route("/read_one_new")
def read_one_new():
    id_show = User.read_one_new()
    return redirect((f"/read_one/{id_show[0]['MAX(id)']}"))

@app.route("/users/new", methods=["GET"])
def new():
    return render_template("new.html")   

@app.route("/read_one/<id_from>", methods=["GET"])
def read_one(id_from):
    selected = User.read_one(id_from)
    return render_template("/read_one.html", selected = selected)

@app.route("/edit/<id_from>")
def edit_template(id_from):
    id_from = id_from
    selected = User.read_one(id_from)
    return render_template("edit.html", id_from = id_from, selected = selected)  

@app.route("/edit_request/<id_from>", methods=["POST"])
def edit(id_from):
    data = {
        "id_from":id_from,    
        "fname": request.form["fname"],
        "lname" : request.form["lname"],
        "email" : request.form["email"]
    }
    print(f"Esta es la data {data}")
    User.edit(data)
    return redirect(f"/read_one/{data['id_from']}")
    
@app.route("/delete/<id_from>")
def delete(id_from):
    User.delete(id_from)
    return redirect("/users")




            
if __name__ == "__main__":
    app.run(debug=True)