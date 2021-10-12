from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form, StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt

# Kullanıcı Kayıt Formu  --- WEB SİTESİ ADRESİ = https://flask-wtf.readthedocs.io/en/stable/quickstart.html#creating-forms -- https://wtforms.readthedocs.io/en/2.3.x/forms/#the-form-class

class RegisterForm (Form):     # Veri tabanında özel olarak oluşturduğumuz içeriklere göre 5 adet değeri yazıp özelleştireceğiz.
    name = StringField("İsim Soyisim",validators=[validators.Length(min = 4,max = 25)]) # validators karakteri doğrulayıcı bir karakterdir. Yani kısıt koyabiliriz.(minimum 4, max 25 karakter sınırı getirdik.) Length komutu ile uzunluğu belirledik.
    username = StringField("Kullanıcı Adı",validators=[validators.Length(min = 4,max = 25)])
    email = StringField("Email Adresi",validators=[validators.Email(message = "Lütfen geçerli bir email adresi giriniz...")]) # validators.email komutu ile girilen email adresinin  geçerli bir email adresi olup olmadığını kontrol ettik ve mesaj olarak geri bildirim vermek istediğimiz için message komutu ile geri bildirim vereceğimiz kelimeleri kullandık.
    password = PasswordField("Parola",validators=[
        validators.DataRequired(message = "Lütfen bir parola belirleyiniz..."), # DataRequired komutu ile parola boş mu dolu mu diye kontrol ettik.
        validators.EqualTo(fieldname = "confirm",message = "Parolanız uyuşmuyor...")
    ])
    confirm = PasswordField("Parola Doğrula")

app = Flask(__name__)
# WEB SİTESİ LİNKİ = https://flask-mysqldb.readthedocs.io/en/latest/
app.config["MYSQL_HOST"] = "localhost" # Bu komut ile hangi hostta çalışıyorsak onu yazmamız gerekiyor.(localde çalıştığımız için localhost dedik)
app.config["MYSQL_USERS"] = "root" # Veri tabanımızın kullanıcı adını vermemiz gerekiyor.(Parola boş ve kullanıcı adı root olarak gelir.)
app.config["MYSQL_PASSWORD"] = "" # Veri tabanına bağlanmamız için gereken parolayı vermemiz gerekiyor.(İlk başta boş geldiği için boş bıraktık.)
app.config["MYSQL_DB"] = "yılmazsoft" # Veri tabanının ismini vermemiz gerekiyor.
app.config["MYSQL_CURSORCLASS"] = "DictCursor" # Bu komut ile veri tabanımızdaki değerleri sözlük haline getirip daha detaylı görmemizi sağlamış olacağız.
mysql = MySQL(app) # Veri tabanımıza app komutunu tanımladık.

@app.route("/")
def index():
    return render_template("anasayfa.html")


# @app.route("/AnaSayfa")
# def AnaSayfa():
#     numbers = [1,2,3,4,5]
#     return render_template("anasayfa.html",numbers = numbers)
# @app.route("/AnaSayfa/<string:id>")
# def deneme(id):
#     return "Ana Sayfa id :"+id

if __name__ == "__main__":
    app.run(debug=True)

