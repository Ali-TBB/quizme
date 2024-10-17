CREATE TABLE IF NOT EXISTS `datasets` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `backup_id` INT,
  `created_at` TIMESTAMP,
  `updated_at` TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `dataset_items` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `dataset_id` INT NOT NULL,
  `role` VARCHAR(255),
  `parts` TEXT,
  `created_at` TIMESTAMP,
  `updated_at` TIMESTAMP,
  FOREIGN KEY (`dataset_id`) REFERENCES datasets(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `quizzes` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `topic` VARCHAR(255) ,
  `difficulty` VARCHAR(10) NOT NULL CHECK (`difficulty` IN ('easy', 'medium', 'hard', 'mixed')),
  `number_of_questions` INT NOT NULL,
  `created_at` TIMESTAMP,
  `updated_at` TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `attachments` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `quiz_id` INT NOT NULL,
  `mime_type` VARCHAR(255) NOT NULL,
  `path` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP,
  `updated_at` TIMESTAMP,
  FOREIGN KEY (`quiz_id`) REFERENCES quizzes(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `questions` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `quiz_id` INT NOT NULL,
  `question_type` VARCHAR(255) NOT NULL CHECK (`question_type` IN ('multiple-answer', 'one-answer')),
  `difficulty` VARCHAR(10) NOT NULL CHECK (`difficulty` IN ('easy', 'medium', 'hard')),
  `content` TEXT NOT NULL,
  `options_ids` TEXT,
  `correct_option_id` INT,
  `created_at` TIMESTAMP ,
  `updated_at` TIMESTAMP ,
  FOREIGN KEY (`quiz_id`) REFERENCES quizzes(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `options` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `question_id` INT NOT NULL,
  `option_text` TEXT NOT NULL,
  `created_at` TIMESTAMP,
  `updated_at` TIMESTAMP,
  FOREIGN KEY (`question_id`) REFERENCES questions(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `answers` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `question_id` INT NOT NULL,
  `quiz_id` INT NOT NULL,
  `answer_ids` TEXT, 
  `correct_ids` TEXT,
  `created_at` TIMESTAMP,
  `updated_at` TIMESTAMP,
  FOREIGN KEY (`question_id`) REFERENCES questions(`id`) ON DELETE CASCADE
);
