import sqlite3
import cgi

HTML_PAGE_1 = """<html>
<title>Головна сторінка</title>
<body>
<h3>2C-Бухгалтерія</h3>
<br>
<form method=POST action="add_employee">
<input type=submit value="Додати Працівника">
</form>
<form method=POST action="update_data">
<input type=submit value="Змінити дані">
</form>
<form method=POST action="show_data">
<input type=submit value="Показати дані">
</form>
</body>
</html>
"""
HTML_PAGE_2 = """
<html>
<title>Employee Registration</title>
<body>
<h3>Додати Працівника</h3>
<form method=POST action="add_emp_to_table">
<table>
<td>
ПІБ <input type=text name=name value="">
</td>
<td>
Оплата <input type=text name=payment value="">
</td>
<td>
Середня Оплата <input type=text name=av_payment value="">
</td>
<br>
{}
<td>
<input type=submit value="Додати до бази">
</td>
</table>
</form>
</body>
</html>
"""
HTML_PAGE_3 = """<html>
<title>Result</title>
<body>
<h3>Result</h3>
<br>
<form method=POST action="go_to_main">
<table>
<td>
{}
</td>
<td>
<input type=submit value="Повернутися на головну">
</td>
</table>
</form>
</body>
</html>
"""
HTML_PAGE_4 = """
<html>
<title>Data changing</title>
<body>
<h3>Змінити дані</h3>
<br>
<form method=POST action="data_check">
<table>
<tr>
<td>
<select name=name value="">
{}
</select>
</td>
<td>
<select name=change value="">
  <option>Імя</option>
  <option>Оплата</option>
  <option>Середнє</option>
  <option>Табель</option>
  <option>Видалити</option>
</select>
</td>
<td>
<input type=submit value="Перевірка">
</td>
</table>
</form>
</body>
</html>
"""

HTML_PAGE_5 = """
<html>
<title>Data changing</title>
<body>
<h3>Поточні дані для {} в {}</h3>
<br>
<form method=POST action="data_change">
<table>
<tr>
<td>
<p>
Зараз {}
</p>
</td>
<td>
Змінити на <input type=text name=changing value="">
</td>
<td>
<input type=submit value="Змінити">
</td>
</table>
</form>
</body>
</html>
"""

HTML_PAGE_6 = """
<html>
<title>Tabel configuration</title>
<body>
<h3>Табель змінити</h3>
<br>
<form method=POST action="change_tabel">
<table>
{}
<td>
<select name=day_change value="">
{}
</select>
</td>
<td>
Змінити на:<input type=text name=changing value="">
</td>
<td>
<input type=submit value="Змінити">
</td>
</table>
</form>
</body>
</html>
"""

HTML_PAGE_7 = """<html>
<title>Visual</title>
<body>
<h3>Data Show</h3>
<br>
<form method=POST action="go_to_main">
<table>
<td>
{}
</td>
<td>
<input type=submit value="Повернутися на головну">
</td>
</table>
</form>
</body>
</html>
"""

