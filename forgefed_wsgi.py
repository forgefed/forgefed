# $ sudo pacman -S python-jinja python-pip
# $ pip install activitypub --user
# $ pip install requests-http-signature --user
#import site ; site.addsitedir('~/.local/lib/python3.7/site-packages/')


import re

from forgefed_constants  import PATH_REGEX , RESP_NOT_FOUND
from forgefed_controller import *
from forgefed_model      import GetPerson


ROUTES =                                      \
{                                             \
  'GET-'           : user_get_handler       , \
  'GET-inbox'      : inbox_get_handler      , \
  'GET-followers'  : followers_get_handler  , \
  'GET-following'  : following_get_handler  , \
  'GET-liked'      : liked_get_handler      , \
  'GET-likes'      : likes_get_handler      , \
  'GET-outbox'     : outbox_get_handler     , \
  'POST-inbox'     : inbox_post_handler     , \
  'POST-followers' : followers_post_handler , \
  'POST-following' : following_post_handler , \
  'POST-liked'     : liked_post_handler     , \
  'POST-likes'     : likes_post_handler     , \
  'POST-outbox'    : outbox_post_handler
}


def application(env , start_response):
  # DEBUG BEGIN
  import datetime ; print("\nnew request " + str(datetime.datetime.now()))

  #status  = STATUS_OK
  #body    = 'Hello World!'
  #body    = 'env =>' + str(env).replace(',' , ',\n\t').replace('{' , '{ ').replace('}' , ' }')
  # DEBUG END


  full_path    = env.get('PATH_INFO')
  method       = env.get('REQUEST_METHOD')
  query        = env.get('QUERY_STRING')
  path         = re.sub(PATH_REGEX , '/' , full_path).split('/')
  person_id    = path[1] if len(path) >= 2 else ''
  channel      = path[2] if len(path) >= 3 else ''
  person       = GetPerson(person_id)
  routes_key   = method + '-' + channel if person != None else ''
  route_fn     = ROUTES.get(routes_key)
  is_valid_req = route_fn != None
  resp         = route_fn(person_id , query) if is_valid_req else RESP_NOT_FOUND
  status       = resp[0]
  body         = resp[1]
  content_type = 'text/plain'
  content_len  = str(len(body))
  headers      = [ ('Content-type'   , content_type) ,
                   ('Content-Length' , content_len ) ]


  # DEBUG BEGIN
  DbgTraceResp(status , body)
  # DEBUG END


  ## respond ##

  start_response(status , headers)

  return [ body.encode('utf8') ]


# DEBUG BEGIN
import json

def DbgTraceReq(full_path , path , person_id , channel , method , req_body , ap_dict , routes_key , route_fn):
  print("full_path  = " + full_path     )
  print("path       = " + '/'.join(path))
  print("person_id  = " + person_id     )
  print("channel    = " + channel       )
  print("method     = " + method        )
  print("req_body   = " + req_body      )
  print("ap_dict    = " + json.dumps(ap_dict , sort_keys=True , indent=2))
  print("routes_key = " + routes_key    )
  print("route_fn   = " + str(route_fn) )

def DbgTraceResp(status , body):
  print("status     = " + status        )
  print("body       = " + body          )

# DEBUG END
