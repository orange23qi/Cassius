CREATE DATABASE IF NOT EXISTS cassius;

USE cassius;

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username` varchar(64) NOT NULL COMMENT '用户名',
  `email` varchar(64) NOT NULL COMMENT 'EMAIL地址',
  `team_id` int(11) DEFAULT NULL COMMENT '项目组ID,关联config_project_teams表',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_username` (`username`),
  UNIQUE KEY `uniq_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT '用户主表';


DROP TABLE IF EXISTS `config_project_teams`;
CREATE TABLE `config_project_teams` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(64) NOT NULL COMMENT '项目组名称',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT '项目组配置表';


DROP TABLE IF EXISTS `config_dba_user`;
CREATE TABLE `config_dba_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(64) NOT NULL COMMENT 'DBA用户名',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT 'DBA用户配置表';


DROP TABLE IF EXISTS `schema_list`;
CREATE TABLE `schema_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(64) NOT NULL COMMENT 'SCHEMA名称',
  `instance_id` int(11) NOT NULL DEFAULT -1 COMMENT '数据库实例ID,关联database_instance_list表',
  `type_id` tinyint NOT NULL DEFAULT -1 COMMENT '数据库类型ID,关联config_database_type表',
  `parent_id` int(11) NOT NULL DEFAULT -1 COMMENT '父节点ID',
  `project_team_id` int(11) NOT NULL DEFAULT -1 COMMENT '归属项目组ID,关联config_project_teams表',
  `is_sharding` tinyint NOT NULL DEFAULT 0 COMMENT '是否Sharding(0:否,1:是)',
  `is_archive` tinyint NOT NULL DEFAULT 0 COMMENT '是否是归档数据库(0:否,1:是)',
  `archive_schema_id` int(11) NOT NULL DEFAULT -1 COMMENT '对应的归档数据库ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_instance_id` (`instance_id`),
  KEY `idx_parent_id` (`parent_id`),
  KEY `idx_project_team_id` (`project_team_id`),
  KEY `idx_name` (`name`),
  KEY `idx_create_time` (`create_time`),
  KEY `idx_update_time` (`update_time`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT '数据库列表';


DROP TABLE IF EXISTS `config_database_type`;
CREATE TABLE `config_database_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(64) NOT NULL COMMENT '数据库类型名称',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT '数据库类型配置表';


DROP TABLE IF EXISTS `database_instance_list`;
CREATE TABLE `database_instance_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `ip` varchar(64) NOT NULL COMMENT '服务器IP地址',
  `vip` varchar(64) DEFAULT NULL COMMENT '服务器浮动IP地址',
  `port` int(11) NOT NULL COMMENT '数据库实例端口',
  `type_id` tinyint NOT NULL DEFAULT -1 COMMENT '数据库实例类型ID,关联config_database_type表',
  `area_id` tinyint NOT NULL DEFAULT -1 COMMENT '数据库实例位置ID,关联config_database_area表',
  `parent_id` int(11) NOT NULL DEFAULT -1 COMMENT '父节点ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_parent_id` (`parent_id`),
  KEY `idx_create_time` (`create_time`),
  KEY `idx_update_time` (`update_time`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT '数据库实例列表';


DROP TABLE IF EXISTS `config_database_area`;
CREATE TABLE `config_database_area` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(64) NOT NULL COMMENT '地理位置名称',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT '数据库地理位置配置表';


DROP TABLE IF EXISTS `order_list`;
CREATE TABLE `order_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `order_id` int(11) NOT NULL COMMENT '工单ID',
  `owner_id` int(11) NOT NULL COMMENT '申请人ID',
  `order_title` varchar(64) NOT NULL COMMENT '工单标题',
  `order_type` int(11) NOT NULL COMMENT '工单类型,关联config_order_type表',
  `db_type` int(11) NOT NULL COMMENT '数据库类型,关联config_database_type表',
  `order_status` tinyint NOT NULL COMMENT '工单状态',
  `auditor_id` int(11) NOT NULL COMMENT '处理人ID',
  `current_user_id` int(11) NOT NULL COMMENT '当前处理人ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_auditor_id` (`auditor_id`),
  KEY `idx_create_time` (`create_time`),
  KEY `idx_update_time` (`update_time`),
  KEY `idx_current_user_id` (`current_user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT '工单主表';


DROP TABLE IF EXISTS `config_order_type`;
CREATE TABLE `config_order_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(64) NOT NULL COMMENT '工单类型名称',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT '工单类型配置表';


DROP TABLE IF EXISTS `config_order_status`;
CREATE TABLE `config_order_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(64) NOT NULL COMMENT '工单状态名称',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT '工单类型状态表';


DROP TABLE IF EXISTS `order_mysql_ddl_info`;
CREATE TABLE `order_mysql_ddl_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `owner_id` int(11) NOT NULL COMMENT '申请人ID',
  `order_id` int(11) NOT NULL COMMENT '工单ID',
  `order_title` varchar(64) NOT NULL COMMENT '工单标题',
  `db_name` varchar(64) NOT NULL COMMENT '数据库名称',
  `remark_text` text DEFAULT NULL COMMENT '用户备注',
  `sql_text` text NOT NULL COMMENT '语句主体',
  `auditor_id` int(11) NOT NULL COMMENT '处理人ID',
  `current_user_id` int(11) NOT NULL COMMENT '当前处理人ID',
  `order_status` tinyint NOT NULL COMMENT '工单状态',
  `dba_suggest` text DEFAULT NULL COMMENT 'DBA修改建议',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_current_user_id` (`current_user_id`),
  KEY `idx_order_id` (`order_id`),
  KEY `idx_auditor_id` (`auditor_id`),
  KEY `idx_create_time` (`create_time`),
  KEY `idx_update_time` (`update_time`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT 'MySQL DDL明细表';


DROP TABLE IF EXISTS `order_mysql_dml_info`;
CREATE TABLE `order_mysql_dml_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `owner_id` int(11) NOT NULL COMMENT '申请人ID',
  `order_id` int(11) NOT NULL COMMENT '工单ID',
  `order_title` varchar(64) NOT NULL COMMENT '工单标题',
  `db_name` varchar(64) NOT NULL COMMENT '数据库名称',
  `remark_text` text DEFAULT COMMENT '用户备注',
  `sql_text` text NOT NULL COMMENT '语句主体',
  `is_backup` tinyint NOT NULL DEFAULT 0 COMMENT '是否需要备份',
  `auditor_id` int(11) NOT NULL COMMENT '处理人ID',
  `current_user_id` int(11) NOT NULL COMMENT '当前处理人ID',
  `order_status` tinyint NOT NULL COMMENT '工单状态',
  `dba_suggest` text DEFAULT NULL COMMENT 'DBA修改建议',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_current_user_id` (`current_user_id`),
  KEY `idx_create_time` (`create_time`),
  KEY `idx_order_id` (`order_id`),
  KEY `idx_update_time` (`update_time`),
  KEY `idx_auditor_id` (`auditor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT 'MySQL DML明细表';