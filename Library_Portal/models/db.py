from gluon.contrib.appconfig import AppConfig
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    db = DAL('google:datastore+ndb')
    session.connect(request, response, db=db)
    response.generic_patterns = ['*'] if request.is_local else []

response.formstyle = myconf.take('forms.formstyle')
response.form_label_separator = myconf.take('forms.separator')

from gluon.tools import Auth, Service, PluginManager
import datetime

auth = Auth(db)
service = Service()
plugins = PluginManager()
auth.settings.extra_fields['auth_user']= [
    Field('is_admin','boolean', default=0, writable=False, readable=False),
    Field('rollnumber','integer'),
    Field('address','string'),
    Field('phonenumber','string'),
    Field('fine','integer',default=0)]
auth.define_tables(username=False, signature=False)
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

def check_initialize():
    if not db().select(db.auth_user.ALL):        
        db.auth_user.insert(
            password = db.auth_user.password.validate('admin1234')[0],
            email = 'admin@iiit.com',
            first_name = 'Library',
            last_name = 'Administrator',
            is_admin = True,
        )

check_initialize()

db.define_table('book',
                Field('title','string',unique=True),
                Field('author','string'),
                Field('edition','string'),
                Field('publisher','string'),
                Field('rating', 'double', default=0, writable=False),
                Field('sumrating', 'double', default=0, writable=False),
                Field('numrating', 'double', default=0, writable=False),
                Field('genre','string'),
                Field('cover','upload'),
                Field('dateadded','datetime', default=datetime.datetime.today()),
                Field('ifebook','integer', default=0),
                Field('ebook','upload'),
                Field('numref','integer', default=0),
                Field('numborrow','integer', default=0),
                Field('numcopy','integer', default=1),
                format='%(title)s')

db.define_table('records',
                Field('bookid','reference book'),
                Field('bookuser','reference auth_user', default=auth.user_id),
                Field('date_borrow','datetime', default=datetime.datetime.today()),
                Field('date_return','datetime'),
                Field('ifret','boolean', default=False))

db.define_table('wish',
                 Field('bookid','reference book'),
                 Field('bookuser','reference auth_user', default=auth.user_id))

db.book.dateadded.readable=db.book.dateadded.writable=False
