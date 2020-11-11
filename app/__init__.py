from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    g,
    abort,
    session,
)
import pymysql

#user 클래스를 만들어 user 객체를 클래스에서 만든 전역변수인 리스트에 append 한다.
#데이터 베이스를 사용하는 대신에 app 에 global 변수를 사용한다. 
class User:
    def __init__(self,id,username,password):
        self.id = id
        self.username = username
        self.password = password
    
      
    def __repr__(self):
        return f'<User:{self.username}' 

class Set:
    def __init__(self,cnt,name='로그인'):
        self.cnt = cnt
        self.name= name
    def setName(self,name):
        self.name = name  

User = Set(0)

#모든 유저들을 나타내는 전역변수 만듬. User 인스턴스들을 append 함


# users = [] 
# users.append(User(id=1,username='우상',password='password1' )) 




print(users[0].password) 

app = Flask(__name__)
app.config.update(
    SECRET_KEY ="woosangyoon1234",
    SESSION_COOKIE_NAME="User_cookie"
)

@app.before_request
def before_request():
    g.db = pymysql.connect(host="localhost", port=3306,user='root',passwd='ywoosang',db='user_db',charset='utf8') 
    #g.user 을 설정. 
    g.user = None
    if 'user_id' in session:
        user_list= [x for x in users if x.id == session['user_id']]
        if user_list == [] :
            user = None
        else :
            user =user_list[0]
        g.user = user 


@app.teardown_request
def teardown_request(exeption):
    g.db.close()  

@app.route('/login', methods=["GET","POST"])
def login():
    #post 로 왔다는 것은 정보를 재전송하고 로그인 버튼을 누른것. 
    if request.method == 'POST' :
        session.pop('user_id', None) 
        #항상 유저가 로그인 시도할 때마다 session 의 user_id 를 pop (제거) 처음부터 다시 시작 
        # 이미 로그인 되어 있는 한경험이 있는 상태에서 다시 로그인을 시도할 때 , 기존에 있던 세션을 제거하고 새로운 새션을 발급한다.
        # 로그인을 다시 하려고 할때 비밀번호를 잘못 치면 로그아웃되고 기존에 로그인을 하고있더라도 다시 정확한 비밀번호를 입력해야한다. 
        user_id = request.form.get('Id')
        user_pw = request.form.get('passwd')

        sql = """select id from user_table where id = '%s' """ % user_id
        cursor.execute(sql)
        select_id = cursor.fetchone()
        sql = """SELECT pwd from user_table where pwd = '%s' """ % user_pw
        cursor.execute(sql)
        select_pwd = cursor.fetchone()
        #오류 방지를 위해 strip 으로 가능한 경우 모두제거 
        db_id = str(select_id).strip(" ,('')")  
        db_pw = str(select_pwd).strip(" ,('')")
        
        if user_id == db_id and user_pw == db_pw :
            g.id = db_id
            g.pw = db_pw
            #아이디 비번이 일치할 경우 메인페이지로 이동 
            sql = """SELECT user_name from user_table where pwd = '%s' """ % user_pw
            cursor.execute(sql)
            #이름 오류 있을시 확인 요망
            raw_name= cursor.fetchone()
            name = str(raw_name).strip(" ,('')")
            User.setName(name) 
            #key : user_id  세션 설정 
            # 여기있는 세션은 cookie 로 내려보내짐. 
            session['user_id'] = user.id
            #메인 페이지로 이동시킴
            return redirect(url_for('mainPage',name="%s" %  str(User.name)))
        else:
            #일치하지 않을 경우 실패 횟수를 증가시키고 다시 로그인 페이지로 이동
            User.cnt +=1
            print(User.cnt)
            #실패 횟수가 3번 이상일 경우 없는 회원으로 간주하고 가입페이지로 이동 
            if User.cnt >= 3 :
               User.cnt = 0 
               return redirect(url_for('signup'))
            return redirect(url_for('login',alert="로그인오류 "+str(User.cnt)+"회") )
        return render_template('login.html',alert=alert)



@app.route('/profile')   
def profile():
    if not g.user:
        # 세션이 없는 유저라면 forbidden error 내고 로그인 페이지로 이동시키기
        abort(403) 
        return render_template('login.html')
    return render_template('profile.html')   


app.run(host='0.0.0.0',debug=True)

#유저가 로그인폼에 입력하면 app이 username과 password 가 맞는지 검사하고 
# 맞다면 app 은 session 을 이용해 user 가 로그인했는지, 로그인하지 않았는지 log 를 적고
# 프로필 페이지로 redirect 시킨다. 



 

