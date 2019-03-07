# $ sudo pacman -S python-jinja python-pip
# $ pip install activitypub --user
#import site ; site.addsitedir('~/.local/lib/python3.7/site-packages/')


from activitypub.manager  import Manager
from activitypub.database import ListDatabase


def inbox_handler(env):     return [ '200 OK' , "inbox"     ]
def followers_handler(env): return [ '200 OK' , "followers" ]
def following_handler(env): return [ '200 OK' , "following" ]
def liked_handler(env):     return [ '200 OK' , "liked"     ]
def likes_handler(env):     return [ '200 OK' , "likes"     ]
def outbox_handler(env):    return [ '200 OK' , "outbox"    ]
ROUTES = {
  '/inbox'     : inbox_handler     ,
  '/followers' : followers_handler ,
  '/following' : following_handler ,
  '/liked'     : liked_handler     ,
  '/likes'     : likes_handler     ,
  '/outbox'    : outbox_handler
}


def application(env , start_response):
  # DEBUG BEGIN
  #status  = '200 OK'
  #body    = 'Hello World!'
  #body    = 'Hello World!\n' + str(alice.to_dict())
  #body    = 'Hello World!\n</pre>' + json.dumps(str(alice.to_dict()) , sort_keys=True , indent=2 , separators=(', ', ': ')) + '<pre>'
  #body    = 'Hello World!\n\nalice =>' + str(alice.to_dict()).replace(',' , ',\n\t').replace('{' , '{ ').replace('}' , ' }') + '\n' + \
  #                          '\nenv =>' + str(env            ).replace(',' , ',\n\t').replace('{' , '{ ').replace('}' , ' }')
  # DEBUG END


  path         = env.get('PATH_INFO').replace('/forge-fed/' , '/')
  method       = env.get('REQUEST_METHOD')
  query        = env.get('QUERY_STRING')
  route_fn     = ROUTES.get(path)
  is_valid_req = route_fn != None
  resp         = route_fn(env) if is_valid_req else [ '404 NOT FOUND' , '_4_0_4_' ]
  status       = resp[0]
  body         = resp[1]
  content_type = 'text/plain'
  content_len  = str(len(body))
  headers      = [ ('Content-type'   , content_type) ,
                   ('Content-Length' , content_len ) ]


  # DEBUG BEGIN
  print('path   = ' + path   + '\n' + \
        'method = ' + method + '\n' + \
        'query  = ' + query  + '\n' + \
        'status = ' + status + '\n' + \
        'body   = ' + body   + '\n' )
  # DEBUG END


  start_response(status , headers)

  return [ body.encode('utf8') ]


## main entry ##

Db        = ListDatabase()
ApManager = Manager(database=Db)
Alice     = ApManager.Person(id="alice")
AliceNote = ApManager.Note(**{ 'sensitive'   : False                                              , \
                               'attributedTo': 'http://localhost:5000'                            , \
                               'cc'          : [ 'http://localhost:5005/followers' ]              , \
                               'to'          : [ 'https://www.w3.org/ns/activitystreams#Public']  , \
                               'content'     : '<p>$source.content</p>'                           , \
                               'tag'         : []                                                 , \
                               'source'      : { 'mediaType' : 'text/markdown' ,                    \
                                                 'content'   : '$temp_text'    }                  , \
                               'published'   : '$NOW'                                             , \
                               'temp_uuid'   : "$UUID"                                            , \
                               'temp_text'   : 'Hello'                                            , \
                               'id'          : 'http://localhost:5005/outbox/$temp_uuid/activity' , \
                               'url'         : 'http://localhost:5005/note/$temp_uuid'            } )

Db.actors.insert_one(Alice.to_dict())


# DEBUG BEGIN
print("init Alice=" + str(Alice) + " => " + str(Db.actors.find_one({ 'id' : 'http://localhost:5000/alice' })))
# DEBUG END
