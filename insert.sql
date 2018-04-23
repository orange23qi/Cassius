insert into config_dba_user(name) values ('zhengwei'), ('chenqi'), ('machengcheng');

insert into config_database_type(name) values ('mysql'), ('mongodb');

insert into config_db_area(name) values ('新加坡hsg'), ('新加坡aws'), ('国内qcd');

insert into config_project_teams(name) values ('diva'), ('erp'), ('seller');

insert into schema_list(name, instance_id, type, project_team_id, archive_schema_id, create_time, update_time) values ('userorder_xx', 1, 1, 1 , null, now(), now()), ('garencieres', 2, 1, 2, null, now(), now()), ('ezseller', 1, 1, 3, null, now(), now()), ('ezbuy_xx', 3, 1, 1, null, now(), now());

insert into config_order_status(name) values ('DBA审核'),('用户修改'),('已完成'),('废弃');

insert into config_order_type(name) values ('MySql表结构变更'),('MySql数据库变更'),('MySql数据库申请'),('MySql用户申请');

insert into users(username) values ('zhengwei'), ('chenqi'), ('machengcheng'), (1);

INSERT INTO `user`(`username`, `email`) VALUES ('mico', 'mico@ezbuy.com'),('zhaokongsheng', 'zhaokongsheng@ezbuy.com'),('zhuhongjian', 'zhuhongjian@ezbuy.com'),('yeqianming', 'yeqianming@ezbuy.com'),('chenye', 'chenye@ezbuy.com'),('fuqianneng', 'fuqianneng@ezbuy.com'),('liyunzhan', 'liyunzhan@ezbuy.com'),('liaoqingwen', 'liaoqingwen@ezbuy.com'),('jenkins', 'jenkins@ezbuy.com'),('yangqiang', 'yangqiang@ezbuy.com'),('wangjing', 'wangjing@ezbuy.com'),('xulin', 'xulin@ezbuy.com'),('lingling', 'lingling@ezbuy.com'),('xiemingxu', 'xiemingxu@ezbuy.com'),('huayulei', 'huayulei@ezbuy.com'),('wuxiaojie', 'wuxiaojie@ezbuy.com'),('jimmy', 'jimmy@ezbuy.com'),('yuningning', 'yuningning@ezbuy.com'),('qianyueting', 'qianyueting@ezbuy.com'),('chenhuan', 'chenhuan@ezbuy.com'),('yangxiu', 'yangxiu@ezbuy.com'),('zhoukaifan', 'zhoukaifan@ezbuy.com'),('yinwenhao', 'yinwenhao@ezbuy.com'),('chenyanli', 'chenyanli@ezbuy.com'),('chenqi', 'chenqi@ezbuy.com'),('wangbing', 'wangbing@ezbuy.com'),('jisimin', 'jisimin@ezbuy.com'),('huwen', 'huwen@ezbuy.com'),('shiyongbin', 'shiyongbin@ezbuy.com'),('tanglong', 'tanglong@ezbuy.com'),('zhangyi', 'zhangyi@ezbuy.com'),('zhengwei', 'zhengwei@ezbuy.com'),('zhujiafeng', 'zhujiafeng@ezbuy.com'),('xutianzhi', 'xutianzhi@ezbuy.com'),('shaoyongtao', 'shaoyongtao@ezbuy.com'),('zhonghongtao', 'zhonghongtao@ezbuy.com'),('liufutian', 'liufutian@ezbuy.com'),('chenlinyong', 'chenlinyong@ezbuy.com'),('liuxiaopeng', 'liuxiaopeng@ezbuy.com'),('machengcheng', 'machengcheng@ezbuy.com'),('zhuguanzhou', 'zhuguanzhou@ezbuy.com'),('testqwer', 'testqwer@ezbuy.com'),('hanwenjia', 'hanwenjia@ezbuy.com'),('zhangtianyou', 'zhangtianyou@ezbuy.com');
