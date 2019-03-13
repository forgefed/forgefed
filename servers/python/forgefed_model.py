import re
from activitypub.database import ListDatabase
from activitypub.manager  import Manager

from forgefed_constants import AP_NS_URL , HOSTNAME , FOREIGN_ID_REGEX , LOCAL_CONFIG , \
                               LOCAL_ID_REGEX , PROTOCOL , PUBLIC_KEY


## getters/setters ##

def CreatePerson(person_id , actor_url='' , inbox_url=''):
  if   actor_url == '' and inbox_url == '':      # local actor
    person_id     = re.sub(LOCAL_ID_REGEX , '' , person_id) + '@' + HOSTNAME
    person_params = { 'id' : person_id }
  elif actor_url != '' and inbox_url != '' and \
       re.search(FOREIGN_ID_REGEX , person_id) : # foreign actor
    person_params = { 'id' : person_id , 'actor' : actor_url , 'inbox' : inbox_url }
  else: raise ValueError("invalid person params: '" + "','".join([person_id , actor_url , inbox_url]) + "'")

  person = GetPerson(person_id)

  if person == None:
    # TODO: publicKey and preferredUsername belong in the activitypub library
    person                   = ApManager.Person(**person_params)
    person.preferredUsername = person_id
    person.publicKey         =           \
    {                                    \
      "id"           : person.url      , \
      "owner"        : person.url      , \
      "publicKeyPem" : str(PUBLIC_KEY)   \
    }

    #print("person.publicKey=" + str(person.publicKey))

    Db.actors.insert_one(person.to_dict())

    if GetPerson(person_id) != None: print("created Person(" + person.id + ")")

    db_person = GetPerson(person_id)
    print("person.publicKey=" + str(person.publicKey))
    print("db_person.publicKey=" + db_person['publicKey'])

  return person


def NewNote(from_id , to_id , body , media_type='text/plain'):
  note_params =                                  \
  {                                              \
    'from_id'   : from_id                      , \
    'to'        : [ to_id ]                    , \
    'cc'        : [ from_id + "/followers" ]   , \
    'tag'       : []                           , \
    'source'    : { 'mediaType' : media_type ,   \
                    'content'   : body       } , \
    'sensitive' : False                        , \
    'temp_uuid' : "$UUID"                      , \
    'temp_text' : body                           \
  }
  note = ApManager.Note(**note_params)

  print("created Note(" + note.id + ") " + from_id + " -> " + to_id)

  return note


def GetPerson(person_id):
  person_id = PROTOCOL + '://' + HOSTNAME + '/' + person_id

  return Db.actors.find_one({'id' : person_id})


def GetActivity(activity_id):
  return Db.activities.find_one({'id' : activity_id})


## validations ##

def IsValidNoteActivity(ap_dict):
  # DEBUG BEGIN
  #DbgTraceIsValidActivity(ap_dict)
  # DEBUG END


  return '@context'     in ap_dict and ap_dict['@context'] == AP_NS_URL and \
         'attributedTo' in ap_dict                                      and \
         'cc'           in ap_dict                                      and \
         'content'      in ap_dict                                      and \
         'id'           in ap_dict                                      and \
         'published'    in ap_dict                                      and \
         'sensitive'    in ap_dict                                      and \
         'source'       in ap_dict                                      and \
           'mediaType'    in ap_dict['source']                          and \
           'content'      in ap_dict['source']                          and \
         'tag'          in ap_dict                                      and \
         'to'           in ap_dict and len(ap_dict['to'])  == 1         and \
         'type'         in ap_dict and ap_dict['type']     == 'Note'    and \
         'url'          in ap_dict


def IsValidActivity(ap_dict):
  # DEBUG BEGIN
  #import json ; print("IsValidActivity() ap_dict=" + json.dumps(ap_dict))
  print("IsValidActivity() TODO:")
  # DEBUG END


  # TODO: validate baseline AP message
  return '@context'     in ap_dict and ap_dict['@context'] == AP_NS_URL and \
         'attributedTo' in ap_dict                                      and \
         'content'      in ap_dict                                      and \
         'id'           in ap_dict                                      and \
         'to'           in ap_dict and len(ap_dict['to'])  == 1


## setup ##

Db        = ListDatabase()
ApManager = Manager(defaults=LOCAL_CONFIG , database=Db)


# DEBUG BEGIN

def DbgTraceIsValidActivity(ap_dict):
  if '@context'     in ap_dict:
    print("'@context'     in")
  else: print("context not in")
  if ap_dict['@context']     == AP_NS_URL:
    print("'@context'     is")
  else: print("context not is")
  if 'attributedTo' in ap_dict:
    print("'attributedTo'     in")
  else: print("attributedTo not in") ;
  if 'cc'           in ap_dict:
    print("'cc'     in")
  else: print("cc not in")
  if 'content'      in ap_dict:
    print("'content'     in")
  else: print("content not in")
  if 'id'           in ap_dict:
    print("'id'     in")
  else: print("id not in")
  if 'published'    in ap_dict:
    print("'published'     in")
  else: print("published not in")
  if 'sensitive'    in ap_dict:
    print("'sensitive'     in")
  else: print("sensitive not in")
  if 'source'       in ap_dict:
    print("'source'     in")
  else: print("source not in")
  if 'mediaType'    in ap_dict['source']:
    print("'media_type'     in")
  else: print("media not in")
  if 'content'      in ap_dict['source']:
    print("'content'     in")
  else: print("content not in")
  if 'tag'          in ap_dict:
    print("'tag'     in")
  else: print("tag not in")
  if 'to'           in ap_dict:
    print("'to'     in")
  else: print("to not in")
  if len(ap_dict['to']) == 1:
    print("to len ok")
  else: print("to len Nok")
  if 'type'         in ap_dict:
    print("'type'     in")
  else: print("'type'    not in")
  if ap_dict['type']         == 'Note':
    print("'type'" + ap_dict['type'] + "    is")
  else: print("'type'" + ap_dict['type'] + " not   is")
  if 'url'          in ap_dict:
    print("'url'     in")
  else: print("url not in")

# DEBUG END
