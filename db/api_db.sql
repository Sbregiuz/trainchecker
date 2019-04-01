create table stations (
	id	integer primary key autoincrement not null,
	city	text not null,
	lat	float not null,
	lon	float not null
);

create table itinerary_stops (
	it_id	integer not null,
	st_id	integer not null,
	arrival time not null,
	departure time not null
);

create table itinerary (
	id	integer primary key autoincrement not null,
	train	integer not null,
	cps	integer not null
);

create table trains (
	id integer primary key autoincrement not null,
	av bit not null
);

insert into stations (city, lat, lon) values ('Bologna Centrale', 0.0, 0.0);
insert into stations (city, lat, lon) values ('Bologna San Vitale', 0.0, 0.0);
insert into stations (city, lat, lon) values ('Bologna Mazzini', 0.0, 0.0);
insert into stations (city, lat, lon) values ('Bologna San Ruffillo', 0.0, 0.0);
insert into stations (city, lat, lon) values ('Rastignano', 0.0, 0.0);

insert into trains (av) values (0);

insert into itinerary (train, cps) values ((select last_insert_rowid()), 10)
