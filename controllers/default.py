# -*- coding: utf-8 -*-

def index():
    form = crud.create(db.chestionar, message='Chestionar creat!')
    return dict(form=form, chestionare=db(db.chestionar.activ==True).select())

@auth.requires_membership('editor')
def intrebari():
    chest = 1
    if len(request.args) > 0:
        chest = request.args[0]
    intrebari = db(db.intrebare.chestionar==chest)
    db.intrebare.pos.default = intrebari.count() + 1
    db.intrebare.chestionar.default = chest
    form = FORM(TEXTAREA(_name='text'), INPUT(_type='submit'))
    if form.accepts(request.vars, session):
        pos = 1
        text = form.vars['text']
        for line in text.split('\n'):
            if line[0].isdigit():
                pos, continut = line.split('.', 1)
            else:
                continut = line
            db.intrebare.insert(pos=pos, continut=continut.strip())
            pos = int(pos) + 1            
    return dict(form=form, intrebari=intrebari.select(orderby=db.intrebare.pos))

@auth.requires_login()
def intrebare():
    curent = 1
    if len(request.args) > 1:
        chest = request.args[0]
        curent = int(request.args[1])
    intr = db.intrebare(chestionar=chest, pos=curent)
    count = db(db.intrebare.chestionar==chest).count()
    if count == 0:
        return redirect(URL('intrebari', args=chest))
    form = FORM(SELECT(
                OPTION('Niciodata', _value='0'),
                OPTION('Uneori', _value='1'),
                OPTION('De cele mai multe ori', _value='2'),
                OPTION('Intodeauna', _value='3'),
                _name='raspuns'), INPUT(_value='Urmatoarea',_type='submit'), _id="evaluare")
    if form.accepts(request.vars, session):
        r = db((db.raspuns.chestionar==intr.chestionar) &
               (db.raspuns.user==auth.user_id)).select().first()
        if not r:
            id = db.raspuns.insert(chestionar=intr.chestionar, lista = [0]*count)
            r = db.raspuns(id)
        lista = r.lista
        lista[curent-1] = form.vars['raspuns']
        r.update_record(lista=lista)
        if curent < count:
            redirect(URL('intrebare', args=(chest, curent+1)))
        else:
            redirect(URL('rezultat', args=chest))
    elif form.errors:
        response.flash = 'Nu ati introdu o valuare corecta... Oaaa cum se poate?'
    return dict(form=form, intrebare=intr, count=count)

@auth.requires_login()
def rezultat():
    return dict()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()
