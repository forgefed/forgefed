LOCAL_CONFIG =                                               \
{                                                            \
  "$SCHEME"           : "https"                            , \
  "$HOST"             : "example.net"                      , \

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

PATH_REGEX = r'^/forge-fed/'

STATUS_OK        = '200 OK'
STATUS_NOT_FOUND = '404 NOT FOUND'
RESP_NOT_FOUND   = [ STATUS_NOT_FOUND , '_4_0_4_' ]
