# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
    return dict(chestionare=db(db.chestionar.activ==True).select())

@auth.requires_login()
def intrebare():
    curent = 1
    if len(request.args) > 1:
        chest = request.args[0]
        curent = int(request.args[1])
    intr = db.intrebare(chestionar=chest, id=curent)
    count = db(db.intrebare.chestionar==chest).count()
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
