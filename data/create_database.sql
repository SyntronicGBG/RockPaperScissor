
--CREATE DATABASE RockPaperSciccors


USE RockPaperSciccors

DROP TABLE movie_data
CREATE TABLE movie_data(
    movie_id INT IDENTITY(1,1),
    hand_sign nvarchar(255) NOT NULL,
    left_or_right_hand nvarchar(255) NOT NULL,
    record_time DATETIME NOT NULL,
    movie_file_path NVARCHAR(255) NOT NULL UNIQUE,
    pixel_width INT NOT NULL,
    pixel_height INT NOT NULL,
    fps INT NOT NULL,
    number_frames INT NOT NULL,
    photo_model NVARCHAR(255) NOT NULL,
    angle nvarchar(255) NOT NULL,
    file_format nvarchar(255) NOT NULL,
    PRIMARY KEY(movie_id)
)


