from flask import Flask,render_template,redirect,url_for,request
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application "SQL ALCHEMY FLASK PROJESİNE ENTEGRE ETME VE VERİ TABANI KONTROLLERİ YAPMA LİNKİ"
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Emre/Desktop/TodoApp/todo.db'  # Projemiz içindeki todo tablosuna klasörün içinden girerek yolunu kopyaladık ve bu ksımda dahil ettik.
db = SQLAlchemy(app)   # Aradaki köprüyü kurmuş olduk.

class Todo(db.Model):     # Tablomuzu oluşturuyoruz.
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))   # Maksimum 80 karakter olarak belirledik.
    complete = db.Column(db.Boolean)   # Ya 0 ya 1 değerini alacak yani 1 değeri true, 0 değeri bize false'yi gösterecek.

@app.route("/")
def index():
    todos = Todo.query.all()  # Veri tabanındaki bütün verileri bu komut yardımı ile almış olduk. 
    return render_template("index.html",todos = todos)
@app.route("/add",methods = ["POST"])
def addTodo():
    title = request.form.get("title")
    newTodo = Todo(title = title,complete = False)  # Veri tabanında objemizi oluşturduk.
    db.session.add(newTodo) # Oluşturduğumuz objemizi veritabanına ekledik.
    db.session.commit()  # Veri tabanında değişiklik yaptığıız için commit komutunu kullandık.

    return redirect(url_for("index"))
@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    if todo.complete == True:
        todo.complete = False
    else:
        todo.complete = True
    db.session.commit()
    return redirect(url_for("index"))
@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":    # Serverimizi ayağa kaldırıyoruz.
    db.create_all()           # Oluşturduğumuz tüm veri tabanı dosyalarımızı yani oluşturduğumuz tüm classlarımızı bu komut ile çağırıyoruz.
    app.run(debug=True)

                                                                                                                                            