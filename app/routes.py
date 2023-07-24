from app import app
from flask import request, send_file, render_template, jsonify, flash, url_for
from app.models import User, Path,Fina,Payment
import os
from app import db
from flask import redirect
from flask_login import login_user, logout_user, login_required,current_user
from app.forms import RegistrationForm
from datetime import datetime
from app.forms import Finan,Pay
from flask import Flask, render_template, jsonify
import pandas as pd


@app.route("/", methods = ["GET","POST"])
def nothing():
    return redirect("index")


@app.route('/index')
@login_required
def index():
    return render_template('index.html')


# '/login' -> 登录和注册
@app.route("/login" ,methods=["POST","GET"])
def  login():
    nextp = request.args.get("next")	#	当页面从原来的页面返回时带的参数，根据这个参数可以直接回到原来
    if request.method == 'GET':
        form=RegistrationForm()
        return render_template("log.html",error="",form=form)

    if request.method == "POST":
        q = request.form.get('hidden')	# 由于一个页面两个表单，由一个hidden的标签来区分，如果hidden有值，就是登录，否则注册
        if q:
            user = User.query.filter_by(name=request.form.get("name")).first()
            if (not user) or (not (user.check_password(request.form.get("password")))):
                flash('用户名或密码错误，请重新输入 mie ~')
                form = RegistrationForm()
                return render_template("log.html", form=form)
            else:
                login_user(user, remember=bool(request.form.get("remberme")))
                if nextp:
                    return redirect(nextp)
                return redirect("/index")
        else:
            if current_user.is_authenticated:
                return redirect(url_for('index'))
            else:
                form = RegistrationForm()
                if form.validate_on_submit():
                    with app.app_context():
                        user = User()
                        user.name = form.username.data
                        user.email = form.email.data
                        user.set_password(form.password.data)
                        db.session.add(user)
                        db.session.commit()
                        flash('注册成功！')
                    return redirect(url_for('login'))
                return render_template('log.html', title='error', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        with app.app_context():
            user = User()
            user.name = form.username.data
            user.email = form.email.data
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)




# 上传文件
@app.route("/upload",methods = ["POST","GET"])
@login_required
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    else:
        name = request.form.get("name")
        tag = request.form.get("tag")
        mes = request.form.get('mes')
        fn = request.form.get('files')
        f = request.files['files']
        fn = request.form.get('newFileName')
        if (fn):
            with app.app_context():
                P = Path.query.filter_by(name=name, tag=tag, fname=fn).all()
                if P:
                    mess = {"error":"同名文件上传失败！"}
                    return jsonify(mess)
                else:
                    path = "D:/app/app/db/{}/".format(tag) + fn
                    path = Path(path=path, tag=tag, name=name, fname=fn, data=datetime.now(),
                                user_id=current_user.id, mes=mes)
                    db.session.add(path)
                    db.session.commit()
                    f.save(os.path.join("D:/app/app/db/{}/".format(tag), fn))
                    mess = "文件上传成功，请继续选择操作"
                    return jsonify(mess)
        if not fn:
            path = "D:/app/app/db/{}/".format(tag) + f.filename
            with app.app_context():
                P = Path.query.filter_by(name=name, tag=tag, fname=f.filename).all()
                if P:
                    mess = {"error":"同名文件上传失败！"}
                    return jsonify(mess)
                else:
                    path = Path(path=path, tag=tag, name=name, fname=f.filename, data=datetime.now(),
                                user_id=current_user.id, mes=mes)
                    db.session.add(path)
                    db.session.commit()
                    f.save(os.path.join("D:/app/app/db/{}/".format(tag), f.filename))
                    mess = "文件上传成功，请继续选择操作"
                    return jsonify(mess)
#   下载文件
@app.route('/download/<path:filename>')
@login_required
def download(filename):
        path = "D:/app/db/uploads/" + filename
        return send_file(path, as_attachment=False)


@app.route("/drawing")
@login_required
def drawing():

    return render_template("drawing.html")


dic = {}
did = {}


