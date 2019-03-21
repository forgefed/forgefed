=begin NOTES
NOTES:
  * new_note:            value   ":to => to_actor_url"     breaks message symmetry
  * post_create_message: missing ":to => [ to_actor_url ]" breaks message symmetry
  * post_delete_message: missing ":id => delete_url"       breaks message symmetry
=end NOTES


require 'http'
require 'openssl'


PVT_KEY_FILE   = '../private.pem'
KEY_ID         = 'rsa-pub-key'
PROTOCOL       = 'https'
HOSTNAME       = 'c7fcb87a.ngrok.io'
URL_PREFIX     = PROTOCOL + '://' HOSTNAME '/'
POST_HOST      = 'mastodon.social'
POST_PATH      = '/inbox'
POST_INBOX_URL = "https://#{POST_HOST}/#{POST_PATH}"
DATE           = Time.now.utc.httpdate
POST_HEADERS   = '(request-target) host date'

AP_NS_URLS     = [ "https://www.w3.org/ns/activitystreams" , "https://w3id.org/security/v1" ]
AP_CONTEXT     = { :@context => AP_NS_URLS }
AP_ACCEPT_TYPE = 'Accept'
AP_CREATE_TYPE = 'Create'
AP_DELETE_TYPE = 'Delete'
AP_FOLLOW_TYPE = 'Follow'
AP_NOTE_TYPE   = 'Note'
AP_UNDO_TYPE   = 'Undo'


def new_note note_url , from_actor_url , to_actor_url , reply_to_url
  {
    :id           => note_url             ,
    :type         => AP_NOTE_TYPE         ,
    :published    => DATE                 ,
    :attributedTo => from_actor_url       ,
    :to           => to_actor_url         ,
    :inReplyTo    => reply_to_url         ,
    :content      => '<p>Hello world</p>'
  }
end

def new_follow follow_url , from_actor_url , to_actor_url , follow_target_url
  {
    :id     => follow_url        ,
    :type   => AP_FOLLOW_TYPE    ,
    :actor  => from_actor_url    ,
    :to     => [ to_actor_url ]  ,
    :object => follow_target_url
  }
end

def post_create_message post_url , create_url , from_actor_url , ap_dict
  ap_dict =
  {
    :id     => create_url     ,
    :type   => AP_CREATE_TYPE ,
    :actor  => from_actor_url ,
    :object => ap_dict
  }

  post post_url , ap_dict
end

def post_accept_message post_url , accept_url , from_actor_url , to_actor_url , ap_dict
  ap_dict =
  {
    :id     => accept_url       ,
    :type   => AP_ACCEPT_TYPE   ,
    :actor  => from_actor_url   ,
    :to     => [ to_actor_url ] ,
    :object => ap_dict
  }

  post post_url , ap_dict
end

def post_undo_message post_url , undo_url , from_actor_url , to_actor_url , ap_dict
  ap_dict =
  {
    :id     => undo_url         ,
    :type   => AP_UNDO_TYPE     ,
    :actor  => from_actor_url   ,
    :to     => [ to_actor_url ] ,
    :object => ap_dict
  }

  post post_url , ap_dict
end

def post_delete_message post_url , from_actor_url , to_actor_url , ap_dict
  ap_dict =
  {
    :type   => AP_DELETE_TYPE   ,
    :actor  => from_actor_url   ,
    :to     => [ to_actor_url ] ,
    :object => ap_dict
  }

  post post_url , ap_dict
end

def post post_url , ap_dict
  keypair       = OpenSSL::PKey::RSA.new File.read PVT_KEY_FILE
  signed_string = "(request-target): post #{POST_PATH}\nhost: #{POST_HOST}\ndate: #{DATE}"
  raw_sig       = keypair.sign OpenSSL::Digest::SHA256.new , signed_string
  signature     = Base64.strict_encode64 raw_sig
  sig_header    = "keyId=\"#{key_id}\",headers=\"#{POST_HEADERS}\",signature=\"#{signature}\""
  headers       = { :Host => "#{POST_HOST}" , :Date => DATE , :Signature => sig_header }
  post_body     = (ap_dict.merge AP_CONTEXT).to_json

  (HTTP.headers headers).post post_url , :body => post_body
end


=begin POST_NEW_NOTE
actor_id     = 'alice@' + HOSTNAME
author_id    = 'bob@' + HOSTNAME
actor_url    = URL_PREFIX + actor_id
author_url   = URL_PREFIX + author_id
create_url   = URL_PREFIX + 'what-goes-here'
note_url     = URL_PREFIX + 'what-goes-here-too'
reply_to_url = URL_PREFIX + 'note-id'
key_id       = URL_PREFIX + author_id + '#' + KEY_ID
inbox_url    = URL_PREFIX + actor_id + POST_PATH

ap_note = new_note note_url , author_url , reply_to_url , actor_url
post_create_message POST_INBOX_URL , create_url , actor_url , ap_note
=end POST_NEW_NOTE
