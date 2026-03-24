/*
 Navicat Premium Dump SQL

 Source Server         : test
 Source Server Type    : MySQL
 Source Server Version : 80040 (8.0.40)
 Source Host           : localhost:3306
 Source Schema         : clever_farming

 Target Server Type    : MySQL
 Target Server Version : 80040 (8.0.40)
 File Encoding         : 65001

 Date: 24/03/2026 19:51:45
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for agri_news_articles
-- ----------------------------
DROP TABLE IF EXISTS `agri_news_articles`;
CREATE TABLE `agri_news_articles`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `nid` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '资讯唯一编号',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文章标题',
  `url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '原文链接(唯一)',
  `category` enum('nyqx','nszd','trsq','zwbch','nyyw') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '分类: nyqx(气象)/nszd(指导)/trsq(土壤)/zwbch(病虫)/nyyw(要闻)',
  `entities` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '提取的实体特征(用于双塔/IP2)',
  `publish_time` datetime NULL DEFAULT NULL COMMENT '网站发布时间',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '系统抓取时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_url`(`url` ASC) USING BTREE,
  INDEX `idx_category`(`category` ASC) USING BTREE,
  INDEX `idx_publish_time`(`publish_time` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 111 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of agri_news_articles
-- ----------------------------
INSERT INTO `agri_news_articles` VALUES (1, 'N_61502b1c', '青藏高原东部多雨雪天气 南方阴雨天气持续', 'http://www.agri.cn/sc/nyqx/202603/t20260324_8822055.htm', 'nyqx', '', '2026-03-24 12:00:00', '2026-03-24 17:44:51');
INSERT INTO `agri_news_articles` VALUES (2, 'N_08568298', '南方地区持续阴雨  青藏高原东部多雨雪', 'http://www.agri.cn/sc/nyqx/202603/t20260324_8822054.htm', 'nyqx', '', '2026-03-24 12:00:00', '2026-03-24 17:44:51');
INSERT INTO `agri_news_articles` VALUES (3, 'N_83fc361d', '南方阴雨持续 新疆雨雪将再度发展', 'http://www.agri.cn/sc/nyqx/202603/t20260323_8821628.htm', 'nyqx', '', '2026-03-23 12:00:00', '2026-03-24 17:44:51');
INSERT INTO `agri_news_articles` VALUES (4, 'N_4a785cbb', '南方地区多阴雨  青藏高原东部多雨雪', 'http://www.agri.cn/sc/nyqx/202603/t20260323_8821627.htm', 'nyqx', '', '2026-03-23 12:00:00', '2026-03-24 17:44:51');
INSERT INTO `agri_news_articles` VALUES (5, 'N_d830142b', '江南华南北部等地有中到大雨 西藏西部和南部有强雨雪', 'http://www.agri.cn/sc/nyqx/202603/t20260320_8821076.htm', 'nyqx', '', '2026-03-20 12:00:00', '2026-03-24 17:44:51');
INSERT INTO `agri_news_articles` VALUES (6, 'N_fd9bc0fa', '南方地区多阴雨  西藏西部和南部有强雨雪', 'http://www.agri.cn/sc/nyqx/202603/t20260320_8821074.htm', 'nyqx', '', '2026-03-20 12:00:00', '2026-03-24 17:44:51');
INSERT INTO `agri_news_articles` VALUES (7, 'N_fc38f701', '西南地区东部江南等地阴雨持续', 'http://www.agri.cn/sc/nyqx/202603/t20260319_8820740.htm', 'nyqx', '', '2026-03-19 12:00:00', '2026-03-24 17:44:51');
INSERT INTO `agri_news_articles` VALUES (8, 'N_9b973279', '西南地区至长江中下游多降水', 'http://www.agri.cn/sc/nyqx/202603/t20260319_8820739.htm', 'nyqx', '', '2026-03-19 12:00:00', '2026-03-24 17:44:51');
INSERT INTO `agri_news_articles` VALUES (9, 'N_b41d96f3', '冷空气影响黄淮以北地区 西南地区东部至江南等地多降雨', 'http://www.agri.cn/sc/nyqx/202603/t20260318_8820413.htm', 'nyqx', '降雨', '2026-03-18 12:00:00', '2026-03-24 17:44:51');
INSERT INTO `agri_news_articles` VALUES (10, 'N_226caf39', '西南地区至长江中下游多降水  冷空气影响黄淮及以北地区', 'http://www.agri.cn/sc/nyqx/202603/t20260318_8820411.htm', 'nyqx', '', '2026-03-18 12:00:00', '2026-03-24 17:44:51');
INSERT INTO `agri_news_articles` VALUES (11, 'N_508aab26', '2026年南方早稻生产技术意见', 'http://www.agri.cn/sc/nszd/202603/t20260313_8818780.htm', 'nszd', '', '2026-03-13 12:00:00', '2026-03-24 17:44:52');
INSERT INTO `agri_news_articles` VALUES (12, 'N_789ef8e1', '2026年北方春季蔬菜生产管理技术指导意见', 'http://www.agri.cn/sc/nszd/202603/t20260302_8815925.htm', 'nszd', '', '2026-03-02 12:00:00', '2026-03-24 17:44:52');
INSERT INTO `agri_news_articles` VALUES (13, 'N_7004eeb8', '2026年南方春季蔬菜生产管理技术指导意见', 'http://www.agri.cn/sc/nszd/202603/t20260302_8815900.htm', 'nszd', '', '2026-03-02 12:00:00', '2026-03-24 17:44:52');
INSERT INTO `agri_news_articles` VALUES (14, 'N_54ba78ba', '2026年冬小麦增施肥促壮苗技术意见', 'http://www.agri.cn/sc/nszd/202602/t20260214_8812660.htm', 'nszd', '小麦,施肥', '2026-02-14 12:00:00', '2026-03-24 17:44:53');
INSERT INTO `agri_news_articles` VALUES (15, 'N_7fcc6e53', '2026年冬小麦春季管理技术意见', 'http://www.agri.cn/sc/nszd/202601/t20260130_8808105.htm', 'nszd', '小麦', '2026-01-30 12:00:00', '2026-03-24 17:44:53');
INSERT INTO `agri_news_articles` VALUES (16, 'N_ac2f67fe', '2026年冬油菜春季管理技术意见', 'http://www.agri.cn/sc/nszd/202601/t20260130_8808103.htm', 'nszd', '', '2026-01-30 12:00:00', '2026-03-24 17:44:53');
INSERT INTO `agri_news_articles` VALUES (17, 'N_f4ab6832', '园艺作物应对低温冻害技术指导意见', 'http://www.agri.cn/sc/nszd/202512/t20251230_8798978.htm', 'nszd', '', '2025-12-30 12:00:00', '2026-03-24 17:44:53');
INSERT INTO `agri_news_articles` VALUES (18, 'N_93dd6970', '冬小麦防冻害保安全越冬技术意见', 'http://www.agri.cn/sc/nszd/202512/t20251209_8792865.htm', 'nszd', '小麦', '2025-12-09 12:00:00', '2026-03-24 17:44:53');
INSERT INTO `agri_news_articles` VALUES (19, 'N_f22b9e24', '生猪养殖降本增效技术指导意见', 'http://www.agri.cn/sc/nszd/202512/t20251203_8791290.htm', 'nszd', '', '2025-12-03 12:00:00', '2026-03-24 17:44:53');
INSERT INTO `agri_news_articles` VALUES (20, 'N_d761afb8', '2025年油菜冬前田间管理技术意见', 'http://www.agri.cn/sc/nszd/202511/t20251127_8789800.htm', 'nszd', '', '2025-11-27 12:00:00', '2026-03-24 17:44:53');
INSERT INTO `agri_news_articles` VALUES (41, 'N_d6f4d3c3', '全省墒情整体适宜  分类施策促苗转化升级', 'http://www.agri.cn/sc/zxjc/trsq/202603/t20260302_8815880.htm', 'trsq', '墒情', '2026-03-02 12:00:00', '2026-03-24 18:18:09');
INSERT INTO `agri_news_articles` VALUES (42, 'N_1b5aec6f', '全省墒情整体适宜  促根增蘖确保全苗越冬', 'http://www.agri.cn/sc/zxjc/trsq/202601/t20260126_8806455.htm', 'trsq', '墒情', '2026-01-26 12:00:00', '2026-03-24 18:18:09');
INSERT INTO `agri_news_articles` VALUES (43, 'N_5cfcd982', '全省墒情整体适宜  抗旱防冻保苗安全越冬', 'http://www.agri.cn/sc/zxjc/trsq/202512/t20251231_8799325.htm', 'trsq', '墒情', '2025-12-31 12:00:00', '2026-03-24 18:18:09');
INSERT INTO `agri_news_articles` VALUES (44, 'N_faf67635', '全省墒情整体适宜 一促到底培育壮苗', 'http://www.agri.cn/sc/zxjc/trsq/202511/t20251124_8788704.htm', 'trsq', '墒情', '2025-11-24 12:00:00', '2026-03-24 18:18:09');
INSERT INTO `agri_news_articles` VALUES (45, 'N_33a17ac8', '全省墒情整体适宜局地偏多  适墒播种以肥促长培育壮苗', 'http://www.agri.cn/sc/zxjc/trsq/202510/t20251030_8781488.htm', 'trsq', '墒情', '2025-10-30 12:00:00', '2026-03-24 18:18:09');
INSERT INTO `agri_news_articles` VALUES (46, 'N_18019a5e', '大部地区降水偏多  全省墒情整体适宜', 'http://www.agri.cn/sc/zxjc/trsq/202509/t20250925_8771071.htm', 'trsq', '墒情', '2025-09-25 12:00:00', '2026-03-24 18:18:10');
INSERT INTO `agri_news_articles` VALUES (47, 'N_157f6254', '全省墒情整体适宜  因地制宜抓好各项田间管理', 'http://www.agri.cn/sc/zxjc/trsq/202509/t20250902_8764175.htm', 'trsq', '墒情', '2025-09-02 12:00:00', '2026-03-24 18:18:10');
INSERT INTO `agri_news_articles` VALUES (48, 'N_3c378eab', '北方冬麦区和西北春播区墒情持续不足 东北春播区墒情适宜', 'http://www.agri.cn/sc/zxjc/trsq/202508/t20250811_8757875.htm', 'trsq', '墒情', '2025-08-11 12:00:00', '2026-03-24 18:18:10');
INSERT INTO `agri_news_articles` VALUES (49, 'N_de340373', '夏收夏种期间全国主要农区土壤墒情', 'http://www.agri.cn/sc/zxjc/trsq/202506/t20250630_8745214.htm', 'trsq', '土壤,墒情', '2025-06-30 12:00:00', '2026-03-24 18:18:10');
INSERT INTO `agri_news_articles` VALUES (50, 'N_bc91c896', '黄土高原春播区墒情持续不足 东北春播区大部墒情适宜 局地墒情过多', 'http://www.agri.cn/sc/zxjc/trsq/202506/t20250605_8738815.htm', 'trsq', '墒情', '2025-06-05 12:00:00', '2026-03-24 18:18:10');
INSERT INTO `agri_news_articles` VALUES (51, 'N_22ebe2a5', '2026年全国油菜重大病虫害发生趋势预报', 'http://www.agri.cn/sc/zxjc/zwbch/202603/t20260302_8815881.htm', 'zwbch', '病虫害,虫害', '2026-03-02 12:00:00', '2026-03-24 18:18:11');
INSERT INTO `agri_news_articles` VALUES (52, 'N_e34a7efa', '2026年全国玉米重大病虫害发生趋势预报', 'http://www.agri.cn/sc/zxjc/zwbch/202601/t20260126_8806456.htm', 'zwbch', '玉米,病虫害,虫害', '2026-01-26 12:00:00', '2026-03-24 18:18:11');
INSERT INTO `agri_news_articles` VALUES (53, 'N_228b639b', '新野：做大“菜篮子” 铺就致富好路子', 'http://www.agri.cn/sc/zxjc/zwbch/202601/t20260112_8802110.htm', 'zwbch', '', '2026-01-12 12:00:00', '2026-03-24 18:18:11');
INSERT INTO `agri_news_articles` VALUES (54, 'N_2bb7ad6d', '百姓“菜篮子”物丰量足“鲜”味浓 土特产点燃“年货经济”新引擎', 'http://www.agri.cn/sc/zxjc/zwbch/202601/t20260112_8802109.htm', 'zwbch', '', '2026-01-12 12:00:00', '2026-03-24 18:18:11');
INSERT INTO `agri_news_articles` VALUES (55, 'N_7ac08f5f', '崇明市民寒冬“菜篮子”，有保障！', 'http://www.agri.cn/sc/zxjc/zwbch/202601/t20260112_8802108.htm', 'zwbch', '', '2026-01-12 12:00:00', '2026-03-24 18:18:11');
INSERT INTO `agri_news_articles` VALUES (56, 'N_f8553e1f', '生物防治“三进”对接活动在江西南昌成功举办', 'http://www.agri.cn/sc/zxjc/zwbch/202512/t20251231_8799326.htm', 'zwbch', '', '2025-12-31 12:00:00', '2026-03-24 18:18:11');
INSERT INTO `agri_news_articles` VALUES (57, 'N_03ed2a4f', '2025年秋播冬油菜苗期病虫害防控技术指导意见', 'http://www.agri.cn/sc/zxjc/zwbch/202510/t20251030_8781492.htm', 'zwbch', '病虫害,虫害', '2025-10-30 12:00:00', '2026-03-24 18:18:11');
INSERT INTO `agri_news_articles` VALUES (58, 'N_2e69311b', '全国中晚稻重大病虫害发生动态及下阶段发生趋势', 'http://www.agri.cn/sc/zxjc/zwbch/202509/t20250925_8771069.htm', 'zwbch', '病虫害,虫害', '2025-09-25 12:00:00', '2026-03-24 18:18:11');
INSERT INTO `agri_news_articles` VALUES (59, 'N_b76535e4', '“七下八上”玉米重大病虫害发生动态及趋势预测', 'http://www.agri.cn/sc/zxjc/zwbch/202509/t20250902_8764179.htm', 'zwbch', '玉米,病虫害,虫害', '2025-09-02 12:00:00', '2026-03-24 18:18:11');
INSERT INTO `agri_news_articles` VALUES (60, 'N_fa3dabdf', '警惕玉米白斑病在西南东北扩散流行', 'http://www.agri.cn/sc/zxjc/zwbch/202508/t20250811_8757876.htm', 'zwbch', '玉米', '2025-08-11 12:00:00', '2026-03-24 18:18:11');
INSERT INTO `agri_news_articles` VALUES (101, 'N_c9e51f4f', '中国—巴西农业分委会第七次会议在京召开', 'http://www.agri.cn/zx/nyyw/202603/t20260324_8822164.htm', 'nyyw', '', '2026-03-24 12:00:00', '2026-03-24 18:53:00');
INSERT INTO `agri_news_articles` VALUES (102, 'N_3e705683', '农业农村部部署2026年“绿剑护粮安”执法行动', 'http://www.agri.cn/zx/nyyw/202603/t20260324_8822132.htm', 'nyyw', '', '2026-03-24 12:00:00', '2026-03-24 18:53:00');
INSERT INTO `agri_news_articles` VALUES (103, 'N_f9dd94fa', '春早抓培训　稳粮保供给——全国农广校体系开展冬春农民大培训', 'http://www.agri.cn/zx/nyyw/202603/t20260324_8821926.htm', 'nyyw', '', '2026-03-24 12:00:00', '2026-03-24 18:53:00');
INSERT INTO `agri_news_articles` VALUES (104, 'N_c49dbe06', '“稳”与“忧”之间的价格博弈——春耕化肥市场透析', 'http://www.agri.cn/zx/nyyw/202603/t20260324_8821895.htm', 'nyyw', '市场,春耕', '2026-03-24 12:00:00', '2026-03-24 18:53:00');
INSERT INTO `agri_news_articles` VALUES (105, 'N_8d28e574', '科学减油，减出健康', 'http://www.agri.cn/zx/nyyw/202603/t20260324_8821957.htm', 'nyyw', '', '2026-03-24 12:00:00', '2026-03-24 18:53:00');
INSERT INTO `agri_news_articles` VALUES (106, 'N_77135217', '春潮涌动万象新 乡村发展正当时', 'http://www.agri.cn/zx/nyyw/202603/t20260323_8821675.htm', 'nyyw', '', '2026-03-23 12:00:00', '2026-03-24 18:53:00');
INSERT INTO `agri_news_articles` VALUES (107, 'N_a95b4686', '农业农村部等七部门部署2026年春耕备耕农资打假工作', 'http://www.agri.cn/zx/nyyw/202603/t20260323_8821755.htm', 'nyyw', '春耕', '2026-03-23 12:00:00', '2026-03-24 18:53:00');
INSERT INTO `agri_news_articles` VALUES (108, 'N_08336e4a', '抓好春耕生产，总书记念兹在兹', 'http://www.agri.cn/zx/nyyw/202603/t20260323_8821676.htm', 'nyyw', '春耕', '2026-03-23 12:00:00', '2026-03-24 18:53:00');
INSERT INTO `agri_news_articles` VALUES (109, 'N_8a922b12', '李强对全国春季农业生产工作作出重要批示强调 高水平保障粮食等重要农产品稳定安全供给 为实现“十五五”良好开局提供有力支撑', 'http://www.agri.cn/zx/nyyw/202603/t20260323_8821674.htm', 'nyyw', '', '2026-03-23 12:00:00', '2026-03-24 18:53:00');
INSERT INTO `agri_news_articles` VALUES (110, 'N_6ac4345b', '沃野染新绿 春耕绘丰景——从春耕一线看“十五五”开局农业生产新气象', 'http://www.agri.cn/zx/nyyw/202603/t20260323_8821677.htm', 'nyyw', '春耕', '2026-03-23 12:00:00', '2026-03-24 18:53:00');

-- ----------------------------
-- Table structure for community_comments
-- ----------------------------
DROP TABLE IF EXISTS `community_comments`;
CREATE TABLE `community_comments`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `post_id` int NOT NULL,
  `user_id` int NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `post_id`(`post_id` ASC) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `community_comments_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `community_posts` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `community_comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of community_comments
-- ----------------------------
INSERT INTO `community_comments` VALUES (1, 1, 2, '建议多用有机肥', '2026-03-21 22:07:30');
INSERT INTO `community_comments` VALUES (2, 10, 2, '123', '2026-03-22 14:22:30');
INSERT INTO `community_comments` VALUES (3, 13, 3, '不错', '2026-03-22 14:31:05');

-- ----------------------------
-- Table structure for community_posts
-- ----------------------------
DROP TABLE IF EXISTS `community_posts`;
CREATE TABLE `community_posts`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `likes_count` int NULL DEFAULT 0,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `community_posts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of community_posts
-- ----------------------------
INSERT INTO `community_posts` VALUES (1, 2, '我的麦田长势喜人！大家都用什么肥料？', 1, '2026-03-21 22:07:23');
INSERT INTO `community_posts` VALUES (2, 2, '111', 0, '2026-03-21 22:21:18');
INSERT INTO `community_posts` VALUES (3, 2, '112221', 0, '2026-03-21 22:21:23');
INSERT INTO `community_posts` VALUES (4, 3, '111', 0, '2026-03-22 12:58:15');
INSERT INTO `community_posts` VALUES (5, 3, '111', 0, '2026-03-22 12:58:19');
INSERT INTO `community_posts` VALUES (6, 2, '111', 0, '2026-03-22 13:18:06');
INSERT INTO `community_posts` VALUES (7, 2, '111', 0, '2026-03-22 13:18:10');
INSERT INTO `community_posts` VALUES (8, 2, '111', 0, '2026-03-22 13:18:58');
INSERT INTO `community_posts` VALUES (9, 2, '111', 0, '2026-03-22 13:21:59');
INSERT INTO `community_posts` VALUES (10, 2, '1', 0, '2026-03-22 13:27:33');
INSERT INTO `community_posts` VALUES (11, 2, '123', 0, '2026-03-22 14:11:43');
INSERT INTO `community_posts` VALUES (12, 2, '123', 0, '2026-03-22 14:11:46');
INSERT INTO `community_posts` VALUES (13, 2, '123asd', 0, '2026-03-22 14:14:18');
INSERT INTO `community_posts` VALUES (14, 1, '测试帖子 - admin - 2026-03-24 17:43:08', 0, '2026-03-24 17:43:08');
INSERT INTO `community_posts` VALUES (15, 2, '测试帖子 - farmer - 2026-03-24 17:43:08', 0, '2026-03-24 17:43:08');

-- ----------------------------
-- Table structure for daily_tasks
-- ----------------------------
DROP TABLE IF EXISTS `daily_tasks`;
CREATE TABLE `daily_tasks`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '任务标题',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '任务描述',
  `task_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '任务类型',
  `priority` enum('high','medium','low') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'medium' COMMENT '优先级',
  `status` enum('pending','in_progress','completed','cancelled') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'pending' COMMENT '任务状态',
  `scheduled_date` date NOT NULL COMMENT '计划日期',
  `scheduled_time` time NULL DEFAULT NULL COMMENT '计划时间',
  `location` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '任务地点',
  `completed_at` datetime NULL DEFAULT NULL COMMENT '完成时间',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_status`(`status` ASC) USING BTREE,
  INDEX `idx_scheduled_date`(`scheduled_date` ASC) USING BTREE,
  CONSTRAINT `daily_tasks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of daily_tasks
-- ----------------------------
INSERT INTO `daily_tasks` VALUES (1, 2, '小麦病虫害防治', '近期发现小麦叶片出现锈病症状，需要立即进行药剂喷洒防治。建议使用三唑酮或丙环唑，注意用药浓度和安全间隔期。', 'pest_control', 'high', 'completed', '2025-10-18', '08:00:00', '东区田块', '2026-03-21 21:29:07', '2025-10-18 00:58:09', '2026-03-21 21:29:07');
INSERT INTO `daily_tasks` VALUES (2, 2, '灌溉作业', '根据土壤墒情监测，西区田块需要进行灌溉。预计灌溉时间2小时，注意控制水量，避免积水。', 'irrigation', 'medium', 'pending', '2025-10-18', '14:00:00', '西区田块', NULL, '2025-10-18 00:58:09', '2025-10-18 00:58:09');
INSERT INTO `daily_tasks` VALUES (3, 2, '追肥作业', '小麦进入拔节期，需要追施拔节肥。建议每亩施用尿素10-15公斤，结合灌溉进行。', 'fertilization', 'low', 'pending', '2025-10-18', '16:00:00', '南区田块', NULL, '2025-10-18 00:58:09', '2025-10-18 00:58:09');
INSERT INTO `daily_tasks` VALUES (4, 2, '田间巡查', '对所有田块进行日常巡查，检查作物生长情况和病虫害发生情况。', 'inspection', 'low', 'completed', '2025-10-18', '06:00:00', '全部田块', NULL, '2025-10-18 00:58:09', '2025-10-18 00:58:09');
INSERT INTO `daily_tasks` VALUES (5, 2, '去田里喷洒农药', '二化螟防治', NULL, 'high', 'pending', '2026-03-21', '08:00:00', 'A区', NULL, '2026-03-21 22:07:32', '2026-03-21 22:07:32');
INSERT INTO `daily_tasks` VALUES (6, 3, '1', '1', NULL, 'medium', 'pending', '2026-03-22', '08:00:00', '农田', NULL, '2026-03-22 12:58:03', '2026-03-22 12:58:03');
INSERT INTO `daily_tasks` VALUES (7, 2, '11', '11', NULL, 'high', 'pending', '2026-03-22', '08:00:00', '农田', NULL, '2026-03-22 13:19:14', '2026-03-22 13:19:14');

-- ----------------------------
-- Table structure for disease_identification_history
-- ----------------------------
DROP TABLE IF EXISTS `disease_identification_history`;
CREATE TABLE `disease_identification_history`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `disease_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `confidence` decimal(5, 2) NOT NULL,
  `symptoms` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `solutions` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `image_path` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `voice_input` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_created_at`(`created_at` ASC) USING BTREE,
  CONSTRAINT `disease_identification_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of disease_identification_history
-- ----------------------------
INSERT INTO `disease_identification_history` VALUES (1, 2, '稻瘟病', 0.95, '叶片黄', '喷药', NULL, NULL, '2026-03-21 22:07:34');

-- ----------------------------
-- Table structure for farming_alerts
-- ----------------------------
DROP TABLE IF EXISTS `farming_alerts`;
CREATE TABLE `farming_alerts`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `alert_type` enum('news','alert') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '主要类型: news-农情速递, alert-农时预警',
  `alert_subtype` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '子类型: nyyw, nszd, nyqx, trsq, zwbch',
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '标题',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '内容',
  `priority` enum('high','medium','low') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'medium' COMMENT '优先级',
  `is_read` tinyint(1) NULL DEFAULT 0 COMMENT '是否已读',
  `location` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '地区',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `read_at` datetime NULL DEFAULT NULL COMMENT '阅读时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_is_read`(`is_read` ASC) USING BTREE,
  INDEX `idx_created_at`(`created_at` ASC) USING BTREE,
  INDEX `idx_alert_type`(`alert_type` ASC) USING BTREE,
  CONSTRAINT `farming_alerts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of farming_alerts
-- ----------------------------
INSERT INTO `farming_alerts` VALUES (1, 2, 'news', 'nyyw', '2024年春耕备耕工作全面展开', '部委发布最新春耕指导意见，要求各省落实粮食安全责任制，确保种子肥料供应充足。', 'medium', 0, '全国', '2026-03-24 19:46:21', NULL);
INSERT INTO `farming_alerts` VALUES (2, 2, 'news', 'nszd', '小麦拔节期田间管理方案', '当前小麦陆续进入拔节期，需重点抓好追肥、灌溉和化控防倒伏工作。建议亩施尿素10公斤。', 'high', 0, '北京市', '2026-03-24 19:46:21', NULL);
INSERT INTO `farming_alerts` VALUES (3, 2, 'alert', 'nyqx', '暴雨蓝色预警', '预计未来24小时内将有大到暴雨，请注意防范可能引发的洪涝灾害，及时疏通排水沟渠。', 'high', 0, '北京市', '2026-03-24 19:46:21', NULL);
INSERT INTO `farming_alerts` VALUES (4, 2, 'alert', 'trsq', '农田墒情监测报告', '近期降雨偏少，东区田块0-20cm土层含水量降至15%，处于轻度干旱状态，建议适时补充灌溉。', 'medium', 0, '东区田块', '2026-03-24 19:46:21', NULL);
INSERT INTO `farming_alerts` VALUES (5, 2, 'alert', 'zwbch', '稻飞虱虫害红色预警', '近期气温适宜，稻飞虱繁殖加快，田间百丛虫量已达2000头，请立即进行药剂防治。', 'high', 0, '北京市', '2026-03-24 19:46:21', NULL);

-- ----------------------------
-- Table structure for knowledge_nodes
-- ----------------------------
DROP TABLE IF EXISTS `knowledge_nodes`;
CREATE TABLE `knowledge_nodes`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `summary` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `keywords` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `view_count` int NULL DEFAULT 0,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of knowledge_nodes
-- ----------------------------
INSERT INTO `knowledge_nodes` VALUES (1, '水稻种植基础知识', '种植技术', '<h3>一、选种与育苗</h3>\n                        <p>选择适合当地气候条件的优质水稻品种，进行种子处理。育苗时注意控制温度和湿度，确保苗期健康生长。</p>\n                        \n                        <h3>二、整地与移栽</h3>\n                        <p>整地要求平整，保持适当水深。移栽时注意株行距，一般行距30cm，株距20cm。</p>\n                        \n                        <h3>三、田间管理</h3>\n                        <p>包括水分管理、施肥、病虫害防治等。注意不同生长阶段的水肥需求。</p>\n                        \n                        <h3>四、收获与储存</h3>\n                        <p>适时收获，避免过熟或欠熟。储存时注意防潮防虫。</p>', '详细介绍水稻从选种到收获的完整种植流程，包括育苗、移栽、田间管理等关键技术要点。', '水稻,种植,育苗,移栽,田间管理', 0, '2025-10-18 00:58:09', '2025-10-18 00:58:09');
INSERT INTO `knowledge_nodes` VALUES (2, '水稻病虫害综合防治技术', '病虫害防治', '<h3>一、主要病害防治</h3>\n                        <p><strong>稻瘟病：</strong>选用抗病品种，合理施肥，及时排水。发病初期可用三环唑等药剂防治。</p>\n                        <p><strong>纹枯病：</strong>控制田间湿度，合理密植。可用井冈霉素等药剂防治。</p>\n                        \n                        <h3>二、主要虫害防治</h3>\n                        <p><strong>稻飞虱：</strong>采用灯光诱杀，保护天敌。可用吡虫啉等药剂防治。</p>\n                        <p><strong>稻纵卷叶螟：</strong>合理密植，及时除草。可用阿维菌素等药剂防治。</p>\n                        \n                        <h3>三、综合防治策略</h3>\n                        <p>以农业防治为基础，生物防治为重点，化学防治为辅助的综合防治体系。</p>', '全面介绍水稻常见病虫害的识别特征、发生规律和综合防治措施，包括农业防治、生物防治和化学防治。', '水稻,病虫害,防治,稻瘟病,稻飞虱,综合防治', 0, '2025-10-18 00:58:09', '2025-10-18 00:58:09');
INSERT INTO `knowledge_nodes` VALUES (3, '有机肥料制作与使用方法', '肥料管理', '<h3>一、有机肥料类型</h3>\n                        <p><strong>堆肥：</strong>利用秸秆、畜禽粪便等有机废弃物堆制而成。</p>\n                        <p><strong>沤肥：</strong>将有机物料在厌氧条件下沤制而成。</p>\n                        <p><strong>绿肥：</strong>种植豆科作物翻压入土作为肥料。</p>\n                        \n                        <h3>二、制作方法</h3>\n                        <p>1. 选择合适的原料；2. 控制碳氮比；3. 调节水分和温度；4. 定期翻堆；5. 充分腐熟。</p>\n                        \n                        <h3>三、使用方法</h3>\n                        <p>基肥施用为主，追肥为辅。注意与化肥配合使用，提高肥效。</p>', '详细介绍有机肥料的制作工艺、养分特点和使用方法，包括堆肥、沤肥、绿肥等不同类型的有机肥料。', '有机肥,堆肥,沤肥,绿肥,制作,使用', 0, '2025-10-18 00:58:09', '2025-10-18 00:58:09');
INSERT INTO `knowledge_nodes` VALUES (4, '土壤改良与培肥技术', '土壤管理', '<h3>一、土壤问题诊断</h3>\n                        <p>通过土壤检测了解土壤养分状况、pH值、有机质含量等指标。</p>\n                        \n                        <h3>二、改良措施</h3>\n                        <p><strong>深耕：</strong>改善土壤结构，增加耕作层厚度。</p>\n                        <p><strong>增施有机肥：</strong>提高土壤有机质含量，改善土壤理化性质。</p>\n                        <p><strong>调节pH值：</strong>酸性土壤施用石灰，碱性土壤施用石膏。</p>\n                        \n                        <h3>三、培肥技术</h3>\n                        <p>轮作倒茬、种植绿肥、秸秆还田等措施。</p>', '介绍土壤改良的基本原理和方法，包括深耕、增施有机肥、调节土壤pH值等技术措施。', '土壤改良,培肥,深耕,有机质,轮作,绿肥', 0, '2025-10-18 00:58:09', '2025-10-18 00:58:09');
INSERT INTO `knowledge_nodes` VALUES (5, '节水灌溉技术', '灌溉技术', '<h3>一、节水灌溉原理</h3>\n                        <p>通过减少水分损失，提高水分利用效率，实现农业可持续发展。</p>\n                        \n                        <h3>二、主要技术</h3>\n                        <p><strong>滴灌：</strong>将水直接输送到作物根部，节水效果显著。</p>\n                        <p><strong>喷灌：</strong>模拟自然降雨，适合大面积农田。</p>\n                        <p><strong>微灌：</strong>介于滴灌和喷灌之间，适合设施农业。</p>\n                        \n                        <h3>三、管理要点</h3>\n                        <p>根据作物需水规律、土壤墒情、天气预报等因素确定灌溉时间和水量。</p>', '介绍现代农业节水灌溉技术，包括滴灌、喷灌、微灌等高效节水灌溉方式及其适用条件。', '节水灌溉,滴灌,喷灌,微灌,水分利用效率', 0, '2025-10-18 00:58:09', '2025-10-18 00:58:09');
INSERT INTO `knowledge_nodes` VALUES (6, '温室蔬菜栽培技术', '设施农业', '<h3>一、温室环境控制</h3>\n                        <p><strong>温度：</strong>根据作物需求调节温室温度，注意昼夜温差。</p>\n                        <p><strong>湿度：</strong>控制空气湿度，防止病害发生。</p>\n                        <p><strong>光照：</strong>合理设计温室结构，充分利用自然光。</p>\n                        \n                        <h3>二、品种选择</h3>\n                        <p>选择适应性强、抗病性好、产量高的优质品种。</p>\n                        \n                        <h3>三、栽培管理</h3>\n                        <p>合理密植、科学施肥、及时防治病虫害。</p>', '详细介绍温室蔬菜栽培的环境控制、品种选择、栽培管理等关键技术，提高温室蔬菜产量和品质。', '温室,蔬菜,栽培,环境控制,品种选择,栽培管理', 0, '2025-10-18 00:58:09', '2025-10-18 00:58:09');
INSERT INTO `knowledge_nodes` VALUES (7, '智慧农业技术应用', '智慧农业', '<h3>一、物联网技术</h3>\n                        <p>通过传感器实时监测土壤、气候、作物生长状况，实现精准管理。</p>\n                        \n                        <h3>二、大数据分析</h3>\n                        <p>收集和分析农业生产数据，为决策提供科学依据。</p>\n                        \n                        <h3>三、人工智能应用</h3>\n                        <p>利用AI技术进行病虫害识别、产量预测、智能灌溉等。</p>\n                        \n                        <h3>四、自动化设备</h3>\n                        <p>无人农机、自动喷药、智能温室等自动化设备提高生产效率。</p>', '介绍物联网、大数据、人工智能等技术在现代农业中的应用，包括精准农业、智能监测、自动化控制等。', '智慧农业,物联网,大数据,人工智能,精准农业,自动化', 0, '2025-10-18 00:58:09', '2025-10-18 00:58:09');
INSERT INTO `knowledge_nodes` VALUES (8, '农产品质量安全控制', '质量安全', '<h3>一、生产标准</h3>\n                        <p>建立完善的生产标准体系，规范农业生产过程。</p>\n                        \n                        <h3>二、检测方法</h3>\n                        <p>采用先进的检测技术和设备，确保检测结果准确可靠。</p>\n                        \n                        <h3>三、认证体系</h3>\n                        <p>建立有机食品、绿色食品、无公害食品等认证体系。</p>\n                        \n                        <h3>四、追溯系统</h3>\n                        <p>建立农产品质量安全追溯系统，实现全程可追溯。</p>', '介绍农产品质量安全控制体系，包括生产标准、检测方法、认证体系等，确保农产品质量安全。', '农产品,质量安全,生产标准,检测,认证,追溯', 0, '2025-10-18 00:58:09', '2025-10-18 00:58:09');

-- ----------------------------
-- Table structure for operation_logs
-- ----------------------------
DROP TABLE IF EXISTS `operation_logs`;
CREATE TABLE `operation_logs`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `admin_id` int NULL DEFAULT NULL,
  `action` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `module` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `details` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `ip_address` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `operation_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of operation_logs
-- ----------------------------
INSERT INTO `operation_logs` VALUES (1, 1, 1, 'admin_login', 'auth', '管理员登入系统', '127.0.0.1', '2026-03-22 13:16:49');
INSERT INTO `operation_logs` VALUES (2, 1, 1, 'update_config', 'system', '更新系统名称', '127.0.0.1', '2026-03-22 13:16:49');
INSERT INTO `operation_logs` VALUES (3, 1, 1, 'view_users', 'user_management', '查看用户列表', '127.0.0.1', '2026-03-22 13:16:49');

-- ----------------------------
-- Table structure for post_likes
-- ----------------------------
DROP TABLE IF EXISTS `post_likes`;
CREATE TABLE `post_likes`  (
  `user_id` int NOT NULL,
  `post_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`, `post_id`) USING BTREE,
  INDEX `post_id`(`post_id` ASC) USING BTREE,
  CONSTRAINT `post_likes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `post_likes_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `community_posts` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of post_likes
-- ----------------------------
INSERT INTO `post_likes` VALUES (2, 1, '2026-03-21 22:07:28');

-- ----------------------------
-- Table structure for system_configs
-- ----------------------------
DROP TABLE IF EXISTS `system_configs`;
CREATE TABLE `system_configs`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `config_key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `config_value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `config_key`(`config_key` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_configs
-- ----------------------------
INSERT INTO `system_configs` VALUES (1, 'site_name', '智禾慧农管理系统', '系统主站名称', '2026-03-22 13:16:49');
INSERT INTO `system_configs` VALUES (2, 'maintenance_mode', '0', '是否开启维护模式 (0: 否, 1: 是)', '2026-03-22 13:16:49');
INSERT INTO `system_configs` VALUES (3, 'max_upload_size', '10', '最大上传文件大小 (MB)', '2026-03-22 13:16:49');
INSERT INTO `system_configs` VALUES (4, 'registration_open', '1', '是否开放新用户注册 (0: 否, 1: 是)', '2026-03-22 13:16:49');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` enum('user','admin') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'user',
  `location` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '详细地址',
  `city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT '北京' COMMENT '城市',
  `crop_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT '小麦' COMMENT '种植作物类型',
  `farm_area` decimal(10, 2) NULL DEFAULT NULL COMMENT '农田面积（亩）',
  `avatar_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '头像URL',
  `last_login` datetime NULL DEFAULT NULL COMMENT '最后登录时间',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_initialized` tinyint(1) NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'admin', '$2b$12$mLGL8njNxh8LMhjUJcfgo.3iAQb2yt6w39K.DoKSgZDtksnvFHeC2', 'admin', NULL, '北京', '小麦', 100.00, NULL, NULL, '2025-10-18 00:58:09', '2026-03-22 19:38:57', 1);
INSERT INTO `users` VALUES (2, 'farmer', '$2b$12$NyemLRt9Za.m3.mFNe1PvOrC7yLg3LQGNMMLoZ15ZoCWkkgFcaNTy', 'user', '武汉市', '武汉', '水稻', 50.00, 'https://ts1.tc.mm.bing.net/th/id/OIP-C.FZ6GQ0UcHCLgdPoHx-4UlgHaHa?rs=1&pid=ImgDetMain&o=7&rm=3', NULL, '2025-10-18 00:58:09', '2026-03-22 19:38:58', 1);
INSERT INTO `users` VALUES (3, 'test_yang', '$2b$12$NTsRYTy1Jmjcx3FhZ9O02OnhPczsCv84BLQOKV5ZU7wA.xLBZiuie', 'user', NULL, '上海', '玉米', 80.00, NULL, NULL, '2026-03-22 04:57:24', '2026-03-22 19:38:58', 1);
INSERT INTO `users` VALUES (4, '111', '$2b$12$zLXpIfQkfBZs5UqFUmq90Ob7TGoZbxTA4CnnICEDceUyaTAmfppIG', 'user', NULL, '广州', '小麦', 30.00, NULL, NULL, '2026-03-22 07:30:30', '2026-03-24 19:16:23', 1);
INSERT INTO `users` VALUES (5, 'test_user_new', '$2b$12$oq8Cn1191JtRPFDeCXIItuCHdFbuwpcvvmTGxtq5nBp.hCbQcIlvq', 'user', NULL, '深圳', '水果', 25.50, NULL, NULL, '2026-03-22 11:41:53', '2026-03-22 19:41:53', 1);
INSERT INTO `users` VALUES (6, 'test_user_2430', '$2b$12$NoDnV0jZfE0gx5kRSgz7TuwQ0/SB9VMuaa9.wdKDHHCCFJ5iis7SW', 'user', NULL, '深圳', '水果', 25.50, NULL, NULL, '2026-03-22 11:44:15', '2026-03-22 19:44:14', 1);
INSERT INTO `users` VALUES (7, 'test_user_6741', '$2b$12$MnL2QsBKc4dFzBs2Iu2jfOb4hXzpdGM7Qnbm5In71vvzA62WFLe5a', 'user', NULL, '深圳', '水果', 25.50, NULL, NULL, '2026-03-22 11:45:21', '2026-03-22 19:45:20', 1);
INSERT INTO `users` VALUES (8, '1234', '$2b$12$UPey.TjceRd82HIkz/7vueMQOiBzukAsRgE/GfQpt/no2JI5WpCW.', 'user', NULL, '长沙', '棉花', 20.00, NULL, NULL, '2026-03-22 12:01:43', '2026-03-22 20:01:43', 1);

SET FOREIGN_KEY_CHECKS = 1;
