from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from flask_babel import _, get_locale
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, \
    ResetPasswordRequestForm, ResetPasswordForm,CommentForm
from app.models import User, Post,Show,Show_info,Show_info_comment
from app.email import send_password_reset_email


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    return redirect(url_for('explore'))


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)

    #获取节目 和对应简介
    ret = db.session.query(Show,Show_info.text).join(Show_info).paginate(
        page=page, per_page=app.config["POSTS_PER_PAGE"], error_out=False)

    next_url = url_for(
        'explore', page=ret.next_num) if ret.next_num else None
    prev_url = url_for(
        'explore', page=ret.prev_num) if ret.prev_num else None
    datas = []

    #将获取到的数据解析成list，每个成员为字典
    for e in ret:
        print(e[0].id,e[0].name,e[0].timestamp,e[0].img,e[1])
        data ={ 'id':e[0].id,
            'name':e[0].name,
             'timestamp':e[0].timestamp,
             'info':e[1],
             'img':e[0].img}
        datas.append(data)

    return render_template('index.html_.j2', title=_('Explore'),
                           shows=datas, next_url=next_url,
                           prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html.j2', title=_('Sign In'), form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('login'))
    return render_template('register.html.j2', title=_('Register'), form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('login'))
    return render_template('reset_password_request.html.j2',
                           title=_('Reset Password'), form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if user is None:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('login'))
    return render_template('reset_password.html.j2', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.followed_posts().paginate(
        page=page, per_page=app.config["POSTS_PER_PAGE"], error_out=False)
    next_url = url_for(
        'index', page=posts.next_num) if posts.next_num else None
    prev_url = url_for(
        'index', page=posts.prev_num) if posts.prev_num else None

    #edited
    _ = db.session.query(User).filter_by(username=username).one().comment
    coms =[]
    for e in _:
        show_id = e.show_id
        showname = db.session.query(Show.name).filter_by(id = show_id).all()[0][0]
        print(showname)
        coms.append({'username':username,
                     'timestamp':e.timestamp,
                     'comment':e.text})
    return render_template('user.html.j2', user=user, posts=posts.items,coms=coms,
                           next_url=next_url, prev_url=prev_url,
                           showname=showname)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html.j2', title=_('Edit Profile'),
                           form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('user', username=username))


#added
@app.route('/show/<show_id>/<show_name>',methods=['post','get'])
@login_required
def show(show_id,show_name):
    #print(current_user)
    form = CommentForm()
    if form.validate_on_submit():

        comment = Show_info_comment(text=form.comment.data,show_id=show_id,user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        #flash(_('Your post is now live!'))
    #     #return redirect(url_for('show',show_id=show_id,show_name=show_name))
    result = db.session.query(Show).filter_by(id=show_id).one().comment_id.order_by(Show_info_comment.timestamp.desc()).all()
    ret=[]
    for e in result:
        user = db.session.query(User).filter_by(id=e.user_id).all()[0]
        ret.append({'username':user.username,'comment':e.text,'timestamp':e.timestamp})


    return  render_template('show_comment.html.j2',coms =ret,showname=show_name,form=form)


