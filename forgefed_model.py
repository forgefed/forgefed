from activitypub.database import ListDatabase
from activitypub.manager  import Manager

from forgefed_constants import *


def DbId(id):
  return DB_ID_PREFIX + id


def MakeGlobalId(id):
  return id + GLOBAL_ID_SUFFIX


def CreatePerson(id):
  person = GetPerson(id)

  if not person:
    person           = ApManager.Person(id=id)
    person.global_id = MakeGlobalId(id)

    Db.actors.insert_one(person.to_dict())
    print("created Person(" + person.id + ")")

  return person


def GetPerson(id):
  return Db.actors.find_one({'id' : DbId(id)})


## main entry ##

Db        = ListDatabase()
ApManager = Manager(database=Db)
Alice     = CreatePerson(id='alice')
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


# DEBUG BEGIN
print("init Alice=" + str(Alice) + " => " + str(GetPerson('alice')))
# DEBUG END
