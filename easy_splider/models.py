# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import Column,Integer,String,Text,Float,Date,Time,create_engine,UniqueConstraint
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
    urlId = Column(String(128), nullable=False, comment='url md5')
    requestName = Column(String(32), comment='请求名称')
    status = Column(Integer, default=999, comment='请求状态')
    requestDate = Column(Date, default=datetime.date.today(), comment='请求日期')
    requestTime = Column(Time, default=datetime.datetime.now().time(), comment='请求时间')
    updateTime = Column(Time, default=datetime.datetime.now().time(), comment='更新时间')
    runCnt = Column(Integer, default=1, comment='加载次数')

    __table_args__ = (
        UniqueConstraint('urlId', 'requestName', name='unique_idx1'),
    )

    def __repr__(self):
        return "<RequestInfo(id=[%d] urlId=[%s] requestUrl=[%s])>" % (self.id, self.urlId, self.requestUrl)

    def __lt__(self, other):
        return self.requestTime < other.requestTime

class JobInfo(Base):
    __tablename__='job_info'
    id = Column(Integer(), primary_key=True)
    jobId= Column(String(100), comment='职位ID')
    companyName= Column(String(100), comment='企业名称')
    companyType = Column(String(100), comment='企业类型')
    companyScale = Column(String(100), comment='企业规模')
    companyTrade = Column(String(100), comment='企业经营范围')
    companyWelfare = Column(String(1000), comment='企业福利')
    jobName = Column(String(100), comment='职位名称')
    jobPay = Column(String(50), comment='职位薪酬')
    jobYear = Column(String(40), comment='工龄要求')
    jobEdu = Column(String(40), comment='学历要求')
    jobMember = Column(String(40), comment='招聘人数')
    jobAddr = Column(String(1000), comment='上班地址')
    jobDesc = Column(Text, comment='工作描述')
    jobDate = Column(String(40), comment='发布日期')
    url = Column(String(100), comment='招聘信息页URL')
    sourceId = Column(String(40), comment='招聘来源')
    sourceDate = Column(String(18), comment='日期')
    parseTime = Column(Float, comment='解析用时')

    def __repr__(self):
        return "<JobInfo(id=[{}] jobid=[{}] companyName=[{}])>".format(self.id, self.jobId, self.companyName)

    def __lt__(self, other):
        return self.sourceDate < other.sourceDate

base_path=r'D:\project\python\spider'
db_url = 'sqlite:///{}\jobs.db?check_same_thread=False'.format(base_path)

engine = create_engine(db_url,echo=False)
Session = sessionmaker(bind=engine)
dbsession = Session()

def request_info_update_insert(requestInfo):
    info = dbsession.query(RequestInfo).filter( RequestInfo.urlId == requestInfo.urlId ).first()
    if info:
        info.status = requestInfo.status
        info.updateTime = datetime.datetime.now().time()
        dbsession.commit()
        # dbsession.query(RequestInfo).filter(RequestInfo.urlId == requestInfo.urlId).update({'status':requestInfo.status,'updateTime':datetime.datetime.now().time()})
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
    Base.metadata.drop_all(engine)
    # RequestInfo.__table__.drop(engine)

if __name__=='__main__':
    # drop_db()
    init_db()