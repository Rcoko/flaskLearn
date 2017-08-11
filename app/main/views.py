# -- coding: utf-8 --
from flask import render_template, session, redirect, url_for, current_app, request
from .. import db
from ..models import Detail,Contents,Keywords,WXUrls
from . import main
from .forms import NameForm
import wechatsogou
import hashlib
from .errors import *
from ..API.reqweb import *


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
    md5_string = ''
    keywords = ''
    title = ''
    des = ''

    #try:
    if keyword.strip() != '':
        lists = vx_obj.search_article(keyword)
        for list in lists:
            wx_url = list['article']['url']
            hash = hashlib.md5()
            hash.update(bytes(wx_url))
            md5_str = hash.hexdigest()
            #list['article'].append('wx_url_md5')
            list['article']['wx_url_md5']=md5_str
            wx_urls = WXUrls(md5_str = md5_str,wx_url=wx_url)
            wx_urls.save()
        sugg_keywords = vx_obj.get_sugg(keyword)
    #except:
    #    print('value errot')

    key_count = len(sugg_keywords)


    if  key_count == 1:
        title = keywords= sugg_keywords[0]
    elif  key_count > 1:
        title = keyword+'_'+sugg_keywords[0]
        for sugg_key in sugg_keywords:
            keywords = keywords+ ','+sugg_key
        keywords = keywords[1:]
    else:
        title =keywords= keyword

    if title.strip() != '':
        hash = hashlib.md5()#md5对象，md5不能反解，但是加密是固定的，就是关系是一一对应，所以有缺陷，可以被对撞出来
        hash.update(bytes(title))#要对哪个字符串进行加密，就放这里
        md5_string = hash.hexdigest()#拿到加密字符串
        keywrods_id = Keywords(md5_string = md5_string,title=keyword)
        keywrods_id.save()
    else:
        print '404.html'

    return render_template('content.html',content_list = lists,title=title,keywords=keywords,des=des,sugg_keywords=sugg_keywords)


@main.route('/post/',methods=['GET', 'POST'])
def post():
    url_md5=request.args.get('md5')
    wx_urls = WXUrls.objects(md5_str=url_md5)[:1]
    if wx_urls.count() == 1:
        wx_url=wx_urls[0].wx_url
        ReqWebInfo.get_wx_article_info(wx_url)
        return render_template('detail.html',)
    else:
        return render_template('404.html')

