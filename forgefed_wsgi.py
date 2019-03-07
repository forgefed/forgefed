# $ sudo pacman -S python-jinja python-pip
# $ pip install activitypub --user
# $ pip install requests-http-signature --user
#import site ; site.addsitedir('~/.local/lib/python3.7/site-packages/')


from activitypub.manager  import Manager
from activitypub.database import ListDatabase


def inbox_get_handler(env):      return [ STATUS_OK , "GET/inbox"      ]
def followers_get_handler(env):  return [ STATUS_OK , "GET/followers"  ]
def following_get_handler(env):  return [ STATUS_OK , "GET/following"  ]
def liked_get_handler(env):      return [ STATUS_OK , "GET/liked"      ]
def likes_get_handler(env):      return [ STATUS_OK , "GET/likes"      ]
def outbox_get_handler(env):     return [ STATUS_OK , "GET/outbox"     ]
def inbox_post_handler(env):     return [ STATUS_OK , "POST/inbox"     ]
def followers_post_handler(env): return [ STATUS_OK , "POST/followers" ]
def following_post_handler(env): return [ STATUS_OK , "POST/following" ]
def liked_post_handler(env):     return [ STATUS_OK , "POST/liked"     ]
def likes_post_handler(env):     return [ STATUS_OK , "POST/likes"     ]
def outbox_post_handler(env):    return [ STATUS_OK , "POST/outbox"    ]
ROUTES = {
  'GET/inbox'      : inbox_get_handler      ,
  'GET/followers'  : followers_get_handler  ,
  'GET/following'  : following_get_handler  ,
  'GET/liked'      : liked_get_handler      ,
  'GET/likes'      : likes_get_handler      ,
  'GET/outbox'     : outbox_get_handler     ,
  'POST/inbox'     : inbox_post_handler     ,
  'POST/followers' : followers_post_handler ,
  'POST/following' : following_post_handler ,
  'POST/liked'     : liked_post_handler     ,
  'POST/likes'     : likes_post_handler     ,
  'POST/outbox'    : outbox_post_handler
}


def application(env , start_response):
  # DEBUG BEGIN
  import json

  #status  = STATUS_OK
  #body    = 'Hello World!'
  #body    = 'Hello World!\n' + str(alice.to_dict())
  #body    = 'Hello World!\n</pre>' + json.dumps(str(alice.to_dict()) , sort_keys=True , indent=2 , separators=(', ', ': ')) + '<pre>'
  #body    = 'Hello World!\n\nalice =>' + str(alice.to_dict()).replace(',' , ',\n\t').replace('{' , '{ ').replace('}' , ' }') + '\n' + \
  #                          '\nenv =>' + str(env            ).replace(',' , ',\n\t').replace('{' , '{ ').replace('}' , ' }')
  # DEBUG END


  path         = env.get('PATH_INFO').replace('/forge-fed/' , '/')
  method       = env.get('REQUEST_METHOD')
  query        = env.get('QUERY_STRING')
  routes_key   = method + path
  route_fn     = ROUTES.get(routes_key)
  is_valid_req = route_fn != None
  resp         = route_fn(env) if is_valid_req else RESP_NOT_FOUND
  status       = resp[0]
  body         = resp[1]
  content_type = 'text/plain'
  content_len  = str(len(body))
  headers      = [ ('Content-type'   , content_type) ,
                   ('Content-Length' , content_len ) ]


  # DEBUG BEGIN
  print('path     = ' + path          + '\n' + \
        'method   = ' + method        + '\n' + \
        'query    = ' + query         + '\n' + \
        'route_fn = ' + str(route_fn) + '\n' + \
        'status   = ' + status        + '\n' + \
        'body     = ' + body          + '\n' )
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
