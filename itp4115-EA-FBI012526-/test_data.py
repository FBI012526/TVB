# from app import db, app
# from app.models import User, Post
# from app.models import Show,Show_info,Show_info_comment
# from sqlalchemy.orm import joinedload
# app_context = app.app_context()
# app_context.push()
# # db.drop_all()
# # db.create_all()
# #
# # u1 = User(username='john', email='john@example.com')
# # u2 = User(username='susan', email='susan@example.com')
# # u1.set_password("P@ssw0rd")
# # u2.set_password("P@ssw0rd")
# # db.session.add(u1)
# # db.session.add(u2)
# # u1.follow(u2)
# # u2.follow(u1)
# #
# # p1 = Post(body='my first post!', author=u1)
# # p2 = Post(body='my first post!', author=u2)
# # db.session.add(p1)
# # db.session.add(p2)
#
#
# #My test
# #
# # u1 = User(username='ab', email='susan3@example.com')
# # u2 = User(username='b', email='susan5@example.com')
# #
# # show1 = Show(name='守护甜心1',img = "https://img1.baidu.com/it/u=4151952692,1362282947&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=750"
# #             )
# # show2 = Show(name='守护甜心2',img = "https://img1.baidu.com/it/u=4151952692,1362282947&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=750"
# #             )
# #
# # db.session.add(show1)
# # db.session.add(show2)
# # for  i in range(10):
# #     e = Show_info(no=i,text='text'+str(i),show=show1)
# #     db.session.add(e)
# #
# # for  i in range(10):
# #     e = Show_info(no=i,text='text'+str(i),show=show2)
# #     db.session.add(e)
# #
# # for  i in range(10):
# #     comment = Show_info_comment(text="我会接着看!",comment_author=u1,which_show=show1)
# #     db.session.add(comment)
# # for  i in range(10):
# #     comment = Show_info_comment(text="我会接着看!",comment_author=u2,which_show=show2)
# #     db.session.add(comment)
# # db.session.commit()
# #
# #
# # qyery all show
# # for e in db.session.query(Show.name,Show.img,Show.timestamp):
# #     print(e.name,e.img,e.timestamp)
# #
# # # query comment by user name
# # for e in db.session.query(User).filter_by(username='ab').one().comment:
# #     print(e)
# #
# # for e in db.session.query(User).filter_by(username='b').one().comment:
# #     print(e)
# #
# # #query show info by show name
# # for e in db.session.query(Show).filter_by(name='守护甜心1').one().info_id:
# #     print(e)
# # for e in db.session.query(Show.name,Show_info.text).join(Show_info).filter(Show.name=='守护甜心1'):
# #     print(e[0],e[1])
# # result = db.session.query(Show,Show_info.text).join(Show_info).filter(Show.name=='守护甜心1').paginate(
# #     page=1, per_page=100, error_out=False)
# # for e in result:
# #     print(e[0].name)