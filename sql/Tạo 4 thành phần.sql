USE taxi_homework;

CREATE TABLE vendors (
    vendor_id INT PRIMARY KEY
) ENGINE=InnoDB;


CREATE TABLE payment_types (
    payment_type_id INT PRIMARY KEY
) ENGINE=InnoDB;


CREATE TABLE rate_codes (
    rate_code_id INT PRIMARY KEY
) ENGINE=INNODB;
CREATE TABLE trips (
    trip_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    vendor_id INT NULL,
    pickup_datetime DATETIME NULL,
    dropoff_datetime DATETIME NULL,

    passenger_count INT NULL,
    trip_distance DECIMAL(10,2) NULL,

    ratecode_id INT NULL,
    store_and_fwd_flag VARCHAR(1) NULL,

    pickup_location_id INT NULL,
    dropoff_location_id INT NULL,

    payment_type INT NULL,

    fare_amount DECIMAL(12,2) NULL,
    extra DECIMAL(12,2) NULL,
    mta_tax DECIMAL(12,2) NULL,
    tip_amount DECIMAL(12,2) NULL,
    tolls_amount DECIMAL(12,2) NULL,
    improvement_surcharge DECIMAL(12,2) NULL,
    total_amount DECIMAL(12,2) NULL,
    congestion_surcharge DECIMAL(12,2) NULL,
    airport_fee DECIMAL(12,2) NULL,

    CONSTRAINT fk_trips_vendor
        FOREIGN KEY (vendor_id)
        REFERENCES vendors(vendor_id),

    CONSTRAINT fk_trips_payment
        FOREIGN KEY (payment_type)
        REFERENCES payment_types(payment_type_id),

    CONSTRAINT fk_trips_ratecode
        FOREIGN KEY (ratecode_id)
        REFERENCES rate_codes(rate_code_id)

) ENGINE=InnoDB;