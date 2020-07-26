from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

_mysql_engine = None

_mysql_session = None


def get_db_url(db_name):
    return "mysql+pymysql://wzy:123@192.168.50.100/" + db_name + "?charset=utf8"


def get_db_engine_by_name(db_name, echo=True):
    url = get_db_url(db_name)
    global _mysql_engine
    if not _mysql_engine:
        _mysql_engine = create_engine(url, echo=echo)

    if not database_exists(url):
        create_database(url)

    # 非常寸、带横杠的数据库名，要用反引号 引上才可以用， 否则sql报错
    use_db_dialect = 'USE ' + "`" + db_name + "`"
    _mysql_engine.execute(use_db_dialect)

    return _mysql_engine



def get_db_session_by_name(db_name):
    global _mysql_session

    if _mysql_session is None:
        get_db_engine_by_name(db_name)
        session_cls = sessionmaker(bind=_mysql_engine)
        _mysql_session = session_cls()

    return _mysql_session
