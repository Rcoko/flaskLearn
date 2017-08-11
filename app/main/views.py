# -- coding: utf-8 --
from flask import render_template, session, redirect, url_for, current_app, request
from .. import db
from ..models import Detail,Contents
from . import main
from .forms import NameForm
import wechatsogou

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))


@main.route('/test/')
def test():
    content = Contents(name="test内容");
    todo1 = Detail(title='teest title', keywords='列表列表列表',description='描述描述描述描述描述',contents=content)
    todo1.save()
    ss = Detail.objects().all()
    objLen = len(ss)
    s1 = ss[0]
    a = 4
    #todo1.save()
    return render_template('detail.html',detail = s1)



@main.route('/content/',methods=['GET', 'POST'])
def content():
    keyword=request.args.get('key')
    vx_obj = wechatsogou.WechatSogouAPI()
    lists = []
    sugg_keywords = []

    try:
        lists = vx_obj.search_article(keyword)
        sugg_keywords = vx_obj.get_sugg(keyword)
    except:
        print('value errot')

    title = '标题'
    keywords = '关键词，关键词2，关键词3'
    des = '描述描述描述描述'
    return render_template('content.html',content_list = lists,title=title,keywords=keywords,des=des,sugg_keywords=sugg_keywords)