@app.route("/direct/<string:tag>")
@login_required
def direct(tag):
    namel = set()
    with app.app_context():
        list = Path.query.filter_by(tag=tag).all()
        documents = []
        listP = []

        for i in list:
            namel.add(i.name)
            u = []
        for j in namel:
            u =Path.query.filter_by(name=j,tag=tag).all()
            u.sort(key=lambda x: x.data,reverse=True)
            listP.append(u)
        if len(listP) == 0:
            listP.append("null")
        # print(listP)
#  hash
        return render_template("direct.html",listP=listP,tag=tag,name=namel,t=len(namel))


@app.route("/view/<path:path>")
@login_required
def view(path):
    return send_file(path, as_attachment=False)


@app.route('/get_excel')
def get_excel():
    # 这里假设你有一个名为 "example.xlsx" 的 Excel 文件
    excel_file_path = r'D:\app\app\static\2023年辅料明细表.xls'
    return send_file(excel_file_path, as_attachment=True)
@app.route('/t')
def t():
    return render_template('t.html')

















@app.route("/<path:name>/<tag>")
def custom(name,tag):
    with app.app_context():
        u = Path.query.filter_by(tag=tag,name=name).all()
        u.sort(key=lambda x: x.data, reverse=True)
    return render_template("custom.html",u=u,tag=tag)


@app.route('/finan', methods=['GET', 'POST'])
# @csrf.exempt  # 关闭 CSRF 保护
def finan():
    form = Finan()
    if form.validate_on_submit():
        records = []
        num_records = len(request.form.getlist('data'))
        for i in range(num_records):
            data = request.form.getlist('data')[i]
            item = request.form.getlist('item')[i]
            vendor = request.form.getlist('vendor')[i]
            specification = request.form.getlist('specification')[i]
            unit = request.form.getlist('unit')[i]
            amount = (request.form.getlist('amount')[i])
            unit_price = (request.form.getlist('unit_price')[i])
            total_price =(request.form.getlist('price')[i])
            remark = request.form.getlist('remark')[i]
            category = request.form.getlist('category')[i]
            # 在这里创建对象并保存到列表中
            record = {
                'data': data,
                'item': item,
                'vendor': vendor,
                'specification': specification,
                'unit': unit,
                'amount': amount,
                'unit_price': unit_price,
                'price': total_price,
                'remark': remark,
                'category': category,
            }
            records.append(record)
        with app.app_context():
            for record in records:
                db.session.add(Fina(record))
            db.session.commit()
        return render_template('finan.html', mes="提交成功", form=form, records=records)
    return render_template('finan.html', form=form)

@app.route('/finanView/<category>')
def finanView(category):
    with app.app_context():
        if category == "laobao":
            category = "五金"
        f = Fina.query.filter_by(category=category).all()
        if not f:
            return "nothing"
        if f:
            return render_template("financial.html",f = f,a=len(f))





#   文件管理
@app.route('/fileManager')
def fileManager():
    return render_template('fileManager.html')


#   财务管理

@app.route('/finanManager')
def finanManager():
    return render_template('finanManager.html')

#  申购

@app.route('/buy')
def buy():
    return render_template('buy.html')


# 应收应付系统
@app.route('/pay')
def pay():
    form = Pay()
    if form.validate_on_submit():
        records = []
        num_records = len(request.form.getlist('data'))
        for i in range(num_records):
            clientName=request.form.getlist('clientName')[i]
            productName = request.form.getlist('productName')[i]
            price = request.form.getlist('price')[i]
            timeStart = request.form.getlist('timStart')[i]
            timeEnd = request.form.getlist('timeEnd')[i]
            time = request.form.getlist('time')[i]
            status = request.form.getlist('status')[i]
            note = request.form.getlist('note')[i]

            # 在这里创建对象并保存到列表中
            record = {
                'clientName':clientName,
                'productName':productName,
                'price':price,
                'timeStart':timeStart,
                'timeEnd':timeEnd,
                'time':time,
                'status':status,
                'note': note,
            }
            records.append(record)
        print(records)
        with app.app_context():
            for record in records:
                db.session.add(Payment(record))
            db.session.commit()
        return render_template('pay.html', mes="提交成功", form=form, records=records)
    return render_template('pay.html', form=form)
