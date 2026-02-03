CREATE DATABASE IF NOT EXISTS twitter;
USE twitter;
DROP TABLE IF EXISTS tweet;
DROP TABLE IF EXISTS follows;

CREATE TABLE tweet (
    tweet_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    tweet_ts  DATETIME DEFAULT CURRENT_TIMESTAMP,
    tweet_text VARCHAR(140) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `tweet` ADD INDEX `tweet_user_id_index` (`user_id`);
SHOW INDEXES FROM tweet;

CREATE TABLE follows (
    follower_id INT NOT NULL,
    followee_id INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `follows` ADD INDEX `follows_follower_id_index` (`follower_id`);
SHOW INDEXES FROM follows;