/*
Navicat MySQL Data Transfer

Source Server         : yzd
Source Server Version : 50548
Source Host           : 115.159.190.214:3306
Source Database       : pricemonitor

Target Server Type    : MYSQL
Target Server Version : 50548
File Encoding         : 65001

Date: 2017-04-28 14:36:14
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
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for `user`
-- ----------------------------

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` smallint(6) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) NOT NULL,
  `user_pwd` varchar(255) NOT NULL,
  `user_email` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

