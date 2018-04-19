insert into config_dba_user(name) values ('zhengwei'), ('chenqi'), ('machengcheng');

insert into config_database_type(name) values ('mysql'), ('mongodb');

insert into config_db_area(name) values ('新加坡hsg'), ('新加坡aws'), ('国内qcd');

insert into config_project_teams(name) values ('diva'), ('erp'), ('seller');

insert into schema_list(name, instance_id, type, project_team_id, archive_schema_id, create_time, update_time) values ('userorder_xx', 1, 1, 1 , null, now(), now()), ('garencieres', 2, 1, 2, null, now(), now()), ('ezseller', 1, 1, 3, null, now(), now()), ('ezbuy_xx', 3, 1, 1, null, now(), now());

insert into config_order_status(name) values ('DBA审核'),('用户修改'),('已完成'),('废弃');

insert into config_order_type(name) values ('MySql表结构变更'),('MySql数据库变更'),('MySql数据库申请'),('MySql用户申请');

insert into users(username) values ('zhengwei'), ('chenqi'), ('machengcheng'), (1);
