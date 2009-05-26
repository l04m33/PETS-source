CREATE TABLE buddies ( uuid char(36) primary key, name varchar(256));
CREATE TABLE buddy_extra (buddy_uuid char(36) references buddies(uuid), name varchar(512), value varchar(512), constraint pk_buddy_extra primary key (buddy_uuid, name));
CREATE TABLE chat_log (id integer primary key, buddy_uuid char(36) references buddies(uuid), content text, log_time date);
CREATE TABLE ext_prefs (ext_id integer references exts(id), name varchar(512), value varchar(512), type varchar(256), constraint pk_ext_prefs primary key (ext_id, name));
CREATE TABLE exts (id integer primary key, name varchar(256), path varchar(512), signature integer unsigned);
CREATE TABLE file_tag (file_hash varchar(256) references local_files(hash), tag_id integer references tags(id), constraint pk_file_tag primary key (file_hash, tag_id));
CREATE TABLE local_files (hash varchar(256) primary key, full_name varchar(512) not null, name varchar(256) not null, seg_size bigint unsigned not null, mod_time date, size bigint);
CREATE TABLE local_segs (hash varchar(256) primary key, offset bigint unsigned, file_hash varchar(256) references local_files(hash), present boolean);
CREATE TABLE prof_attrs ( name varchar(512) primary key, value varchar(512) );
CREATE TABLE tags (id integer primary key, name varchar(256) unique);
CREATE TRIGGER fkt_be_buddies
before insert on buddy_extra
for each row begin
  select raise(rollback, 'referenced "buddy_uuid" does not exist in table "buddies"')
  where (select uuid from buddies where uuid = new.buddy_uuid) is null;
end;
CREATE TRIGGER fkt_cl_buddies
before insert on chat_log
for each row begin
  select raise(rollback, 'referenced "buddy_uuid" does not exist in table "buddies"')
  where (select uuid from buddies where uuid = new.buddy_uuid) is null;
end;
CREATE TRIGGER fkt_ep_exts
before insert on ext_prefs
for each row begin
select raise(rollback, 'referenced "ext_id" does not exist in table "exts"')
where (select id from exts where id = new.ext_id) is null;
end;
CREATE TRIGGER fkt_ft_files
before insert on file_tag
for each row begin
  select raise (rollback, 'referenced "file_hash" does not exist in table "local_files"')
  where (select hash from local_files where hash = new.file_hash) is null;
end;
CREATE TRIGGER fkt_ft_tags
before insert on file_tag
for each row begin
  select raise (rollback, 'referenced "tag_id" does not exist in table "tags"')
  where (select id from tags where id = new.tag_id) is null;
end;
CREATE TRIGGER fkt_segs_files
before insert on local_segs
for each row begin
  select raise (rollback, 'referenced "file_hash" does not exist in table "local_files"')
  where (select hash from local_files where hash = new.file_hash) is null;
end;
CREATE TRIGGER fktd_buddies
before delete on buddies
for each row begin
  delete from buddy_extra where buddy_uuid = old.uuid;
  delete from chat_log where buddy_uuid = old.uuid;
end;
CREATE TRIGGER fktd_exts
before delete on exts
for each row begin
  delete from ext_prefs where ext_id = old.id;
end;
CREATE TRIGGER fktd_files
before delete on local_files
for each row begin
  delete from file_tag where file_hash = old.hash;
  delete from local_segs where file_hash = old.hash;
end;
CREATE TRIGGER fktd_tags
before delete on tags
for each row begin
  delete from file_tag where tag_id = old.id;
end;
CREATE TRIGGER fktu_be_buddies
before update on buddy_extra
for each row begin
  select raise(rollback, 'referenced "buddy_uuid" does not exist in table "buddies"')
  where (select uuid from buddies where uuid = new.buddy_uuid) is null;
end;
CREATE TRIGGER fktu_cl_buddies
before update on chat_log
for each row begin
  select raise(rollback, 'referenced "buddy_uuid" does not exist in table "buddies"')
  where (select uuid from buddies where uuid = new.buddy_uuid) is null;
end;
CREATE TRIGGER fktu_ep_exts
before update on ext_prefs
for each row begin
select raise(rollback, 'referenced "ext_id" does not exist in table "exts"')
where (select id from exts where id = new.ext_id) is null;
end;
CREATE TRIGGER fktu_ft_files
before update on file_tag
for each row begin
select raise (rollback, 'referenced "file_hash" does not exist in table "local_files"')
where (select hash from local_files where hash = new.file_hash) is null;
end;
CREATE TRIGGER fktu_ft_tags
before update on file_tag
for each row begin
select raise (rollback, 'referenced "tag_id" does not exist in table "tags"')
where (select id from tags where id = new.tag_id) is null;
end;
CREATE TRIGGER fktu_segs_files
before update on local_segs
for each row begin
  select raise (rollback, 'referenced "file_hash" does not exist in table "local_files"')
  where (select hash from local_files where hash = new.file_hash) is null;
end;

