import sqlite3
from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)

data = []

# Veritabanı oluşturma fonksiyonu
def create_table():
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tblBook (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booktitle TEXT,
                bookauthor TEXT,
                bookyear INTEGER
            );
        """)
    print("Tablo oluşturuldu.")

# Veritabanı tablosunu oluştur
create_table()

def veriAl():
    global data
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute("select * from tblBook")
        data = cur.fetchall()
        for i in data:
            print(i)


def veriekle(title, author, year):
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute("insert into tblBook (booktitle, bookauthor, bookyear) values (?,?,?)", (title, author, year))
        print("veriler eklendi")




def verisil(id):
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute("delete from tblBook where id =?", (id,))
        con.commit
        print("veriler silindi")   





def veriguncelle(id, title, author, year):
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute("update tblBook set booktitle = ? , bookauthor = ? , bookyear = ? where id = ? ", (title, author, year,id))
        print("veriler guncellendi")     



        


@app.route("/index")
def index():

    books = [

    {
        'bookTitle':'Bloğumuza Hoşgeldiniz'
    },

    {
        'bookTitle':'Keyifli Günler'
    }

    ]



    return render_template("index.html", books = books)


@app.route("/kitap")
def kitap():
    print("kitap")
    veriAl()
    return render_template("kitap.html", veri=data)



@app.route("/contact")
def contact():
    print("contact")
    return render_template("contact.html")




@app.route("/gönderiekle", methods=["GET", "POST"])
def gönderiekle():
    print("gönderiekle")
    if request.method == "POST":
        bookTitle = request.form.get("bookTitle")
        bookAuthor = request.form.get("bookAuthor")
        bookYear = request.form.get("bookYear")
        veriekle(bookTitle, bookAuthor, bookYear)

    return render_template("kitapekle.html")


@app.route("/kitapsil/<string:id>")
def kitapsil(id):
    print("kitapsil silinecek id", id)
    verisil(id)
    return redirect(url_for("kitap"))



@app.route("/kitapguncelle/<string:id>", methods=["GET", "POST"])
def kitapguncelle(id):
    if request.method == "GET":
        print("guncellenecek id", id)
        guncellenecekveri = []
        for d in data:
            if str(d[0]) == id:
                guncellenecekveri = list(d)

        return render_template("kitapguncelle.html", veri = guncellenecekveri)

    else:
        bookID = request.form.get("bookID")
        bookTitle = request.form.get("bookTitle")
        bookAuthor = request.form.get("bookAuthor")
        bookYear = request.form.get("bookYear")
        veriguncelle(bookID, bookTitle, bookAuthor, bookYear)
        return redirect(url_for("kitap"))
    



@app.route("/kitapdetayi/<string:id>")
def kitapdetayi(id):
    detayVeri=[]
    for d in data:
        if str(d[0]) == id:
             detayVeri = list(d)

    return render_template("kitapdetayi.html", veri = detayVeri)


app.static_folder = 'C:\\gorsel\\static'

if __name__ == "__main__":
    app.run(debug = True)

    