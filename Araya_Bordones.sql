drop table if exists producto cascade ;
drop table if exists carrito cascade ;
drop table if exists producto cascade ;
drop table if exists carrito_productos cascade ;
drop table if exists venta cascade ;
drop table if exists cliente cascade ;
drop table if exists historial_de_ventas cascade ;


CREATE TABLE producto(
 	producto_id text PRIMARY KEY,
	precio 		int NOT NULL,
	stock 		int NOT NULL
);

CREATE TABLE carrito(
	carrito_id 	text PRIMARY KEY,
	monto_total int NOT NULL
);

CREATE TABLE carrito_productos(
	carrito_id 	text REFERENCES carrito(carrito_id),
	producto 	text REFERENCES producto(producto_id)
);

CREATE TABLE venta (
	venta_id 	text PRIMARY KEY,
	producto_id text REFERENCES producto(producto_id),
	fecha 		text NOT NULL,
	valor_total int NOT NULL
);

CREATE TABLE cliente (
	rut 		text PRIMARY KEY,
	usuario 	text NOT NULL,
	carrito_id 	text REFERENCES carrito(carrito_id),
	passw 		text NOT NULL,
	saldo 		int NOT NULL
);

CREATE TABLE historial_de_ventas(
	rut 		text REFERENCES cliente(rut),
	venta_id 	text REFERENCES venta(venta_id)
);


