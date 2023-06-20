SET PASSWORD FOR root@localhost='';

DROP DATABASE IF EXISTS book;

CREATE DATABASE book;

USE book;

CREATE TABLE booktable (
  bookid INT PRIMARY KEY NOT NULL,
  bookname VARCHAR(100) NOT NULL,
  bookauthor VARCHAR(100) NOT NULL,
  bookprice DECIMAL(10, 2) NOT NULL,
  bookrating DECIMAL(3, 2) NOT NULL
);