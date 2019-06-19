
-- staging table for activitie
create table stg_activity (
    ticket_id     int
  , performed_at  text
  , status        text
  , created_on_ts timestamp default CURRENT_TIMESTAMP
)
;

-- relational modelling
-- normalize text status
create table freshdesk_status (
    status_id             integer primary key -- auto incremets
  , status_desc           varchar(200) unique --this will have to be unique as matches are by name
  , complete_status_flag  boolean
  , created_on_ts         timestamp default CURRENT_TIMESTAMP
)
;

-- table for ticket data
create table freshdesk_ticket (
      ticket_id       int primary key
    , start_ts        timestamp
    , end_ts          timestamp
    , complete_flag   boolean
    , activity_count  int
    , created_on_ts timestamp default CURRENT_TIMESTAMP
)
;

--table for ticket activity
create table freshdesk_ticket_activity (
    ticket_activity_id  integer primary key
  , ticket_id           int
  , performed_at_ts     timestamp
  , status_id           int
  , created_on_ts       timestamp default CURRENT_TIMESTAMP
  , FOREIGN KEY(ticket_id) REFERENCES freshdesk_ticket(ticket_id)
  , FOREIGN KEY(status_id) REFERENCES freshdesk_status(status_id)
)
;
