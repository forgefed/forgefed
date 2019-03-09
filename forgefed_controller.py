from forgefed_constants import RESP_NOT_FOUND , STATUS_OK
from forgefed_model     import ApManager , GetPerson , IsValidActivity , IsValidNoteActivity


def user_get_handler(person_id , ap_dict):
  person = GetPerson(person_id)

  return [ STATUS_OK , "this is " + person_id ] if person != None else RESP_NOT_FOUND


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


print("ready")


# DEBUG BEGIN
from forgefed_model import CreateNote , CreatePerson

Alice     = CreatePerson(person_id='alice')
Bob       = CreatePerson(person_id='bob')
AliceNote = CreateNote(from_id=Alice.id , to_id=Bob.id , body='Hello Note')

#from forgefed_model import GetActivity
#print("Alice="     + str(Alice    ) + " => " + str(GetPerson  (Alice    .id)))
#print("Bob="       + str(Bob      ) + " => " + str(GetPerson  (Bob      .id)))
#print("AliceNote=" + str(AliceNote) + " => " + str(GetActivity(AliceNote.id)))
#from forgefed_model import Db ; from pprint import pprint ; print("Db=") ; pprint(vars(Db))
# DEBUG END
