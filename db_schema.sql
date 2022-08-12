CREATE TABLE IF NOT EXISTS TweetVisualizationStreamlit
(
    'created_at' TEXT NOT NULL,
    'id' INT NOT NULL AUTOINCREMENT,
    'source' VARCHAR(200) NOT NULL,
    'clean_text' TEXT DEFAULT NULL,
    'polarity' FLOAT DEFAULT NULL,
    'subjectivity' FLOAT DEFAULT NULL,
    'language' TEXT DEFAULT NULL,
    'favorite_count' INT DEFAULT NULL,
    'retweet_count' INT DEFAULT NULL,
    'original_author' TEXT DEFAULT NULL,
    'screen_count' INT NOT NULL,
    'followers_count' INT DEFAULT NULL,
    'friends_count' INT DEFAULT NULL,
    'hashtags' TEXT DEFAULT NULL,
    'user_mentions' TEXT DEFAULT NULL,
    'place' TEXT DEFAULT NULL,
    'place_coordinate' VARCHAR(150) DEFAULT NULL,
    PRIMARY KEY('id')
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;
