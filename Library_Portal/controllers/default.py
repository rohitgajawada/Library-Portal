import datetime
@auth.requires_login()
def index():
    thedate=datetime.date.today()
    page=0
    items_per_page=10
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    rows=db(db.book).select(db.book.ALL, orderby=db.book.dateadded, limitby=limitby)
    pops=db(db.book).select(db.book.ALL, orderby=db.book.rating, limitby=limitby)
    wishes=db(db.wish.bookuser == auth.user.id).select(db.wish.ALL, orderby=db.wish.id)
    return locals()

def manage():
    grid=SQLFORM.grid(db.auth_user)
    return locals()

def user():
    return dict(form=auth())

def libreg():
    return dict(form=auth.register())

@auth.requires(auth.user!=None and auth.user.is_admin==True)
def libadmin():
    if auth.user!=None and auth.user.is_admin==True:
        grid = SQLFORM.grid(db.book)
        return dict(grid=grid)
    else:
        return dict()

def mycheck():
    abook = db.book(request.vars.check)
    number = db((db.records.bookuser ==  auth.user.id) & (db.records.ifret == False)).count()
    if number>=3:
        response.flash='You cannot borrow any more books so you will have to return a book'
    else:
        num = abook.numcopy - abook.numref
        if num <= abook.numborrow:
            response.flash='No more books available!'
            return str("Ran out of copies")
        else:
            return str(num)+" books available" 

def wishlist():
    mywish = db.book(request.vars.love)
    nwish = db((db.wish.bookuser == auth.user.id) & (db.wish.bookid == mywish.id)).count()
    if nwish != 1:
        db.wish.insert(bookid = mywish.id, bookuser=auth.user.id)
    return str("Added to wishlist") 

def status():
    if auth.user == None:
        rows=[]
        return dict()
    if len(request.args): 
        page=int(request.args[0])
    else: 
        page=0
    items_per_page=10
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    rows=db(db.records.bookuser == auth.user.id).select(db.records.ALL, orderby=db.records.date_borrow, limitby=limitby)
    return locals()

def borrow():
    form1=FORM(INPUT(_id='keyword1', _name='keyword1', _onkeyup='ajax("callback1", ["keyword1"], "target1");')) 
    target_div1=DIV(_id='target1')

    form2=FORM(INPUT(_id='keyword2', _name='keyword2', _onkeyup="ajax('callback2', ['keyword2'], 'target2');")) 
    target_div2=DIV(_id='target2')

    form3=FORM(INPUT(_id='keyword3', _name='keyword3', _onkeyup="ajax('callback3', ['keyword3'], 'target3');")) 
    target_div3=DIV(_id='target3')

    return locals()

def borrows():
    form=FORM(INPUT(_id='keyword', _name='keyword', _onkeyup="ajax('callback', ['keyword'], 'target');")) 
    target_div=DIV(_id='target')
    return locals()

def callback():
    query = db.auth_user.email.contains(request.vars.keyword)
    mems = db(query).select(orderby=db.auth_user.email)
    links = [A(str(mem.email)+" - "+str(mem.first_name)+" "+str(mem.last_name), _href=URL('selectborrow',args=mem.id)) for mem in mems]
    return UL(*links)

def selectborrow():
    member = db.auth_user(request.args(0,cast=int)) or redirect(URL('index'))
    myid = member.id
    
    form1=FORM(INPUT(_id='key1', _name='key1', _onkeyup="ajax('http://127.0.0.1:8000/Library_Portal/default/call1', ['key1'], 'target1')")) 
    target_div1=DIV(_id='target1')

    
    return locals()

def call1():
    query = db.book.title.contains(request.vars.key1)
    books = db(query).select(orderby=db.book.title)
    links = [A(b.title, _href=URL('show',args=b.id)) for b in books]
    return UL(*links)

def mylike():
    rec = db.recipe(request.vars.hi)
    mrec = db((db.mlike.aliker == auth.user.id) & (db.mlike.recid == rec.id)).count()
    if mrec != 1:
        db.mlike.insert(recid = rec.id, aliker=auth.user.id)
        newlikes = rec.likes + 1
        rec.update_record(likes=newlikes)
    else:
        newlikes = rec.likes

    return str(newlikes) 

def callback1():
    query = db.book.title.contains(request.vars.keyword1)
    books = db(query).select(orderby=db.book.title)
    links = [A(b.title, _href=URL('show',args=b.id)) for b in books]
    return UL(*links)

def callback2():
    query = db.book.author.contains(request.vars.keyword2)
    books = db(query).select(orderby=db.book.author)
    links = [A(b.author, _href=URL('show',args=b.id)) for b in books]
    return UL(*links)

def callback3():
    query = db.book.genre.contains(request.vars.keyword3)
    books = db(query).select(orderby=db.book.genre)
    links = [A(b.genre, _href=URL('show',args=b.id)) for b in books]
    return UL(*links)

def show():

    form=FORM('Rating:  ',
              INPUT(_type='radio', _name='test', _value="1", value='b'),
              INPUT(_type='radio', _name='test', _value="2", value='b'),
              INPUT(_type='radio', _name='test', _value="3", value='b'),
              INPUT(_type='radio', _name='test', _value="4", value='b'),
              INPUT(_type='radio', _name='test', _value="5", value='b'),
              INPUT(_id="rate", _type='submit'))

    mybook = db.book(request.args(0,cast=int)) or redirect(URL('index'))

    if form.process().accepted:
        number = db((db.records.bookuser ==  auth.user.id) & (db.records.bookid == mybook.id )).count()
        if number:
            sum = mybook.sumrating
            num = mybook.numrating
            sum = sum + int(form.vars["test"])
            num = num + 1
            newrating = sum/num
            mybook.update_record(rating = newrating, sumrating = sum, numrating = num)

    return dict(mybook=mybook, form=form)

def ebooks():
    if len(request.args): 
        page=int(request.args[0])
    else: 
        page=0
    items_per_page=10
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    rows=db(db.book.ifebook==1).select(db.book.ALL, orderby=db.book.title, limitby=limitby)
    return locals()

@cache.action()
def download():
    return response.download(request, db)

def call():
    return service()

def download_pdf():
    filename=request.args[0]
    path=os.path.join(request.folder,'uploads', filename)
    response.headers['ContentType'] ="application/pdf"
    response.headers['Content-Disposition']="inline; " + filename
    return response.stream(open(filename), chunk_size=65536)
