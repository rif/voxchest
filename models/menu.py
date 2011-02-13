# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = T('Chestionare Vox')
response.subtitle = T('Chestionare biserica Vox Domini Timisoara')

#http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Radu Ioan Fericean'
response.meta.description = 'Aplicatie de creat chestionare'
response.meta.keywords = 'chestionare, vox, vox domini, timisoara'
response.meta.generator = 'Web2py Enterprise Framework'
response.meta.copyright = 'Copyright 2011'


##########################################
## this is the main application menu
## add/remove items as required
##########################################

response.menu = [
    (T('Home'), False, URL(request.application,'default','index'), [])
    ]
