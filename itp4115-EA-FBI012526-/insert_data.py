from app import db, app
from app.models import User, Post
from app.models import Show,Show_info,Show_info_comment
from sqlalchemy.orm import joinedload
app_context = app.app_context()
app_context.push()
db.drop_all()
db.create_all()

u1 = User(username='john', email='john@example.com')
u2 = User(username='susan', email='susan@example.com')

#插入节目
show1 = Show(name='守护甜心1',img = "https://img1.baidu.com/it/u=4151952692,1362282947&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=750")
db.session.add(show1)
#插入节目简介
show_info = Show_info(no=1,text='text'+str(1),show=show1)
db.session.add(show_info)

#插入节目
show2 = Show(name='速度与激情',img = "https://img1.baidu.com/it/u=4151952692,1362282947&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=750")
db.session.add(show2)
#插入节目简介
show_info2 = Show_info(no=1,text='这是简介'+str(1),show=show2)
db.session.add(show_info2)




#插入评论
for  i in range(10):
    comment = Show_info_comment(text="我会接着看!",comment_author=u1,which_show=show1)
    db.session.add(comment)

for  i in range(10):
    comment = Show_info_comment(text="我会接着看!",comment_author=u2,which_show=show2)
    db.session.add(comment)
db.session.commit()


# qyery all show
for e in db.session.query(Show.name,Show.img,Show.timestamp):
    print(e.name,e.img,e.timestamp)

# query comment by user name
for e in db.session.query(User).filter_by(username='john').one().comment:
    print(e)

for e in db.session.query(User).filter_by(username='susan').one().comment:
    print(e)

#query show info by show name
for e in db.session.query(Show).filter_by(name='守护甜心1').one().info_id:
    print(e)
# for e in db.session.query(Show.name,Show_info.text).join(Show_info).filter(Show.name=='守护甜心1'):
#     print(e[0],e[1])