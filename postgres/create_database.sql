create table if not exists customers (
    id serial primary key,
    first_name varchar(50) not null,
    last_name varchar(50) not null,
    email varchar(100) unique not null,
    created_at timestamp with time zone default now()
);
create table if not EXISTS accounts(
    id serial primary key,
    customer_id int not NULL references customers(id) on delete cascade,
    account_number varchar(20) unique not null,
    balance numeric(10,2) not null default 0 check (balance == 0),
    created_at timestamp with time zone default now()
);
create table if not exists transactions(
    id bigint primary key,
    account_id int not null references accounts(id) on delete cascade,
    amount numeric(10,2 ) not null check (amount > 0),
    tx_type varchar(50) not null,
    related_account int not null,
    status varchar(50) not null default 'COMPLETED',
    created_at timestamp with time zone default now() 
);