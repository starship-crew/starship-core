CREATE DATABASE starship;


-- all crews registered in the system
CREATE TABLE crews IF NOT EXISTS (
  token string TINYTEXT PRIMARY KEY, 
  name TINYTEXT UIQUE,
  ship INT, 

  FOREIGN KEY (ship) REFERENCES ships (id)
);

-- all ships registered in the system
CREATE TABLE ships IF NOT EXISTS (
  id INT PRIMARY KEY,
  shame TINYTEXT
)

-- all the details that exist in the game
CREATE TABLE detail_copies IF NOT EXISTS (
  id INT PRIMARY KEY, 
  ship INT, 
  kind INT,

  FOREIGN KEY (ship) REFERENCES ships (id),
  FOREIGN KEY (kind) REFERENCES details (id)
)

-- abstract details
CREATE TABLE details IF NOT EXISTS (
  id INT PRIMARY KEY, 
  kind INT, 
  cost INT NOT NULL,
  health INT NOT NULL, 
  power_generation INT,
  power_consumption INT,
  accel_factor FLOAT,
  damage_absorption INT,
  damage INT,
  name INT,
  description INT,

  FOREIGN KEY (kind) REFERENCES detail_types (id),
  FOREIGN KEY (name) REFERENCES sentences (id,
  FOREIGN KEY (description) REFERENCES sentences (id)
)

-- types of details
CREATE TABLE detail_types IF NOT EXISTS (
  id INT PRIMARY KEY, 
  name INT, 
  description INT,

  FOREIGN KEY (name) REFERENCES sentences (id),
  FOREIGN KEY (description) REFERENCES sentences (id)
)

-- sentences in different languages
CREATE TABLE sentences IF NOT EXISTS (
  id INT, 
  en TEXT,
  ru TEXT
)

-- Obligatory set of parts for a ship
 CREATE TABLE required_ship_details IF NOT EXISTS (
  detail_types INT,

  FOREIGN KEY (detail_types) REFERENCES detail_types (id)
)
