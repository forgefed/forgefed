import requests

from forgefed_constants import AP_POST_HEADERS , HTTP_SIG_AUTH , RESP_NOT_FOUND , STATUS_OK
from forgefed_model     import ApManager , CreateNote , GetPerson , IsValidActivity , IsValidNoteActivity


def user_get_handler(person_id , ap_dict):
  person = GetPerson(person_id)

  return [ STATUS_OK , json.dumps(person['ap-dict']) ] if person != None else RESP_NOT_FOUND


def inbox_get_handler(person_id , ap_dict):      return [ STATUS_OK , "GET/inbox"      ]
def followers_get_handler(person_id , ap_dict):  return [ STATUS_OK , "GET/followers"  ]
def following_get_handler(person_id , ap_dict):  return [ STATUS_OK , "GET/following"  ]
def liked_get_handler(person_id , ap_dict):      return [ STATUS_OK , "GET/liked"      ]
def likes_get_handler(person_id , ap_dict):      return [ STATUS_OK , "GET/likes"      ]
def outbox_get_handler(person_id , ap_dict):     return [ STATUS_OK , "GET/outbox"     ]

def inbox_post_handler(person_id , ap_dict):
  ## validate request ##

  person = GetPerson(person_id)

  if person == None:
    return RESP_NOT_FOUND


  ## handle request ##

  to_person_id   = ap_dict['to'          ][0]
  from_person_id = ap_dict['attributedTo']
  note_body      = ap_dict['content'     ]


  # DEBUG BEGIN
  #print("inbox_post_handler() IsValidNoteActivity="       + str(IsValidNoteActivity(ap_dict)) + \
                            #" to_person_id == person_id=" + str(to_person_id == person_id))
  # DEBUG END


  if IsValidNoteActivity(ap_dict) and to_person_id == person_id:
    incoming_note = CreateNote(from_id=from_person_id , to_id=person_id , body=note_body)

    ApManager.on_post_to_box('inbox' , incoming_note)

    return [ STATUS_OK , "POST/inbox" ]
  else:
    return [ STATUS_OK , 'POST/UNHANDLED_ACTIVITY_TYPE' ]

def followers_post_handler(person_id , ap_dict): return [ STATUS_OK , "POST/followers" ]
def following_post_handler(person_id , ap_dict): return [ STATUS_OK , "POST/following" ]
def liked_post_handler(person_id , ap_dict):     return [ STATUS_OK , "POST/liked"     ]
def likes_post_handler(person_id , ap_dict):     return [ STATUS_OK , "POST/likes"     ]
def outbox_post_handler(person_id , ap_dict):    return [ STATUS_OK , "POST/outbox"    ]


def SignedGetReq(url):
  resp = requests.get(url , auth=HTTP_SIG_AUTH)


  # DEBUG BEGIN
  print("SignedGetReq() url=" + url + " resp=" + resp.text)
  # DEBUG END


def SignedPostReq(url , a_dict):
  post_body = str(a_dict).encode()
  resp      = requests.post(url , headers=AP_POST_HEADERS , data=post_body , auth=HTTP_SIG_AUTH)


  # DEBUG BEGIN
  print("SignedPostReq() url=" + url + "\n\tpost_body=" + str(post_body) + "\n\tresp=" + resp.text)
  # DEBUG END


# WIP BEGIN
#def key_resolver(key_id, algorithm):
  #return public_keys[key_id]

#HTTPSignatureAuth.verify(request, key_resolver=key_resolver)
# WIP END


print("ready")


# DEBUG BEGIN
from forgefed_model import CreatePerson

Alice     = CreatePerson(person_id='alice')
Bob       = CreatePerson(person_id='bob')
AliceNote = CreateNote(from_id=Alice.id , to_id=Bob.id , body='Hello Note')

#from forgefed_model import GetActivity
#print("Alice="     + str(Alice    ) + " => " + str(GetPerson  (Alice    .id)))
#print("Bob="       + str(Bob      ) + " => " + str(GetPerson  (Bob      .id)))
#print("AliceNote=" + str(AliceNote) + " => " + str(GetActivity(AliceNote.id)))
#from forgefed_model import Db ; from pprint import pprint ; print("Db=") ; pprint(vars(Db))

from forgefed_constants import TEST_REMOTE_INBOX_URL
from forgefed_model import GetActivity
#SignedGetReq(TEST_REMOTE_ACTOR_URL)
#SignedPostReq(TEST_REMOTE_INBOX_URL , {"k1":"v1"})
SignedPostReq(TEST_REMOTE_INBOX_URL , GetActivity(AliceNote.id))
# DEBUG END
