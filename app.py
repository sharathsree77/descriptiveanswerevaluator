# import the Flask class from the flask module
from flask import Flask, render_template, flash, session
#from flask_bootstrap import Bootstrap
from flask import Flask, render_template, redirect, url_for, request
import pymysql
import pymysql.cursors
import re

import Similarity_wn_pos
from Similarity_wn_pos import similarityMatcher
import levenshtein
from levenshtein import levenshtein1
import cosine
from cosine import cosine1
import jaccard 
from jaccard import jaccard1
import dice
from dice import dice1


# create the application object
app2 = Flask(__name__)
#Bootstrap(app2)
#global studAns
#studAns="hi"
#global tutAns
#tutAns="hi"
# use decorators to link the function to a url

connection = pymysql.connect(host='localhost',user='root', password='822315',db='project',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

@app2.route('/',methods=['GET', 'POST'])
def home():
    error=None
    #print(ans)
    #try:
        #with connection.cursor() as cursor:
            # Read a single record
            #sql = "DELETE FROM `stud` ;" 
            #cursor.execute(sql)
        #connection.commit()
    #except Exception as e:
        #print(e)
        #return e
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "CREATE TABLE IF NOT EXISTS nums"+" (`id` int(11) NOT NULL AUTO_INCREMENT,`no` int(11) NOT NULL, `sub` varchar(255),PRIMARY KEY (`id`))AUTO_INCREMENT=1 ;" 
            cursor.execute(sql)
        connection.commit()
    except Exception as e:
        print(e)
        return e
    #finally:
    #    connection.close()
           # return render_template('invalidOpt.html',error=error)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "CREATE TABLE IF NOT EXISTS results"+" (`id` int(11) NOT NULL AUTO_INCREMENT,`usn` varchar(255) NOT NULL, `subject` varchar(255) NOT NULL,`question` varchar(255) NOT NULL, `tutans` varchar(1000) NOT NULL, `studans` varchar(1000) NOT NULL, `marks` varchar(255) NOT NULL,`cosine` varchar(255) NOT NULL,`levenshtein` varchar(255) NOT NULL,`jaccard` varchar(255) NOT NULL,`dice` varchar(255) NOT NULL,`semantic` varchar(255) NOT NULL,`total` varchar(255) NOT NULL,PRIMARY KEY (`id`))AUTO_INCREMENT=1 ;"
            cursor.execute(sql)
        connection.commit()
    except Exception as e:
        print(e)
        return e
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "CREATE TABLE IF NOT EXISTS stud"+" (`id` int(11) NOT NULL AUTO_INCREMENT,`usn` varchar(255) NOT NULL, `answer` varchar(1000) NOT NULL,`subject` varchar(255) NOT NULL,PRIMARY KEY (`id`))AUTO_INCREMENT=1 ;"
            cursor.execute(sql)
        connection.commit()
    except Exception as e:
        print(e)
        return e
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "CREATE TABLE IF NOT EXISTS subjects"+" (`id` int(11) NOT NULL AUTO_INCREMENT,`subname` varchar(255) NOT NULL, PRIMARY KEY (`id`))AUTO_INCREMENT=1 ;"
            cursor.execute(sql)
        connection.commit()
    except Exception as e:
        print(e)
        return e
    return render_template("alerts-copy.html",error=error)
"""
     return
       
    <font face="garamond" size=6 color="purple">
    <h1>
    <center>Welcome to Automated Descriptive Answers Evaluator</center>
    </h1>
    </font>
    <body bgcolor="pink">
    <br>
    <br><br>   
    <p align="left"><a href="/loginT"><font face="comic sans ms"  size=6 color="navy">TutorLogin</font></a>  
    <br>
    <br><br>   
    <a href="/loginS"><font face="comic sans ms"  size=6 color="navy">StudentLogin</font></a>
    """

@app2.route('/about', methods=['GET', 'POST'])
def abt():
    error = None
    return render_template('about.html',error=error)  # render a template

@app2.route('/testAvailable', methods=['GET', 'POST'])
def testAvail():
    error = None
    res3=[]
    try:

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`,`sub` FROM `nums`"
            cursor.execute(sql)
            result3 = cursor.fetchall()
            #print(result3)
            #d=result2['id']
            #e=result2['sub']
            #n1=int(d)
            print(result3)
            #print(d)
            #print(e)
    finally:
        print("ENTEREDDDDDDDDDD")
    #n=int(num)
    #return "Done"
    idd=[]
    subb=[]
    print(result3)
    for i in range(0, len(result3)):
        print(result3[i]['id'])
        idd.append(result3[i]['id'])
        subb.append(result3[i]['sub'])
    print(idd)
    print(subb)
    #return "DONEE"
    return render_template('testAvailable.html',id_d=idd, sub_b=subb)  # render a template

@app2.route('/loginT', methods=['GET', 'POST'])
def loginTut():
    error = None
    global v
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error='invalid'
            return render_template('invalidTut.html',error=error)
        else:
            return render_template('tutoption.html',error=error)
            #return redirect(url_for('enter_num'))
    return render_template('index.html',error=error)  # render a template

@app2.route('/signup',methods = ['POST','GET'])
def signUp():
    return render_template('signup.html')

@app2.route('/signUpStud',methods = ['GET','POST'])
def signUpStud():
    if request.method == 'POST': 
        usn = request.form['username']
        password = request.form['password']
        with connection.cursor() as cursor:
                
            sql = "INSERT INTO `studlogin` (`usn`,`pass`) VALUES (%s,%s)"
            cursor.execute(sql, (usn,password))
                    
            connection.commit()
        #connection.close()
    return render_template('indexS.html')
@app2.route('/loginS', methods=['GET', 'POST'])
def loginStud():
    global usn
    usn=""
    error = None
    global z
    z=0
    global sa
    sa=[]
    if request.method == 'POST':
        usn=request.form['username']
        with connection.cursor() as cursor:
            sql = "SELECT  `pass`  FROM `studlogin` WHERE `usn`=%s"
            cursor.execute(sql, (usn ))
            result = cursor.fetchall()
        
        if( len(result)==1 and request.form['password'] == result[0]['pass']):
            return testSelection()
        else:
            return render_template('invalidStud.html',error=error)
        #if request.form['username'] != 'stud' or request.form['password'] != 'stud':
            #error='invalid'
            #return "invalid"
        #else:
            #return redirect(url_for('welStud'))
    return render_template('indexS.html',error=error)  # render a template

def simil():
    #print(studAns+ tutAns)
    global usn
    global s
    global li
    global ai
    res=[]
    rc=[]
    rd=[]
    rl=[]
    rj=[]
    #return "HIIIII"
    print("SIMIL")
    print(li)
    print(ai)
    #return "hi"
    
    try:
        #with connection.cursor() as cursor:
            # Create a new record
            #sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            #cursor.execute(sql, ('webmaster@python.org', 'very-secret'))


        #connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `answer`, `subject`, `usn` FROM `stud` WHERE `usn`=%s AND `subject`=%s"
            cursor.execute(sql, (usn, s ))
            result = cursor.fetchall()
            print(result)
            print(len(li))
            #return "jj"
            si=[]
            ui=[]
            su=[]
            for j in range(0,len(li)):
                a=result[j]
                si.append(a['answer'])
                ui.append(a['usn'])
                su.append(a['subject'])
    finally:
        print("entered")        
    
    for i in range(0,len(ai)):
        
        vl=levenshtein1(ai[i],si[i])
        rl.append(vl)
        vc=cosine1(ai[i],si[i])
        rc.append(vc)
        vj=jaccard1(ai[i],si[i])
        rj.append(vj)
        vd=dice1(ai[i],si[i])
        rd.append(vd)
        vs=similarityMatcher(si[i], ai[i])
        #vs=similarityMatcher(ai[i], si[i])
        res.append(vs)
    
    print(str(res)+"%")
    tot=0
    for i in range(0,len(ai)):
        tot+=float(res[i])
    tot=tot/len(ai)
    print("FFFFFFFFFFFFFFFFFFFFFFFFF")
    print(tot)
    for i in range(0,len(ai)):
        
        try:
            print(usn)
            print(ai[i])
            print(li[i])
            print(res[i])
            print(str(rc[i]))
            print(rl[i])
            print(rj[i])
            print(rd[i])
            print(res[i])
            with connection.cursor() as cursor:
            # Read a single record
                sql = "INSERT INTO `results` (`usn`, `subject`, `question`,`tutans`, `studans`, `marks`, `cosine`,`levenshtein`, `jaccard`, `dice`, `semantic`,`total`)VALUES (%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, (usn,s,str(li[i]),str(ai[i]),str(si[i]),str(res[i]),str(rc[i]),str(rl[i]),str(rj[i]),str(rd[i]),str(res[i]),str(tot)))
            #result = cursor.fetchall()
            #print(result)
                print(len(li))
            #return "jj"
            connection.commit()
        finally:
            print("entered")         
    #return "Done"
    return render_template('resultPage.html',t_q=li,t_a=ai,s_a=si,n=len(ai),result=res,total=tot)

@app2.route('/options',methods=['GET', 'POST'])
def enter_page():
    error=None
    global v
    #return "OPTIONS"
    if request.method == 'POST':
        v=request.form['testn']
        print(v)
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `subjects` (`subname`) VALUES (%s)"
                cursor.execute(sql, (v))
                #result = cursor.fetchall()
            connection.commit()
        finally:
                print("ENTERED")
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "CREATE TABLE "+v+" (`id` int(11) NOT NULL AUTO_INCREMENT,`question` varchar(1000) NOT NULL, `answer` varchar(1000) NOT NULL,PRIMARY KEY (`id`))AUTO_INCREMENT=1 ;"
                cursor.execute(sql)
            connection.commit()
        except Exception as e:
            print(e)
            return render_template('invalidOpt.html',error=error)
        return redirect(url_for('enter_num'))
    return render_template('testname.html',error=error)  # render a template

@app2.route('/results',methods=['GET', 'POST'])
def res():
    #print(studAns+ tutAns)
    res2=[]
    try:

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`,`sub` FROM `nums`"
            cursor.execute(sql)
            result2 = cursor.fetchall()
            #print(result1)
            #d=result2['id']
            #e=result2['sub']
            #n1=int(d)
            print(result2)
            #print(d)
            #print(e)
    finally:
        print("ENTEREDDDDDDDDDD")
    #n=int(num)
    #return "Done"
    idd=[]
    subb=[]
    print(result2)
    for i in range(0, len(result2)):
        print(result2[i]['id'])
        idd.append(result2[i]['id'])
        subb.append(result2[i]['sub'])
    print(idd)
    print(subb)
    #return "DONEE"
    return render_template('selectTestRes.html',id_d=idd, sub_b=subb)

@app2.route('/respage',methods=['GET', 'POST'])
def res_page():

    if(request.method=='POST'):
        code1=request.form['code']
        try:
            cod=int(code1)
        except:
            return render_template('invalidCodeRes.html')
        print(cod)
        
        
        s=""
        z=0
        try:

            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `sub` FROM `nums` WHERE `id`=%s"
                cursor.execute(sql,(cod))
                result = cursor.fetchone()
                
                s=result['sub']
                print(result)
        except Exception as e:
            return render_template('invalidCodeRes.html')
                
        finally:
            print("ENTERED")
        try:

            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `usn`, `subject`, `question`,`tutans`, `studans`, `marks`, `cosine`,`levenshtein`, `jaccard`, `dice`, `semantic`,`total` FROM `results` WHERE `subject`=%s"
                cursor.execute(sql,(s))
                result = cursor.fetchall()
                print(result)
                print(len(result))
                #return "HHHH"

        finally:
            print("ENTERED")
            #return("opp")
        #x=int(num)
        u=[]
        su=[]
        q=[]
        t=[]
        st=[]
        m=[]
        c=[]
        l=[]
        j=[]
        d=[]
        s=[]
        tot=[]
        summ=0
        for i in range(0,len(result)):
            u.append(result[i]['usn'])
            su.append(result[i]['subject'])
            q.append(result[i]['question'])
            t.append(result[i]['tutans'])
            st.append(result[i]['studans'])
            m.append(result[i]['marks'])
            c.append(result[i]['cosine'])
            l.append(result[i]['levenshtein'])
            j.append(result[i]['jaccard'])
            d.append(result[i]['dice'])
            s.append(result[i]['semantic'])
            tot.append(result[i]['total'])
            summ += float(tot[i])
        #print(u+su+q) 
        avg = summ / len(result)         
        return render_template('tutResPage.html',n=len(result),u1=u,su1=su,q1=q,t1=t,st1=st,m1=m,c1=c,l1=l,j1=j,d1=d,s1=s,tot1=tot,avg = avg)

        
@app2.route('/num',methods=['GET', 'POST'])
def enter_num():
    global v
    #print("V HERE"+v)
    global num
    global res
    res=[]
    global y
    y=0
    global z
    z=0
    global q
    q=[]
    global ta
    ta=[]
    global tq
    tq=[]
    global sa
    sa=[]
    error=None
    if(request.method=='POST'):
        num1=request.form['num']
        try:
            num=int(num1)
            if(num<1):
                return render_template('invalidNum.html')
        except Exception as e:
            return render_template('invalidNum.html')
        #print(num)
        #for i in range(0,num):
        #    return redirect(url_for('welTut'))
        #simil(ans)
        
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `nums` (`no`,`sub`) VALUES (%s,%s)"
                cursor.execute(sql,(num,v))


            connection.commit()
        finally:
                print("ENTERED")
        return redirect(url_for('welTut'))
    return render_template('NumberPageMod.html')  # return a string

@app2.route('/welcomeT',methods=['GET', 'POST'])
def welTut():
    global v
    try:
        #with connection.cursor() as cursor:
            # Create a new record
            #sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            #cursor.execute(sql, ('webmaster@python.org', 'very-secret'))


        #connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `no` FROM `nums` WHERE `id`=(SELECT max(`id`) FROM `nums`)"
            cursor.execute(sql)
            result = cursor.fetchone()
            d=result['no']
            x=int(d)
            print(result)
            print(x)
    finally:
        print("ENTERED")
    #x=int(num)
    global y
    error=None
    if(request.method=='POST'):
        global tutAns
        tq.append(request.form['Text1'])
        ta.append(request.form['Text2'])
        tutAns=request.form['Text2']
        #print(tutAns+str(x))
        #print(ta)
        
        y=y+1
        if(y<x):
            try:
                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT INTO "+v+" (`question`, `answer`) VALUES (%s, %s)"
                    cursor.execute(sql, (tq[y-1], ta[y-1]))


                connection.commit()

                #with connection.cursor() as cursor:
                    # Read a single record
                    #sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                    #cursor.execute(sql, ('webmaster@python.org',))
                    #result = cursor.fetchone()
                    #print(result)
            finally:
                print("ENTERED")
            return render_template('tutorsPage.html',no=num)
        #simil(ans)
        try:
                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT INTO "+v+" (`question`, `answer`) VALUES (%s, %s)"
                    cursor.execute(sql, (tq[y-1], ta[y-1]))


                connection.commit()

        finally:
                print("ENTERED")
        return render_template('donePage.html')
    return render_template('tutorsPage.html',no=num)  # return a string

@app2.route('/testSelection',methods=['GET', 'POST'])
def testSelection():
    #print(studAns+ tutAns)
    res1=[]
    try:

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`,`sub` FROM `nums`"
            cursor.execute(sql)
            result1 = cursor.fetchall()
            #print(result1)
            #d=result1['id']
            #e=result1['sub']
            #n1=int(d)
            print(result1)
            #print(d)
            #print(e)
    finally:
        print("ENTEREDDDDDDDDDD")
    #n=int(num)
    #return "Done"
    idd=[]
    subb=[]
    print(result1)
    for i in range(0, len(result1)):
        print(result1[i]['id'])
        idd.append(result1[i]['id'])
        subb.append(result1[i]['sub'])
    print(idd)
    print(subb)
    #return "DONEE"
    return render_template('selectTest.html',id_d=idd, sub_b=subb)

@app2.route('/welcomeS',methods=['GET', 'POST'])
def welStud():
    global s
    s=""
    if(request.method=='POST'):
        code1=request.form['code']

        print((code1))
        
        with connection.cursor() as cursor:
                # Create a new record
                sql = "SELECT COUNT( DISTINCT 'subname' ) as count FROM `subjects`"
                cursor.execute(sql)
                result = cursor.fetchall()
        connection.commit()
        cod=int(code1)
        print(result)
        if(cod> result[0]["count"] and cod<1):
            return render_template('invalidSubCode.html')
        

   
            
        print(cod)
        global li
        li=[]
        global ai
        ai=[]
        global sa
        sa=[]
        global x
        #return "hi"
        
        global z
        z=0
        try:

            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `no`,`sub` FROM `nums` WHERE `id`=%s"
                cursor.execute(sql,(cod))
                result = cursor.fetchone()
                d=result['no']
                s=result['sub']
                x=int(d)

                print(result)
                print(x)
        except Exception as e:
            print("hello")
            return render_template('invalidSubCode.html')
        finally:
            print("ENTERED")
            #return("opp")
        #x=int(num)
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `question`, `answer` FROM "+s
                cursor.execute(sql)
                result = cursor.fetchall()
                li=[]
                ai=[]
                for j in range(0,x):
                    a=result[j]
                    li.append(a['question'])
                    ai.append(a['answer'])
        finally:
            print(li)
            #return "dooo"
            return redirect(url_for('studans'))

@app2.route('/StudAns',methods=['GET', 'POST'])
def studans():        
    global sa
    global z
    global li
    global x    
    if(request.method=='POST'):
        error=None

        print("HI")
        print(li)
        #return "jj"
        global studAns
        studAns=request.form['Text2']
        sa.append(request.form['Text2'])
        print(sa) 
        z=z+1
        if(z<x):
            try:
                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT INTO `stud` (`usn`, `answer`,`subject`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (usn, sa[z-1], s))


                connection.commit()

            except Exception as e:
                return str(e)
            finally:
                print("ENTERED")
            return render_template('studentsPage.html',ques=li, index=z)
        print(z)
        try:
                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT INTO `stud` (`usn`, `answer`, `subject`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (usn, sa[z-1], s))


                connection.commit()

        finally:
                print("ENTERED")
        return simil()
        #return "DONE"
    return render_template('studentsPage.html', ques=li, index=0)  # return a string


# start the server with the 'run()' method
if __name__ == '__main__':
    app2.secret_key='abcd'
    app2.run(debug=True)