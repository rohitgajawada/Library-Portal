response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
                  _class="navbar-brand",_href="http://www.web2py.com/",
                  _id="web2py-logo")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'
response.google_analytics_id = None
response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

DEVELOPMENT_MENU = True

def _():
    app = request.application
    ctr = request.controller
    response.menu += [
        (T('Register'), False, URL('libreg')),
        (T('Search'), False, URL('borrow')),
        (T('Status'), False, URL('status')),
        (T('E-books'), False, URL('ebooks')),
        (T('My Sites'), False, URL('admin', 'default', 'site'))
    ]

if auth.user!=None and auth.user.is_admin==True:
    response.menu += [(T('libadmin'), False, URL('libadmin'))]

if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu()
