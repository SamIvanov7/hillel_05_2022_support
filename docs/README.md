1. Social network database model:
https://www.hackerdraw.com/docs/3ec3d8c4-9563-4b44-8f7e-325a88b643e1

### hackerdraw source-code:

```
Table user {
  id integer
  role integer
  first_name varchar
  middle_name varchar
  last_name varchar
  username varchar
  mobile varchar
  email varchar
  password varchar
  profile_bio text
  registered_at timestamp
  last_login timestamp
}

Table roles {
    id integer
    name varchar
    created_at timestamp
    updated_at timestamp

}

Ref: user.role > roles.id

Table comments {
    id integer
    user_id integer
    post_id integer
    content text
    created_at timestamp
    updated_at timestamp
}

Ref: comments.user_id > user.id

Ref: comments.post_id > user_post.id

Table likes {
    id integer
    user_id integer
    post_id integer
    created_at timestamp
    updated_at timestamp
}

Ref: likes.user_id > user.id

Ref: likes.post_id > user_post.id

Table user_friend {
  friendship_id integer
  source_id integer
  target_id integer
  status varchar
  notes varchar
  created_at timestamp
  updated_at timestamp
}

Ref: user_friend.source_id > user.id

Ref: user_friend.target_id > user.id

Table user_blacklist {
  id integer
  source_id integer
  target_id integer
  created_at timestamp
  updated_at timestamp
}
Ref: user_blacklist.source_id > user.id

Ref: user_blacklist.target_id > user.id

Table user_follower {
  id integer
  source_id integer
  target_id integer
  created_at timestamp
  updated_at timestamp
}

Ref: user_follower.source_id > user.id

Ref: user_follower.target_id > user.id

Table user_message {
  id integer
  source_id integer
  target_id integer
  message text
  created_at timestamp
  updated_at timestamp
}

Ref: user_message.source_id > user.id

Ref: user_message.target_id > user.id

Table user_post {
  id integer
  user_id integer
  sender_id integer
  post_message text
  created_at timestamp
  updated_at timestamp
}

Ref: user_post.user_id > user.id

Ref: user_post.sender_id > user.id

Table group {
  id integer
  created_by integer
  updated_by integer
  name varchar
  details text
  profile text
  content text
  created_at timestamp
  updated_at timestamp
}

Ref: group.created_by > user.id

Ref: group.updated_by > user.id

Table group_message {
  id integer
  group_id integer
  user_id integer
  message text
  created_at timestamp
  updated_at timestamp
}

Ref: group_message.group_id > group.id

Ref: group_message.user_id > user.id

Table group_member {
  id integer
  group_id integer
  user_id integer
  role integer
  status integer
  user_notes text
  created_at timestamp
  updated_at timestamp
}

Ref: group_member.group_id > group.id

Ref: group_member.user_id > user.id

Table group_post {
  id integer
  group_id integer
  user_id integer
  message text
  created_at timestamp
  updated_at timestamp
}

Ref: group_post.group_id > group.id
```


2. Car service database model:
www.hackerdraw.com/viewer/3faef111ad7c4bb8925b1898c36d8198

### hackerdraw source-code

```
Table client {
  id integer
  username varchar
  password varchar
  role integer
  last_name varchar
  first_name varchar
  adress_id varchar
  created_at timestamp
  updated_at timestamp
}

Ref: visit.client_id > client.id

Ref: visit.service_id > client.id

Table visit {
  id integer
  client_id integer
  service_id integer
  quantity integer
  input_date timestamp
  output_date timestamp
}

Ref: role.id > client.role

Table role {
  id integer
  name varchar
  created_at timestamp
  updated_at timestamp
}

Table services {
  id integer
  name varchar
  description text
  duration_hours integer
  service_price money
  created_at timestamp
  updated_at timestamp
}

Ref: services.id > visit.service_id
```