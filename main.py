from flask import Flask, render_template, url_for, request, session
import db
app = Flask('app')

app.secret_key = 'FLRML.FLORMAIL.SECRET_KEY.K3N57SH'

@app.route('/')
def index():
  if 'u' in session:
    return '<meta http-equiv="refresh" content="0; url=account/my" />'
  return render_template("index.html")

@app.route('/account/login', methods = ['POST', 'GET'])
def praceLogin():
  if 'u' in session:
    return '<meta http-equiv="refresh" content="0; url=my" />'
  msg = ''
  if request.method == "POST":
    uname = request.form.get("uname")
    psw = request.form.get("psw") 
    u = db.check_user(uname, psw)     
    try:
      if len(u) > 0:
        session['u'] = uname
        session['p'] = psw
        session['e'] = db.check_email(uname)
        msg = "Loading..."
        print("NOWE LOGOWANIE: ", session['u']) 
        return '<meta http-equiv="refresh" content="0; url=my" />'
    except TypeError:
      msg = "Login and/or password are incorrect"
  return render_template("/login.html", msg=msg)

@app.route('/account/create', methods=['POST', 'GET'])
def rej():
  if 'u' in session:
    return '<meta http-equiv="refresh" content="0; url=my" />'
  msg = ''
  if request.method == "POST":
    uname = request.form.get("uname")
    psw = request.form.get("psw") 
    email = request.form.get("email1") + request.form.get('email2')
    u = db.check_user(uname, psw)   
    try:
      if len(u) > 0:
        msg = 'This login is in use!'
    except:
      print("NOWA REJESTRACJA: ", uname)
      db.add_user(uname, psw, email)
      session['u'] = uname
      session['p'] = psw
      session['e'] = email
      msg = "Loading..."
      print("NOWE LOGOWANIE: ", session['u']) 
      return '<meta http-equiv="refresh" content="0; url=my" />'
  return render_template('register.html', msg=msg)

@app.route('/account/signout')
def wl():
  session.clear()
  return '<meta http-equiv="refresh" content="0; url=../account/login" />'

@app.route('/account/inbox')
def inbox():
  if not 'u' in session:
    return '<meta http-equiv="refresh" content="0; url=login" />'
  mail = db.inbox(session['e'])
  if mail == None:
    mail = ""
  mail = db.Reverse(mail)
  return render_template('inbox.html', mail=mail)

@app.route('/redirect/<l>')
def re(l):
  return render_template("redirect.html", l=l)

@app.route('/account/my')
def my():
  if 'u' in session:
    return render_template('my.html')
  else:
    return '<meta http-equiv="refresh" content="0; url=signout" />'

@app.route('/mail')
def mail():
  if not 'u' in session:
    return '<meta http-equiv="refresh" content="0; url=../account/login" />'
  try:
    id_ = request.args.get("id")
    mail = db.get_mail_by_id(id_)
    if session['e'] == mail[0] or session['e'] == mail[1]:
      return render_template("mail.html", title=mail[3], fromu=mail[0], tou=mail[1], content=mail[2])
    else:
      return '<meta http-equiv="refresh" content="0; url=../account/my" />' 
  except:
    return render_template("mail.html", title="Not found!", fromu="", tou="", content="")

@app.route('/mail/create', methods=['POST', 'GET'])
def createMail():
  if not 'u' in session:
    return '<meta http-equiv="refresh" content="0; url=../account/login" />'
  if request.method == "POST":
    id_ = db.rand()
    from_ = session['e']
    to_ = request.form.get("tou").lower()
    con_ = request.form.get("content")
    title_ = request.form.get("title")
    db.send(from_, to_, con_, title_, id_)
    return f'<meta http-equiv="refresh" content="0; url=../mail?id={id_}" />'
  return render_template('create.html')

@app.route('/mail/sent')
def sent():  
  if not 'u' in session:
    return '<meta http-equiv="refresh" content="0; url=../account/login" />'
  mail = db.sent(session['e'])
  if mail == None:
    mail = ""
  mail = db.Reverse(mail)
  return render_template('outbox.html', mail=mail)

@app.route('/account/settings')
def more():
  return render_template('more.html')

@app.route('/account/settings/password', methods=['POST', 'GET'])
def chnPsw():
  msg = ''
  if request.method == "POST":
    old = request.form.get("old")
    new = request.form.get("new")
    if db.login(session['u'], old):
      session['p'] = new
      db.update_pass(new, session['u'])
      return '<meta http-equiv="refresh" content="0; url=../my" />'
      print(f"old '{old}', new '{new}', sp '{session['p']}', su '{session['u']}'")
    else:
      msg = "Password is incorrect!"
  return render_template('changepsw.html', msg=msg)

@app.route('/account/delete', methods=['POST', 'GET'])
def delacc():
  msg = ''
  if request.method == "POST":
    if request.form.get("psw") == session['p']:
      db.del_account(session['u'])
      session.clear()
      return '<meta http-equiv="refresh" content="0; url=../../" />'
    else:
      msg == 'Password is incorrect!'
  return render_template('del.html', msg=msg)
    
@app.errorhandler(404)
def e404(e):
  return render_template('redirect.html')

app.run(host='0.0.0.0', port=8080, debug=True)
