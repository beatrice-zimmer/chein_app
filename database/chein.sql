DROP DATABASE IF EXISTS Chein;
CREATE DATABASE Chein;
USE Chein;

-- =====================================================

CREATE TABLE cliente (
    idCliente INT PRIMARY KEY, 
    nome VARCHAR(100),
    email VARCHAR(50),
    usuario VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(32) NOT NULL
);

CREATE TABLE produto (
    idProduto INT PRIMARY KEY,
    nome VARCHAR(100),
    descricao VARCHAR(100),
    preco DECIMAL(9,2),
    estoque INT DEFAULT 100
);

CREATE TABLE compra (
    idCompra INT PRIMARY KEY,
    fkIdCliente INT NOT NULL,
    dataCompra DATETIME DEFAULT NOW(),
    valorTotal DECIMAL(9,2)
);

CREATE TABLE produtoCompra (
    idProdutoCompra INT PRIMARY KEY,
    fkIdCompra INT NOT NULL, 
    fkIdProduto INT NOT NULL,
    quantidade INT DEFAULT 1,
    subTotal DECIMAL(9,2)
);

-- =====================================================

ALTER TABLE compra ADD CONSTRAINT fkCompra
    FOREIGN KEY (fkIdCliente)
    REFERENCES cliente (idCliente)
    ON DELETE CASCADE;
 
ALTER TABLE produtoCompra ADD CONSTRAINT fkProdutoCompra1
    FOREIGN KEY (fkIdProduto)
    REFERENCES produto (idProduto)
    ON DELETE RESTRICT;
 
ALTER TABLE produtoCompra ADD CONSTRAINT fkProdutoCompra2
    FOREIGN KEY (fkIdCompra)
    REFERENCES compra (idCompra)
    ON DELETE CASCADE;

-- =====================================================

-- TRIGGER PARA CALCULAR O SUBTOTAL DE PRODUTOCOMPRA (INSERT)
DROP TRIGGER IF EXISTS calcSubTotalInsert;

DELIMITER $$
CREATE TRIGGER calcSubTotalInsert
BEFORE INSERT
ON produtoCompra
FOR EACH ROW
BEGIN
    DECLARE precoProduto DECIMAL(9,2);
    
    SELECT preco 
    INTO precoProduto
    FROM produto
    WHERE idProduto = NEW.fkIdProduto;

    SET NEW.subTotal = precoProduto * NEW.quantidade;
END$$
DELIMITER ;



-- TRIGGER PARA ATUALIZAR SUBTOTAL DE PRODUTOCOMPRA (UPDATE)
DROP TRIGGER IF EXISTS calcSubTotalUpdate;

DELIMITER $$
CREATE TRIGGER calcSubTotalUpdate
BEFORE UPDATE ON produtoCompra
FOR EACH ROW
BEGIN
    DECLARE precoProduto DECIMAL(9,2);

    SELECT preco
    INTO precoProduto
    FROM produto
    WHERE idProduto = NEW.fkIdProduto;

    SET NEW.subTotal = precoProduto * NEW.quantidade;
END$$
DELIMITER ;



-- TRIGGER PARA CALCULAR O VALOR TOTAL DA COMPRA (INSERT EM PRODUTOCOMPRA)
DROP TRIGGER IF EXISTS calcValorTotal;

DELIMITER $$
CREATE TRIGGER calcValorTotal
AFTER INSERT ON produtoCompra
FOR EACH ROW
BEGIN
    DECLARE total DECIMAL(9,2);

    SELECT SUM(subtotal) 
    INTO total
    FROM produtoCompra
    WHERE fkIdCompra = NEW.fkIdCompra;

    UPDATE compra
    SET valorTotal = total
    WHERE idCompra = NEW.fkIdCompra;
END$$
DELIMITER ;



-- TRIGGER PARA ATUALIZAR O VALOR TOTAL DE COMPRA (UPDATE DE PRODUTOCOMPRA)
DROP TRIGGER IF EXISTS atualizaValorTotalUpdate;

DELIMITER $$
CREATE TRIGGER atualizaValorTotalUpdate
AFTER UPDATE ON produtoCompra
FOR EACH ROW
BEGIN
    DECLARE total DECIMAL(9,2);
    
    SELECT SUM(subTotal)
    INTO total
    FROM produtoCompra
    WHERE fkIdCompra = NEW.fkIdCompra;

    UPDATE compra
    SET valorTotal = total
    WHERE idCompra = NEW.fkIdCompra;
END$$
DELIMITER ;



-- TRIGGER PARA ATUALIZAR O VALORTOTAL DE COMPRA (DELETE EM PRODUTOCOMPRA)
DROP TRIGGER IF EXISTS atualizaValorTotalDelete;

DELIMITER $$
CREATE TRIGGER atualizaValorTotalDelete
AFTER DELETE ON produtoCompra
FOR EACH ROW
BEGIN
    DECLARE total DECIMAL(9,2);

    SELECT SUM(subTotal)
    INTO total
    FROM produtoCompra
    WHERE fkIdCompra = OLD.fkIdCompra;

    UPDATE compra
    SET valorTotal = IFNULL(total, 0)
    WHERE idCompra = OLD.fkIdCompra;
