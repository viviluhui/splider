# -*- coding:utf-8 -*-

'''
    weibo User
    {
        id, 微博ID
        username, 微博用户名
        introname,
        sex,
        member_level,
        industry,
        intro,
        verify,
    }
'''
import datetime
from sqlalchemy import Column,String,Integer,Time,Date,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class RequestInfo(Base):
    __tablename__ = 'request_info'

    '''
        请求状态 同http返回状态 
        999     未请求
        200     请求成功
        0       表示异常 无重启请求
        负值    cnt + 负值 > 0 也不再重启请求

        请求类别
        js
        media下载
    '''
    id = Column(Integer, primary_key=True)
    requestUrl = Column(String(256), comment='url')
    urlId = Column(String(128), unique=True, nullable=False, comment='url md5')
    requestName = Column(String(32), comment='请求名称')
    status = Column(Integer, default=999, comment='请求状态')
    requestDate = Column(Date, default=datetime.date.today(), comment='请求日期')
    requestTime = Column(Time, default=datetime.datetime.now().time(), comment='请求时间')
    updateTime = Column(Time, default=datetime.datetime.now().time(), comment='更新时间')
    runCnt = Column(Integer, default=1, comment='加载次数')

    def __repr__(self):
        return "<RequestInfo(id={} urlId={} requestUrl={})>".format(self.id, self.urlId, self.requestUrl)

    def __lt__(self, other):
        return self.requestTime < other.requestTime

class WeiboUser(Base):
    __tablename__ = 'weibo_user_info'
    id = Column(Integer, primary_key=True)
    userid = Column(String(48), comment='微博用户id')
    username = Column(String(128), comment='微博用户名')
    introname = Column(String(128), comment='微博介绍')
    gender = Column(String(8), comment='性别', default='1')
    province = Column(String(128), comment='所在省')
    city = Column(String(128), comment='所在市')
    birthday = Column(String(128), comment='生日')
    viplevel = Column(String(48), comment='用户等级')
    industry = Column(String(128), comment='所属行业')
    intro = Column(String(1024), comment='微博简介')
    verify = Column(String(4), comment='是否认证', default='0')
    member = Column(String(4), comment='是否会员', default='0')
    focusnumber = Column(String(48), comment='关注数量')
    fansnumber = Column(String(48), comment='粉丝数量')
    weibonumber = Column(String(48), comment='微博数量')

class WeiboInfo(Base):
    __tablename__ = 'weibo_info'
    id = Column(Integer, primary_key=True)
    weibo_url = Column(String(48), comment='微博的URL，可以作为微博的唯一标识')
    user_id = Column(String(48), comment='微博作者的ID')
    content = Column(String(48), comment='微博的内容')
    tool = Column(String(48), comment='发布的工具，一般是手机型号')
    created_at = Column(String(48), comment='微博发表时间')
    image_group = Column(String(48), comment='微博附带图的URL')
    repost_num = Column(String(48), comment='转发数')
    comment_num = Column(String(48), comment='评论数')
    like_num = Column(String(48), comment='点赞数')
    is_repost = Column(String(48), comment='是否是转发的微博')

class WeiboComment(Base):
    __tablename__ = 'weibo_comment_info'
    id = Column(Integer, primary_key=True)
    comment_url = Column(String(48), comment='这则评论的URL，可以作为唯一ID')
    user_id = Column(String(48), comment='评论的用户ID')
    weibo_url = Column(String(48), comment='weibo的URL')
    content = Column(String(48), comment='评论内容')
    created_at = Column(String(48), comment='评论创建时间')

class WeiboRelation(Base):
    __tablename__ = 'weibo_social_relation'
    id = Column(Integer, primary_key=True)
    fan_user_id = Column(String(48), comment='关注者的用户ID')
    follower_user_id = Column(String(48), comment='被关注者的用户ID')

engine = create_engine(r'sqlite:///D:\project\python\pylib\weibo.db?check_same_thread=False',echo=False)
Session = sessionmaker(bind=engine)
dbsession = Session()

def request_info_update_insert(requestInfo):
    info = dbsession.query(RequestInfo).filter( RequestInfo.urlId == requestInfo.urlId ).first()
    if info:
        info.status = requestInfo.status
        info.updateTime = datetime.datetime.now().time()
    else:
        dbsession.add(requestInfo)

def init_db():
    # 创建数据表。一方面通过engine来连接数据库，另一方面根据哪些类继承了Base来决定创建哪些表
    # checkfirst=True，表示创建表前先检查该表是否存在，如同名表已存在则不再创建。其实默认就是True
    Base.metadata.create_all(engine,checkfirst=True)
    # 上边的写法会在engine对应的数据库中创建所有继承Base的类对应的表，但很多时候很多只是用来则试的或是其他库的
    # 此时可以通过tables参数指定方式，指示仅创建哪些表
    # Base.metadata.create_all(engine,tables=[Base.metadata.tables['users']],checkfirst=True)
    # 在项目中由于model经常在别的文件定义，没主动加载时上边的写法可能写导致报错，可使用下边这种更明确的写法
    # User.__table__.create(engine, checkfirst=True)

def drop_db():
    # Base.metadata.drop_all(engine)
    RequestInfo.__table__.drop(engine)

if __name__=='__main__':
    drop_db()
    init_db()