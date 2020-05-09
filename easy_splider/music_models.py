# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import Column,String,Integer,Float,Time,Date,DateTime,create_engine
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
    requestUrl =  Column(String(256), comment='url')
    urlId = Column(String(128), unique=True, nullable=False, comment='url md5')
    requestName = Column(String(32), comment='请求名称')
    status = Column(Integer, default=999, comment='请求状态')
    requestDate = Column(Date, default=datetime.date.today(), comment='请求日期')
    requestTime = Column(Time, default=datetime.datetime.now().time(),comment='请求时间')
    updateTime = Column(Time, default=datetime.datetime.now().time(), comment='更新时间')
    runCnt = Column(Integer, default=1, comment='加载次数')

    def __repr__(self):
        return "<RequestInfo(id=[%d] urlId=[%s] requestUrl=[%s])>" % (self.id, self.urlId, self.requestUrl)

    def __lt__(self, other):
        return self.requestTime<other.requestTime

class MediaInfo(Base):
    __tablename__ = 'media_info'
    id = Column(Integer, primary_key=True)
    mediaId = Column(String(128), comment='URL ID')
    mediaUrl = Column(String(256), comment='媒体URL')
    artistId = Column(String(128), comment='歌手ID')
    mediaName = Column(String(256), comment='媒体名称')
    mediaLang = Column(String(32), comment='语种')
    country = Column(String(48), comment='地区')
    proxycompany = Column(String(256), comment='发行公司')
    compose = Column(String(32), comment='作曲人')
    writer = Column(String(32), comment='作词人')
    author = Column(String(32), comment='演唱人')
    publishTime = Column(String(18), comment='发行时间')
    albumName = Column(String(128), comment='专辑名称')
    lrcUrl = Column(String(256), comment='字幕url')
    mediaSize = Column(Integer(), comment='影音大小')
    mediaFormat = Column(String(18), comment='影音格式')
    albumId = Column(String(48), comment='媒体ID 歌手下唯一')
    source=Column(String(32), comment='来源')
    sourceDate = Column(DateTime, default=datetime.datetime.now(), comment='日期时间')
    useTime = Column(Float, comment='用时')
    useStatus = Column(String(2), default='00', comment='是否可用')
    downStatus = Column(String(2), default='00', comment='下载状态')
    downTime = Column(Float, comment='下载用时')

    def __repr__(self):
        return "<MediaInfo(id=[%d] mediaId=[%s] mediaName=[%s])>" % (self.id, self.mediaId, self.mediaName)

class ArtistInfo(Base):
    __tablename__ = 'artist_info'
    id = Column(Integer, primary_key=True)
    artistId = Column(String(128), comment='歌手ID')
    name = Column(String(128), comment='名称')
    area = Column(String(48), comment='地区')
    birth = Column(String(16), comment='生日')
    startBirth = Column(String(24), comment='星座')
    introduce = Column(String(1000), comment='介绍')

engine = create_engine(r'sqlite:///D:\project\python\pylib\music.db?check_same_thread=False',echo=False)
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
    Base.metadata.create_all(engine,checkfirst=True)

def drop_db():
    # Base.metadata.drop_all(engine)
    RequestInfo.__table__.drop(engine)

if __name__=='__main__':
    drop_db()
    init_db()