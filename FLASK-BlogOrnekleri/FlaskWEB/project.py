from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form, StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps

#   Kullanıcı Giriş Decorator  https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/ sitesinden aldığımız deften sonra gelen if ve return kısımlarını silip kendi yazdığımız sitenin sessionunun kullanacağız.
def login_required(f):   # Bu fonksiyonu proje içinde siteye giriş kısıtlaması getirmek istediğimiz her sayfadan önce kullanarak kullanıcının giriş izninin olmasını sağlarız.
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için lütfen giriş yapınız...","danger")
            return redirect(url_for("login"))
    return decorated_function


# Kullanıcı Kayıt Formu  --- WEB SİTESİ ADRESİ = https://flask-wtf.readthedocs.io/en/stable/quickstart.html#creating-forms -- https://wtforms.readthedocs.io/en/2.3.x/forms/#the-form-class

class RegisterForm (Form):     # Veri tabanında özel olarak oluşturduğumuz içeriklere göre 5 adet değeri yazıp özelleştireceğiz.
    name = StringField("İsim Soyisim",validators=[validators.Length(min = 4,max = 25,message="Lütfen geçerli ad soyad bilgisi giriniz...")]) # validators karakteri doğrulayıcı bir karakterdir. Yani kısıt koyabiliriz.(minimum 4, max 25 karakter sınırı getirdik.) Length komutu ile uzunluğu belirledik.
    username = StringField("Kullanıcı Adı",validators=[validators.Length(min = 4,max = 25,message="Lütfen geçerli bir kullanıcı adı giriniz...")])
    email = StringField("Email Adresi",validators=[validators.Email(message = "Lütfen geçerli bir email adresi giriniz...")]) # validators.email komutu ile girilen email adresinin  geçerli bir email adresi olup olmadığını kontrol ettik ve mesaj olarak geri bildirim vermek istediğimiz için message komutu ile geri bildirim vereceğimiz kelimeleri kullandık.
    password = PasswordField("Parola",validators=[
        validators.DataRequired(message = "Lütfen bir parola belirleyiniz..."), # DataRequired komutu ile parola boş mu dolu mu diye kontrol ettik.
        validators.EqualTo(fieldname = "confirm",message = "Parolanız uyuşmuyor...")
    ])
    confirm = PasswordField("Parola Doğrula")
class LoginForm(Form):
    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")

app = Flask(__name__)
app.secret_key = "yılmazsof_mesaj_deneme" # Kayıt ol işleminden sonraki uyarı mesajı için gereken takma key.

# WEB SİTESİ LİNKİ = https://flask-mysqldb.readthedocs.io/en/latest/

app.config["MYSQL_DATABASE_HOST"] = "localhost" # Bu komut ile hangi hostta çalışıyorsak onu yazmamız gerekiyor.(localde çalıştığımız için localhost dedik)
app.config["MYSQL_USERS"] = "root" # Veri tabanımızın kullanıcı adını vermemiz gerekiyor.(Parola boş ve kullanıcı adı root olarak gelir.)
app.config["MYSQL_PASSWORD"] = "" # Veri tabanına bağlanmamız için gereken parolayı vermemiz gerekiyor.(İlk başta boş geldiği için boş bıraktık.)
app.config["MYSQL_DB"] = "yılmazsoft" # Veri tabanının ismini vermemiz gerekiyor.
app.config["MYSQL_CURSORCLASS"] = "DictCursor" # Bu komut ile veri tabanımızdaki değerleri sözlük haline getirip daha detaylı görmemizi sağlamış olacağız.
mysql = MySQL(app) # Veri tabanımıza app komutunu tanımladık.



@app.route("/")
def anasayfa():
    return render_template("anasayfa.html",islem = 5)
@app.route("/hakkimizda")
def hakkımızda():
    numbers = [1,2,3,4,5]
    return render_template("hakkimizda.html",numbers = numbers,)
