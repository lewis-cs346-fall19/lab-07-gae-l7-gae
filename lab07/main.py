import webapp2
import MySQLdb, random
import gcloudpasswords

conn = MySQLdb.connect(unix_socket = gcloudpasswords.SQL_HOST,
                       user        = gcloudpasswords.SQL_USER,
                       passwd      = gcloudpasswords.SQL_PASSWD,
                       db          = "lab07")

id = "%032x" % random.getrandbits(128)

class MainPage(webapp2.RequestHandler):
    def get(self):
        if self.request.cookies.get("id") is None:
            query = ("insert into sessions (s_id) values (\"%s\")" % id)
            cursor = conn.cursor()
            cursor.execute(query)
            cursor.close()
            conn.commit()
            global id
            id = "%032x" % random.getrandbits(32)
            self.response.set_cookie("id", id, max_age=1800)
            return self.redirect("/")
        else:
            query = ("select username from sessions where s_id = \"%s\"" % id)
            cursor = conn.cursor()
            cursor.execute(query)
            username = cursor.fetchone()
            cursor.close()
            if (username is None):
                self.response.headers["Content-Type"] = "text/html"
                self.response.write("""
                <hmtl>
                <head><title>Main Page Lab07</title></head>
                <br>
                <b><font size='+2'>Home Page</font></b>
                <hr>
                <form action='add_user' method=POST>
                <p> username: <br><input type="text", name="username" maxlength="30"</br>
                <p><input type="submit" value="Submit">
                </form>
                </body>
                </html>
                """)


class AddUser(webapp2.RequestHandler):
    def post(self):
        username = self.request.POST["username"]
        query = ("update sessions set username=\"%s\" where s_id=\"%s\"" % (username, id))
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.close()
        conn.commit()


class Test(webapp2.RequestHandler):
    def get(self):
        cursor = conn.cursor()
        cursor.execute("select * from dotaheroes")
        self.response.write(cursor.fetchall())
        cursor.close()


app = webapp2.WSGIApplication([
    ("/", MainPage),
    ("/test", Test),
    ("/add_user", AddUser),
], debug=True)
