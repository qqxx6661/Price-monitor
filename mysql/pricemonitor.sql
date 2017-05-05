/*
Navicat MySQL Data Transfer

Source Server         : qqxx6661
Source Server Version : 50548
Source Host           : localhost:3306
Source Database       : pricemonitor

Target Server Type    : MYSQL
Target Server Version : 50548
File Encoding         : 65001

Date: 2017-05-05 14:52:28
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `monitor`
-- ----------------------------
DROP TABLE IF EXISTS `monitor`;
CREATE TABLE `monitor` (
  `id` smallint(6) NOT NULL AUTO_INCREMENT,
  `item_id` int(11) NOT NULL,
  `item_name` varchar(255) DEFAULT NULL,
  `item_price` decimal(10,2) DEFAULT NULL,
  `user_price` decimal(10,2) NOT NULL,
  `status` smallint(6) NOT NULL,
  `user_id` smallint(6) NOT NULL,
  `mall_name` varchar(255) DEFAULT NULL,
  `note` varchar(255) DEFAULT '无备注',
  `add_date` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for `online_users`
-- ----------------------------
DROP TABLE IF EXISTS `online_users`;
CREATE TABLE `online_users` (
  `session` char(100) NOT NULL DEFAULT '',
  `time` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` smallint(6) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) NOT NULL,
  `user_pwd` varchar(255) NOT NULL,
  `user_email` varchar(255) NOT NULL,
  `register_date` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8;
