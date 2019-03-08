from activitypub.database import ListDatabase
from activitypub.manager  import Manager

from forgefed_constants import LOCAL_CONFIG


## getters/setters ##

def CreatePerson(person_id):
  person = GetPerson(person_id)

  if not person:
    person = ApManager.Person(id=person_id)

    Db.actors.insert_one(person.to_dict())
    print("created Person(" + person.id + ")")

  return person


def CreateNote(from_id , to_id , body , media_type='text/plain'):
  note = ApManager.Note(**{'from_id'   : from_id                      , \
                           'to'        : [ to_id ]                    , \
                           'cc'        : [ from_id + "/followers" ]   , \
                           'tag'       : []                           , \
                           'source'    : { 'mediaType' : media_type ,
                                           'content'   : body       } , \
                           'sensitive' : False                        , \
                           'temp_uuid' : "$UUID"                      , \
                           'temp_text' : body                         } )
  Db.activities.insert_one(note.to_dict())
  print("created Note(" + note.id + ") " + from_id + " -> " + to_id)

  return note


def GetPerson(person_id):
  return Db.actors.find_one({'id' : person_id})


def GetActivity(activity_id):
  return Db.activities.find_one({'id' : activity_id})


## setup ##

Db        = ListDatabase()
ApManager = Manager(defaults=LOCAL_CONFIG , database=Db)
