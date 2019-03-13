# $ sudo pacman -S python-cryptography python-jinja python-pip python-requests
# $ pip install activitypub --user
# $ pip install requests-http-signature --user
#import site ; site.addsitedir('~/.local/lib/python3.7/site-packages/')


import json
import re

from forgefed_constants  import PATH_REGEX , RESP_INVALID_ACTIVITY , RESP_NOT_FOUND
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
  import datetime ; cprint("\nnew request " + str(datetime.datetime.now()) , DBG_COLOR_INCOMING)

  #status  = STATUS_OK
  #body    = 'Hello World!'
  #body    = 'env =>' + str(env).replace(',' , ',\n\t').replace('{' , '{ ').replace('}' , ' }')
  # DEBUG END


  ## parse request ##

  full_path = env.get('PATH_INFO'     )
  method    = env.get('REQUEST_METHOD')

  if   method == 'GET' : ap_dict = ''
  elif method == 'POST':
    try:
      req_body_len = int(env.get('CONTENT_LENGTH' , 0))
      req_body     = env['wsgi.input'].read(req_body_len).decode('utf8')
      ap_dict      = json.loads(req_body)
    except (ValueError):
      method   = 'INVALID_JSON_POST' # invalidate the request route
      req_body = None
      ap_dict  = None

  path             = re.sub(PATH_REGEX , '/' , full_path).split('/')
  person_id        = path[1] if len(path) >= 2 else ''
  channel          = path[2] if len(path) >= 3 else ''
  person           = GetPerson(person_id)
  routes_key       = method + '-' + channel if person != None else ''
  route_fn         = ROUTES.get(routes_key)
  is_valid_req     = route_fn != None
  is_valid_payload = method != 'POST' or IsValidActivity(ap_dict)


  # DEBUG BEGIN
  if method != 'POST': req_body = ''
  DbgTraceReq(full_path , path , person_id , channel , method , req_body , ap_dict , routes_key , route_fn)
  # DEBUG END


  ## handle request ##

  resp         = route_fn(person_id , ap_dict) if is_valid_req and is_valid_payload else \
                 RESP_INVALID_ACTIVITY         if is_valid_req                      else \
                 RESP_NOT_FOUND
  status       = resp[0] if len(resp) == 2 else '442 BORKED'
  body         = resp[1] if len(resp) == 2 else 'INVALID_RESP'
  content_type = 'application/ld+json; profile="https://www.w3.org/ns/activitystreams"'       if routes_key == 'GET-'       else 'text/plain'
  #content_type = 'application/ld+json'       if routes_key == 'GET-'       else              \
                 #'application/activity+json' if routes_key == 'GET-inbox' or                 \
                                                #routes_key == 'GET-outbox' else 'text/plain'
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
from termcolor import cprint
from forgefed_constants import DBG_COLOR_INCOMING
def DbgTraceReq(full_path , path , person_id , channel , method , req_body , ap_dict , routes_key , route_fn):
  apdict = json.dumps(ap_dict , sort_keys=True , indent=2)

  cprint("full_path  = " + full_path      , DBG_COLOR_INCOMING)
  cprint("path       = " + '/'.join(path) , DBG_COLOR_INCOMING)
  cprint("person_id  = " + person_id      , DBG_COLOR_INCOMING)
  cprint("channel    = " + channel        , DBG_COLOR_INCOMING)
  cprint("method     = " + method         , DBG_COLOR_INCOMING)
  cprint("req_body   = " + req_body       , DBG_COLOR_INCOMING)
  cprint("ap_dict    = " + apdict         , DBG_COLOR_INCOMING)
  cprint("routes_key = " + routes_key     , DBG_COLOR_INCOMING)
  cprint("route_fn   = " + str(route_fn)  , DBG_COLOR_INCOMING)

def DbgTraceResp(status , body):
  cprint("status     = " + status         , DBG_COLOR_INCOMING)
  cprint("body       = " + body           , DBG_COLOR_INCOMING)

# DEBUG END