@app.route("/iletisim")
def iletisim():
    ceviri = [
        {"class":"sınıf","car":"araba","school":"okul"},
        {"room":"oda","name":"ad","surname":"soyad"},
        {"department":"bölüm","apple":"elma","orange":"turuncu"}
    ]
    return render_template("iletisim.html",ceviri = ceviri)

@app.route("/iletisim/<string:id>")
def deneme(id):
    return "iletişim id :"+id

                #KAYIT OLMA  # https://flask.palletsprojects.com/en/1.1.x/patterns/wtforms/
@app.route("/giris", methods = ["GET","POST"])
def giris():
    form = RegisterForm(request.form)
# https://www.youtube.com/watch?v=qBNI9uPJAg8  ->sorun: phpmyadmin windows oturıcıya izin vermiyor, xamp/mysql/bin dosyasında mysqld altında skip-grant-tables ekle ve restart at
    if request.method == "POST" and form.validate(): #Request'in get request mi post request mi olduğunu anlıyoruz ve form.validate komutu ile yukarıda yazdığımız validators kısıtlamalarının sağlanmasını istiyoruz ve sağlanmadığında yukarıda message kısmına yazdığımız uyarıları kullanıcılara vereceğiz.
        name = form.name.data # By komutlar ile texteki verileri veri tabanına kaydetmek için alıyoruz.(üst kısımda kaç tane veri yazdıysak onları alıyoruz sadece)
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data) # Bu komut ile kullanıcı tarafından girilen şifre bilgsi veritabanında şifreli bir şekilde gözükecektir.
        
        cursor = mysql.connection.cursor() #cursor komutu veri tabanı üzerinde işlem yapmamızı sağlıyor ve bu komut ile işlem yapmaya başlamış oluyoruz.(veri tabanının ismi önemli yukarıda yazdığımız veri tabanı ismini yazıyoruz(mysql))
        sorgu = "Insert into users(name,email,username,password) VALUES(%s,%s,%s,%s)" #veri tabanına oluşturduğumuz tabloya değer ekliyoruz
    
        cursor.execute(sorgu,(name,email,username,password))  # SQL Sorgusu oluşturuyoruz ve her değer yukarıdaki %s'in yerini alıyor.
        mysql.connection.commit() # Veri tabanında değişiklik yapıyoruz. (Veri tabanından sadece bilgi çekilecekse bu komutu yazmamıza gerek yoktur. Ancak biz bu projemizde veritabanına veri ekleyeceğimiz için yazmamız gerekli. Veri tabanında silme, değiştirme vb. işlemler için bu komutu yazmamız gereklidir.)
        cursor.close()  # MYSQL bağlantısını kapattık.
        flash("Başarılı bir şekilde kayıt oldunuz...","success")  # Kayıt sonrası mesaj için bilgi verdik ve 2. parametre olarak success değerini kullandık. https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/
        return redirect(url_for("login"))  # "redirect" komutu ile şart sağlandığında index sayfasına gittik.
    else:
        return render_template("giris.html", form = form)
