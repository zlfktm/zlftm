create database pethotel;

use pethotel;

create table PetOwners(
	ownerID int primary key auto_increment,
    name varchar(45),
    contact varchar(45)
);

create table Pets(
	petID int primary key auto_increment,
    ownerID int,
    foreign key (ownerID) references PetOwners(ownerID),
    name varchar(45),
    species varchar(45),
    breed varchar(45)
);

create table Rooms(
	roomID int primary key auto_increment,
    roomNumber int,
    roomType varchar(45),
    pricePerNight int
);

create table Reservations(
	reservationID int primary key auto_increment,
    petID int,
    foreign key (petID) references Pets(petID),
    roomID int,
    foreign key (roomID) references Rooms(roomID),
    startDate Date,
    endDate Date
);

create table Services(
	serviceID int primary key auto_increment,
    reservationID int,
    foreign key (reservationID) references Reservations(reservationID),
    serviceName varchar(45),
    servicePrice int
);