class DB:
    def __init__(self, filename):
        self.filename = filename

    def create_rb(self, create_response_dict):
        try:
            conn = sqlite3.connect(self.filename)
            curs = conn.cursor()
            curs.execute("CREATE TABLE IF NOT EXISTS {}(Імя PRIMARY KEY,Оплата,Середнє)".format('Працівники'))
            curs.execute("CREATE TABLE IF NOT EXISTS {}(Імя PRIMARY KEY,Сума)".format('Нарахування'))
            name = "_".join(create_response_dict["name"].split())
            payment = create_response_dict["payment"]
            av_payment = create_response_dict["av_payment"]
            curs.execute("INSERT INTO Працівники(Імя,Оплата,Середнє) VALUES (?,?,?)", (name, payment, av_payment))
            curs.execute("CREATE TABLE {}('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30')".format(name))
            l = []
            for j in create_response_dict["days"]:
                work = create_response_dict["days"][j]
                l.append(work)
            curs.execute("INSERT INTO {}('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)".format(name), l)
            money = 0
            for k in l:
                if k == 'л':
                    money += 0.8 * payment
                elif k == 'в':
                    money += av_payment
                else:
                    money += int(k) * payment
            curs.execute("INSERT INTO Нарахування(Імя,Сума) VALUES (?,?)", (name, money))
            conn.commit()
            conn.close()
            return "Completed"
        except:
            return "Error"


    def show_data(self):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        d = {}
        r1 = curs.execute("SELECT * FROM Нарахування").fetchall()
        for i in r1:
            d[i[0]]=i[1]
        """
        elif choice == 'один':
            name = input("Введіть імя: ")
            r2 = curs.execute("SELECT Сума FROM Нарахування WHERE Імя == ?", (name,)).fetchone()
            d += name + ' ' + str(r2[0])"""
        conn.commit()
        conn.close()
        print(d)
        return d

    def data_from_pracivniki(self, column):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        r = [i[0] for i in curs.execute("SELECT {} FROM Працівники".format(column)).fetchall()]
        conn.commit()
        conn.close()
        return r

    def update_rb(self, data_change):
        try:
            conn = sqlite3.connect(self.filename)
            curs = conn.cursor()
            if self.column == "Імя":
                curs.execute("UPDATE Нарахування SET {} == ? WHERE Імя == ?".format(self.column), (data_change,self.name)).fetchall()
                curs.execute("UPDATE Працівники SET {} == ? WHERE Імя == ?".format(self.column), (data_change,self.name)).fetchall()
                curs.execute("ALTER TABLE {} RENAME TO {}".format(self.name, data_change)).fetchone()
            elif self.column == "Видалити":
                curs.execute("DELETE FROM Працівники WHERE Імя = ?", (self.name,))
                curs.execute("DELETE FROM Нарахування WHERE Імя = ?", (self.name,))
                curs.execute("DROP TABLE {}".format(self.name))
                conn.commit()
                conn.close()
                return "Completed"
            elif self.column == "Оплата":
                new_payment = int(data_change)
                av_payment = curs.execute("SELECT Середнє FROM Працівники WHERE Імя == ?", (self.name,)).fetchone()
                curs.execute("UPDATE Працівники SET Оплата == ? WHERE Імя == ?", (new_payment, (self.name)))
                p = curs.execute("SELECT * FROM {}".format(self.name)).fetchall()
                p1 = list(p[0])
                money1 = 0
                for k in p1:
                    if k == 'л':
                        money1 += 0.8 * new_payment
                    elif k == 'в':
                        money1 += int(av_payment[0])
                    else:
                        money1 += int(k) * new_payment
                curs.execute("UPDATE Нарахування SET Сума == ? WHERE Імя == ?", (money1, (self.name)))
            elif self.column == 'Середнє':
                new_av_payment = int(data_change)
                payment = curs.execute("SELECT Оплата FROM Працівники WHERE Імя == ?", (self.name,)).fetchone()
                curs.execute("UPDATE Працівники SET Середнє == ? WHERE Імя == ?", (new_av_payment, self.name))
                q = curs.execute("SELECT * FROM {}".format(self.name)).fetchall()
                q1 = list(q[0])
                money2 = 0
                for k in q1:
                    if k == 'л':
                        money2 += 0.8 * int(payment[0])
                    elif k == 'в':
                        money2 += new_av_payment
                    else:
                        money2 += int(k) * int(payment[0])
                curs.execute("UPDATE Нарахування SET Сума == ? WHERE Імя == ?", (money2, self.name))
            elif self.column == 'Табель':
                day = int(data_change[0])
                day_res = data_change[1]
                payment = curs.execute("SELECT Оплата FROM Працівники WHERE Імя == ?", (self.name,)).fetchone()
                av_payment = curs.execute("SELECT Середнє FROM Працівники WHERE Імя == ?", (self.name,)).fetchone()
                r = curs.execute("SELECT * FROM {}".format(self.name)).fetchall()
                res = list(r[0])
                res[day - 1] = day_res
                curs.execute("DELETE FROM {} WHERE rowid = (SELECT rowid FROM {} LIMIT 1)".format(self.name, self.name))
                curs.execute("INSERT INTO {}('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)".format(self.name), res)
                money3 = 0
                for k in res:
                    if k == 'л':
                        money3 += 0.8 * int(payment[0])
                    elif k == 'в':
                        money3 += int(av_payment[0])
                    else:
                        money3 += int(k) * int(payment[0])
                curs.execute("UPDATE Нарахування SET Сума == ? WHERE Імя == ?", (money3, self.name))
            conn.commit()
            conn.close()
            return "Completed"
        except:
            return "Error"

    def get_data_rb(self, column, name):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        self.column = column
        self.name = name
        if self.column == "Табель":
            r = curs.execute("SELECT * FROM {}".format(self.name)).fetchall()
            conn.commit()
            conn.close()
            temp_dict = {}
            for i in range(30):
                temp_dict[i+1]=r[0][i]
            return temp_dict
        if self.column != "Видалити":
            r = curs.execute("SELECT {} FROM Працівники WHERE Імя = ?".format(column), (name,)).fetchall()
            conn.commit()
            conn.close()
            return r[0][0]
        else:
            conn.commit()
            conn.close()
            return None