@app.route("/login",methods = ["GET","POST"])
def login():
    form = LoginForm(request.form)

        # KULLANICI GİRİŞİ 
    if request.method == "POST":   # Metodumuz post ise formdaki bilgileri alıyoruz.
        username = form.username.data   # Formdaki bilgileri aldık
        password_entered = form.password.data

        cursor = mysql.connection.cursor() # Veri tabanı üzerinde işlem yapmamızı sağlayan cursorumuzu oluşturduk.

        sorgu = "Select * From users where username = %s"  # Girilen kullanıcı veri tabanında varmı diye bir sorgu oluşturuyoruz.

        result = cursor.execute(sorgu,(username,))  # Eğer girilen bilgilere göre bir kullanıcı yok ise result 0 geliyor ve hata mesajı ekrana yansıyor.

        if result > 0: # Result 0 gelmiyorsa bu dögüye girer yani result 0dan büyük ve böyle bir kullanıcı var ise 
            data = cursor.fetchone() # Bu komut ile kullanıcının veritabanındaki bütün bilgilerini alıyoruz.
            real_password = data["password"]
            if sha256_crypt.verify(password_entered,real_password): # Girilen şifreyi verify fonksiyonu ile veritabanındaki şifre ile karşılaştırmış oluyoruz.
                flash("Başarılı bir şekilde giriş yaptınız...","success")

                session["logged_in"] = True  # Giriş çıkış kontrollerini yapmak için session kontrolünü başlattık ve bunu uygulamanın heryerinde kullanabileceğiz.
                session["username"] = username

                return redirect(url_for("anasayfa")) # kullanıcının bütün bilgileri doğru geldiğinde anasayfaya yönlendiriyoruz.
            else:
                flash("Parolanızı yanlış girdiniz...","danger")
        else:
            flash("Böyle bir kullanıcı bulunmuyor","danger") #result 0 gelince bu döngüye girer.
            return redirect(url_for("login")) # ve tekrar giriş sayfasına yönlendiriyoruz.
        
    return render_template("login.html",form = form)  # form değerini login htmlde kullanmak için gönderdik.

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("anasayfa"))


@app.route("/kontrolpanel")
@login_required     # /kontrolpanel sayfasından hemen önce yukarıda yazdığımız decoratoru kullandık ve sitemize kayıtlı olan kullanıcıların sadece bu sayfaya erişmesini sağlamış olduk.
def kontrolpanel():
    return render_template("kontrolpanel.html")

class ArticleForm(Form):
    title = StringField("Makale Başlığı",validators = [validators.Length(min = 5,max = 100,message=("Makale başlığı en az 5 en fazla 100 karakterden oluşmalıdır!"))])
    content = TextAreaField("Makale İçeriği",validators=[validators.Length(min = 4, max = 100,message=("Makale içeriği en az 4, en fazla 100 karakterden oluşmalıdır!"))])  # Uzun bir text alanı gerektiği için textareafieldi yazdık. 

@app.route("/makalekle",methods = ["GET","POST"])
@login_required
def makalekle():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():   # üst tarafta validate kısmında bazı kısıtlamalar getirdiğimiz için form.validate() komutunu da koşulumuza dahil ettik.
        title = form.title.data    # Tablolara girilen verileri alıyoruz.
        content = form.content.data 

        cursor = mysql.connection.cursor()  # Veri tabanı üzerinde işlem yapmamızı sağlayan cursorumuzu başlattık

        sorgu = "Insert into articles(title,author,content) VALUES(%s,%s,%s)"  # Veri tabanında tabloyu oluştururken id kısmını auto seçitiğimiz için ve otomatik artacağı için ve yine veri tabanında oluşturduğumuz created_date komutunun da otomatik zaman verilerini tuttuğu için bu bölümde yazmamıza gerek kalmadı.

        cursor.execute(sorgu,(title,session["username"],content))  # execute yardımıyla cursor üzerindeki sorgumuzu başlatıık.

        mysql.connection.commit() # Sorgumuz veri tabanında değişiklik yapacağı için commit işlemini yaptık.

        cursor.close()

        flash("Makale başarılı bir şekilde eklendi...","success")
        return redirect(url_for("kontrolpanel"))
    
    return render_template("/makalekle.html",form = form)

@app.route("/makaleler")
def makaleler():
    cursor = mysql.connection.cursor()
    sorgu = "Select * From articles"   # Veri tabanındaki bütün makaleleri çekmek için Select*From articles dedik.
    result = cursor.execute(sorgu)      #Sorguyu çalıştırdık ve sorgudan dönen sonucu result'a atadık.

    if result > 0:
        makaleler = cursor.fetchall()  # fetchall fonksiyonu veritabanındaki tüm makaleleri liste içinde sözlük olarak dönecek.
        return render_template("makaleler.html",makaleler = makaleler)
    else:
        return render_template("/makaleler.html")
if __name__ == "__main__":
    app.run(debug=True)