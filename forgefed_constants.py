from requests_http_signature import HTTPSignatureHeaderAuth


PROTOCOL     = 'https'
HOSTNAME     = 'example.net'
TCP_PORT     = 8888
LOCAL_CONFIG =                                               \
{                                                            \
  "$SCHEME"           : PROTOCOL                           , \
  "$HOST"             : HOSTNAME                           , \
  "$PORT"             : TCP_PORT                           , \

  "Person.id"         : "$id@$HOST"                        , \
  "Person.likes"      : "$id/likes"                        , \
  "Person.following"  : "$id/following"                    , \
  "Person.followers"  : "$id/followers"                    , \
  "Person.liked"      : "$id/liked"                        , \
  "Person.inbox"      : "$id/inbox"                        , \
  "Person.outbox"     : "$id/outbox"                       , \
  "Person.url"        : "$DOMAIN/$id"                      , \

  "Note.id"           : "$temp_uuid"                       , \
  'Note.attributedTo' : "$from_id"                         , \
  'Note.content'      : "<p>$source.content</p>"           , \
  'Note.published'    : "$NOW"                             , \
  'Note.url'          : "$DOMAIN/$from_id/note/$temp_uuid"
}

#TEST_REMOTE_ACTOR_URL = 'https://forge.angeley.es/' # vervis
TEST_REMOTE_INBOX_URL = 'https://forge.angeley.es/inbox' # vervis
HTTP_SIG_PUB_KEY_FILE = 'public.pem'
HTTP_SIG_PVT_KEY_FILE = 'private.pem'
with open(HTTP_SIG_PUB_KEY_FILE , 'rb') as public_key_file:
  PUBLIC_KEY          = public_key_file .read()
with open(HTTP_SIG_PVT_KEY_FILE , 'rb') as private_key_file:
  PRIVATE_KEY         = private_key_file.read()
AP_POST_HEADERS       = { 'Content-Type'      : 'application/activity+json'                  ,
                          'Accept'            : 'application/json'                           ,
                          'ActivityPub-Actor' : PROTOCOL + '://' + HOSTNAME + '/dummy-actor' } # vervis extension
AP_SIGN_HEADERS       = [ '(request-target)' , 'host' , 'date' , 'ActivityPub-Actor' ] # vervis extension (ActivityPub-Actor)
AP_SIGN_ALGORITHM     = 'rsa-sha256'
HTTP_SIG_KEY_ID       = HOSTNAME
KEYFILE_PUB_HEADER    = b'-----BEGIN PUBLIC KEY-----\n'
KEYFILE_PUB_FOOTER    = b'-----END PUBLIC KEY-----\n'
KEYFILE_PVT_HEADER    = b'-----BEGIN RSA PRIVATE KEY-----\n'
KEYFILE_PVT_FOOTER    = b'-----END RSA PRIVATE KEY-----\n'
HTTP_SIG_AUTH         = HTTPSignatureHeaderAuth(headers=AP_SIGN_HEADERS , algorithm=AP_SIGN_ALGORITHM , \
                                                key_id=HTTP_SIG_KEY_ID  , key=PRIVATE_KEY             )

PATH_REGEX = r'^/forge-fed/'
AP_NS_URL  = 'https://www.w3.org/ns/activitystreams'

STATUS_OK             = '200 OK'
STATUS_NOT_FOUND      = '404 NOT FOUND'
RESP_NOT_FOUND        = [ STATUS_NOT_FOUND , '{ "message" : "resource not found" }'            ]
RESP_INVALID_JSON     = [ STATUS_OK        , '{ "message" : "invalid JSON struct" }'           ]
RESP_INVALID_ACTIVITY = [ STATUS_OK        , '{ "message" : "invalid activity-pub activity" }' ]


# DEBUG BEGIN
#from pprint import pprint ; print("HTTP_SIG_AUTH=") ; pprint(vars(HTTP_SIG_AUTH))
# DEBUG END


## validations/sanity/env check ##

if PUBLIC_KEY[0:27] != KEYFILE_PUB_HEADER or \
   PUBLIC_KEY[-25:] != KEYFILE_PUB_FOOTER or \
   len(PUBLIC_KEY)  != 451               :
  raise ValueError("invalid keyfile: '" + HTTP_SIG_PUB_KEY_FILE + "'")

if PRIVATE_KEY[0:32] != KEYFILE_PVT_HEADER or \
   PRIVATE_KEY[-30:] != KEYFILE_PVT_FOOTER or \
   len(PRIVATE_KEY)  != 1675              :
  raise ValueError("invalid keyfile: '" + HTTP_SIG_PVT_KEY_FILE + "'")
