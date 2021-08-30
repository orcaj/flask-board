from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo2.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\xba\x11\xed\x1d\xdc\x98\xee[\xffu\xfe\xadz\x99\xde\x0e'
