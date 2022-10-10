-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'Users'
-- 
-- ---

DROP TABLE IF EXISTS [Users];

CREATE TABLE [Users] (
  id INTEGER PRIMARY KEY,
  username VARCHAR(20) NOT NULL UNIQUE,
  first_name VARCHAR(20) NOT NULL,
  last_name VARCHAR(20) NOT NULL,
  [password] VARCHAR(120),
  education VARCHAR(35) DEFAULT 'Unknown',
  employment VARCHAR(35) DEFAULT 'Unknown',
  music VARCHAR(40) DEFAULT 'Unknown',
  movie VARCHAR(40) DEFAULT 'Unknown',
  nationality VARCHAR(35) DEFAULT 'Unknown',
  birthday DATE DEFAULT 'Unknown'
);

-- ---
-- Table 'Posts'
-- 
-- ---

DROP TABLE IF EXISTS [Posts];

CREATE TABLE [Posts](
  id INTEGER PRIMARY KEY,
  u_id INTEGER,
  content INTEGER,
  [image] VARCHAR,
  [creation_time] DATETIME,
  FOREIGN KEY (u_id) REFERENCES [Users](id)
);


-- ---
-- Table 'Friends'
-- 
-- ---

DROP TABLE IF EXISTS [Friends];

CREATE TABLE [Friends](
  u_id INTEGER NOT NULL REFERENCES Users,
  f_id INTEGER NOT NULL REFERENCES Users,
  PRIMARY KEY(u_id, f_id),
  FOREIGN KEY (u_id) REFERENCES [Users](id),
  FOREIGN KEY (f_id) REFERENCES [Users](id)
);

-- ---
-- Table 'Comments'
-- 
-- ---

DROP TABLE IF EXISTS [Comments];

CREATE TABLE [Comments](
  id INTEGER PRIMARY KEY,
  p_id INTEGER,
  u_id INTEGER,
  comment VARCHAR(250),
  [creation_time] DATETIME,
  FOREIGN KEY (p_id) REFERENCES Posts(id),
  FOREIGN KEY (u_id) REFERENCES Users(id)
);
