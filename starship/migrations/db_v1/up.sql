CREATE DATABASE starship_db;


-- все экипажи зарегестрированные в системе
CREATE TABLE crews (
  token string TINYTEXT PRIMARY KEY, 
  name TINYTEXT UIQUE,
  ship INT, 

  FOREIGN KEY (ship) REFERENCES ships (id)
);

-- все корабли зарегестрированные в системе
CREATE TABLE ships (
  id INT PRIMARY KEY,
  shame TINYTEXT
)

-- все детали существующие в игре
CREATE TABLE dateil_copies (
  id INT PRIMARY KEY, 
  ship INT, 
  kind INT,

  FOREIGN KEY (ship) REFERENCES ships (id),
  FOREIGN KEY (kind) REFERENCES details (id)
)

-- абстрактные детали
CREATE TABLE datails (
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

-- типы деталей
CREATE TABLE detail_types(
  id INT PRIMARY KEY, 
  name INT, 
  description INT,

  FOREIGN KEY (name) REFERENCES sentences (id),
  FOREIGN KEY (description) REFERENCES sentences (id)
)

-- предложения на разных языках
CREATE TABLE sentences (
  id INT, 
  en TEXT,
  ru TEXT
)

-- Обязательный набор деталей для коробля
 CREATE TABLE required_ship_details (
  detail_types INT,

  FOREIGN KEY (detail_types) REFERENCES detail_types (id)
)