END$$
DELIMITER ;



-- TRIGGER PARA ALTERAR O ESTOQUE (INSERT EM PRODUTOCOMPRA)
DROP TRIGGER IF EXISTS updateEstoque;

DELIMITER $$
CREATE TRIGGER updateEstoque
AFTER INSERT 
ON produtoCompra
FOR EACH ROW
BEGIN
    UPDATE produto
    SET estoque = estoque - NEW.quantidade
    WHERE idProduto = NEW.fkIdProduto;
END$$
DELIMITER ;



-- TRIGGAR PARA ATUALIZAR ESTOQUE (UPDATE EM PRODUTOCOMPRA)
DROP TRIGGER IF EXISTS updateEstoqueUpdate;

DELIMITER $$
CREATE TRIGGER updateEstoqueUpdate
AFTER UPDATE 
ON produtoCompra
FOR EACH ROW
BEGIN
    UPDATE produto
    SET estoque = estoque + OLD.quantidade
    WHERE idProduto = OLD.fkIdProduto;

    UPDATE produto
    SET estoque = estoque - NEW.quantidade
    WHERE idProduto = NEW.fkIdProduto;
END$$
DELIMITER ;



-- TRIGGER PARA ATUALIZAR ESTOQUE (DELETE EM PRODUTOCOMPRA)
DROP TRIGGER IF EXISTS updateEstoqueDelete;

DELIMITER $$
CREATE TRIGGER updateEstoqueDelete
AFTER DELETE 
ON produtoCompra
FOR EACH ROW
BEGIN
    UPDATE produto
    SET estoque = estoque + OLD.quantidade
    WHERE idProduto = OLD.fkIdProduto;
END$$
DELIMITER ;

-- =====================================================

INSERT INTO cliente (idCliente, nome, email, usuario, senha) VALUES
(1, 'Joao Pereira',      'joao9@email.com',           'joao.pereira',      '176df8dca6350f96ba61e20ffd388ca9'),
(2, 'Maria Silva',       'marias@email.com',          'maria.silva',       '80d10e9949ca848279fd798400af534a'),
(3, 'Ana Lima',          'limaana@email.com',         'ana.lima',          '773522a697d4432e783dcf3893ee26be'),
(4, 'Lucas Carvalho',    'lucas93@email.com',         'lucas.carvalho',    'ea9a1b941f6e7f8afccdb95bf7b302f1'),
(5, 'Pedro Santos',      'pedros@email.com',          'pedro.santos',      '2414eed44fd97f8eabcfdf820716b7ff'),
(6, 'Gabriel Ferreira',  'gabriel@email.com',         'gabriel.ferreira',  'da7a2e8e6303939f65d419e4e2a60f15'),
(7, 'Chappell Roan',     'midwestprincess@email.com', 'chappell.roan',     'da7a2e8e6303939f65d419e4e2a60f15'),
(8, 'Pedro Pascal',      'pedropascal@gmail.com',     'pedro.pascal',      '2414eed44fd97f8eabcfdf820716b7ff'),
(9, 'Beatrice Zimmer',   'beatrice@email.com',        'beatrice.zimmer',   '1aca959640de9ca6e533fb0c996f6372');

INSERT INTO produto (idProduto, nome, descricao, preco) VALUES
(1, 'Camiseta Básica',    'Camiseta de algodão confortável',                 49.90),
(2, 'Calça Jeans Skinny', 'Calça jeans ajustada ao corpo',                  129.90),
(3, 'Jaqueta de Couro',   'Jaqueta sintética com acabamento premium',       199.90),
(4, 'Vestido Floral',     'Vestido curto estampado floral',                  89.90),
(5, 'Tênis Esportivo',    'Tênis leve ideal para corrida',                  249.90),
(6, 'Blusa de Moletom',   'Moletom com capuz e bolso frontal',              159.90),
(7, 'Bermuda Cargo',      'Bermuda com bolsos laterais e ajuste na cintura', 79.90),
(8, 'Sandália Feminina',  'Sandália confortável com salto médio',           119.90),
(9, 'Boné Snapback',      'Boné ajustável com aba reta',                     59.90);

INSERT INTO compra (idCompra, fkIdCliente, dataCompra) VALUES
(1, 2, '2025-04-02'),
(2, 4, '2022-12-03'),
(3, 6, '2024-01-04'),
(4, 8, '2023-09-05'),
(5, 7, '2021-10-06');

INSERT INTO produtoCompra (idProdutoCompra, fkIdCompra, fkIdProduto, quantidade) VALUES
(1, 1, 1, 2),
(2, 1, 2, 3),
(3, 2, 5, 2),
(4, 2, 9, 3),
(5, 4, 6, 2);

INSERT INTO produtoCompra (idProdutoCompra, fkIdCompra, fkIdProduto) VALUES
(6, 3, 2),
(7, 5, 3),
(8, 5, 4);

SELECT * FROM cliente;
SELECT * FROM produto;
SELECT * FROM compra;
SELECT * FROM produtoCompra;