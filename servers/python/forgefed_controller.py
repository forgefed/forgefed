import json
import requests

from forgefed_constants import AP_POST_HEADERS , HTTP_SIG_AUTH , RESP_NOT_FOUND , STATUS_OK
from forgefed_model     import ApManager , NewNote , GetActivity , GetPerson , \
                               IsValidActivity , IsValidNoteActivity


## request handlers ##

def user_get_handler(person_id , ap_dict):
  #person = GetPerson(person_id)
  person = Alice
  person_json = json.dumps(person.to_dict())


  cprint("user_get_handler() person_id=" + person_id + "\n\tresp=" + person_json , DBG_COLOR_OUTGOING)


  return [ STATUS_OK , person_json ] if person != None else RESP_NOT_FOUND


def inbox_get_handler(person_id , ap_dict):
  SignedPostReq(Bob.inbox , AliceNote.to_dict()) # DEBUG
  return [ STATUS_OK , "GET/inbox"      ]
def followers_get_handler(person_id , ap_dict):  return [ STATUS_OK , "GET/followers"  ]
def following_get_handler(person_id , ap_dict):  return [ STATUS_OK , "GET/following"  ]
def liked_get_handler(person_id , ap_dict):      return [ STATUS_OK , "GET/liked"      ]
def likes_get_handler(person_id , ap_dict):      return [ STATUS_OK , "GET/likes"      ]
def outbox_get_handler(person_id , ap_dict):     return [ STATUS_OK , "GET/outbox"     ]

def inbox_post_handler(person_id , ap_dict):
  ## validate request ##

  person = GetPerson(person_id)

  if person == None: return RESP_NOT_FOUND


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


## outgoing requests ##

def SignedGetReq(url):
  resp = requests.get(url , auth=HTTP_SIG_AUTH)


  # DEBUG BEGIN
  print("SignedGetReq() url=" + url + " resp=" + resp.text , DBG_COLOR_OUTGOING)
  # DEBUG END


def SignedPostReq(url , activity_dict):
  if IsValidActivity(activity_dict):
    post_body = str(activity_dict).encode()
    resp      = requests.post(url , headers=AP_POST_HEADERS , data=post_body , auth=HTTP_SIG_AUTH)

    if resp.status_code == 200: ApManager.on_post_to_box('outbox' , activity_dict)


    # DEBUG BEGIN
    cprint("SignedPostReq() url=" + url + "\n\tpost_body=" + str(post_body) + "\n\tstatus=" + str(resp.status_code) + "\n\tresp=" + resp.text , DBG_COLOR_OUTGOING)
  else: cprint("SignedPostReq() invalid - dropping\n\turl=" + url + "\n\tpost_body=" + str(activity_dict) , DBG_COLOR_OUTGOING)
  # DEBUG END


# WIP BEGIN
#def key_resolver(key_id, algorithm):
  #return public_keys[key_id]

#HTTPSignatureAuth.verify(request, key_resolver=key_resolver)
# WIP END


## event handlers ##

def OnBoxRecv(box , activity_id):
  # NOTE: this fires after message is written to the DB
  print("OnBoxRecv() box=" + box + " activity_id=" + activity_id)

  activity = GetActivity(activity_id)

  if activity != None:
    activity_msg = activity_id + " => " + activity['attributedTo'] + " -> " + activity['to']

    if box == 'inbox'  : print("received activity: " + activity_msg)
    if box == 'outbox' : print("sent activity: "     + activity_msg)


ApManager.set_callback(OnBoxRecv)


print("ready")


# DEBUG BEGIN
from termcolor import cprint
from forgefed_constants import DBG_COLOR_OUTGOING , TEST_REMOTE_ACTOR_ID , TEST_REMOTE_ACTOR_URL , \
                               TEST_REMOTE_INBOX_URL
from forgefed_model import CreatePerson

Alice     = CreatePerson('alice')
Bob       = CreatePerson(TEST_REMOTE_ACTOR_ID , TEST_REMOTE_ACTOR_URL , TEST_REMOTE_INBOX_URL)
AliceNote = NewNote(from_id=Alice.id , to_id=Bob.id , body='Hello Note')

print("Alice="     + str(Alice    ) + " => " + str(GetPerson  (Alice    .preferredUsername)))
#print("Bob="       + str(Bob      ) + " => " + str(GetPerson  (Bob      .preferredUsername)))
#print("AliceNote=" + str(AliceNote) + " => " + str(GetActivity(AliceNote.id)))
#from forgefed_model import Db ; from pprint import pprint ; print("Db=") ; pprint(vars(Db))

#SignedGetReq(TEST_REMOTE_ACTOR_URL)
#SignedPostReq(Bob.inbox , {"k1":"v1"})
#SignedPostReq(Bob.inbox , AliceNote.to_dict())
# DEBUG END