def make_table_to_html():
    res="<table>"
    for i in range(3):
        res+="<tr>"
        for j in range(10):
            res += f'<td>День {str((j+1)+(i*10))}<input type=text name=day_{str((j+1)+(i*10))} value=""></td>'
        res+="</tr>"
    res+="</table>"
    return res

def application(environ, start_response):
    if environ.get('PATH_INFO', '').lstrip('/') == '' or environ.get('PATH_INFO', '').lstrip('/') == 'go_to_main':
        body = HTML_PAGE_1
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

    elif environ.get('PATH_INFO', '').lstrip('/') == "add_employee":
        body = HTML_PAGE_2.format(make_table_to_html())
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

    elif environ.get('PATH_INFO', '').lstrip('/') == "add_emp_to_table":
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        create_response_dict = {}
        if 'name' in form and 'payment' in form and 'av_payment' in form:
            day_empty = False
            for i in range(30):
                if "day_{}".format(str(i+1)) not in form:
                    day_empty = True
            if not day_empty:
                create_response_dict["name"]=form["name"].value
                create_response_dict["payment"]=int(form["payment"].value)
                create_response_dict["av_payment"]=int(form["av_payment"].value)
                create_response_dict["days"]={}
                for i in range(30):
                    create_response_dict["days"]["{}".format(str(i+1))]=form["day_{}".format(str(i+1))].value
                print(create_response_dict)
                body = HTML_PAGE_3.format(rb.create_rb(create_response_dict))

        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

    elif environ.get('PATH_INFO', '').lstrip('/') == "update_data":
        name_list = sorted(rb.data_from_pracivniki("Імя"))
        option_format = ""
        for i in name_list:
            option_format+="<option>{}</option>".format(i)
        body = HTML_PAGE_4.format(option_format)
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

    elif environ.get('PATH_INFO', '').lstrip('/') == "data_check":
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        if 'name' in form and 'change' in form:
            if form["change"].value == "Табель":
                dict_format = rb.get_data_rb(form["change"].value, form["name"].value)
                html_format = "<table>"
                for i in dict_format:
                    html_format +="<td>day {} = {}</td>".format(str(i), dict_format[i])
                html_format += "</table>"
                option_format = ""
                for i in range(30):
                    option_format+="<option>{}</option>".format(i+1)
                body = HTML_PAGE_6.format(html_format, option_format)
            elif form["change"].value == "Видалити":
                rb.get_data_rb(form["change"].value, form["name"].value)
                body = HTML_PAGE_3.format(rb.update_rb("None"))
            else:
                body = HTML_PAGE_5.format(form["name"].value,form["change"].value,rb.get_data_rb(form["change"].value, form["name"].value))
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

    elif environ.get('PATH_INFO', '').lstrip('/') == "data_change":
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        if 'changing' in form:
            body = HTML_PAGE_3.format(rb.update_rb(form['changing'].value))
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

    elif environ.get('PATH_INFO', '').lstrip('/') == "show_data":
        html_format="<table>"
        temp_dict = rb.show_data()
        for i in temp_dict:
            html_format+="<td>{}:{}</td>".format(i,temp_dict[i])
        html_format+="</table>"
        body = HTML_PAGE_7.format(html_format)
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

    elif environ.get('PATH_INFO', '').lstrip('/') == "change_tabel":
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        if 'day_change' in form and 'changing' in form:
            data_change = (form['day_change'].value, form['changing'].value)
            body = HTML_PAGE_3.format(rb.update_rb(data_change))
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

    else:
        start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
        body = 'Сторінку не знайдено'

    return [bytes(body, encoding='utf-8')]


if __name__ == '__main__':
    # створити та запуститити WSGI-сервер
    from wsgiref.simple_server import make_server
    filename = 'accounts.db'
    rb = DB(filename)
    print('=== Local WSGI webserver ===')
    httpd = make_server('localhost', 8000, application)
    httpd.serve_forever()
