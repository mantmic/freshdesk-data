/*
    This would ordinarily be a stored procedure / plsql function. SQLite does not support those, and it may be out of scope for a small excerise

    This is a script to populate schema from data in staging table
*/

-- delete existing data
delete from freshdesk_ticket_activity ;
delete from freshdesk_ticket ;
delete from freshdesk_status ;

-- normalize status
insert into freshdesk_status (
    status_desc
  , complete_status_flag
)
select distinct
    cast ( status as varchar(200) ) as status_desc
  , case when status in ( 'Closed', 'Resolved' ) then True
         else False
    end as complete_status_flag
from
  stg_activity
;


-- this query will be repeated for ticket activity, ideally a temporary table could be used to only perform this join once
-- normalize ticket
with ta as
( select
    a.ticket_id
  , s.complete_status_flag
  , datetime ( a.performed_at ) as performed_at_ts
from
  stg_activity a
  join
  freshdesk_status s
    on a.status = s.status_desc
)
insert into freshdesk_ticket (
      ticket_id
    , start_ts
    , end_ts
    , complete_flag
    , activity_count
)
select
    t.ticket_id
  , t.start_ts
  , te.end_ts
  , case when te.end_ts is not null then True
         else False
    end as complete_flag
  , t.activity_count
from
  ( select
        ta.ticket_id
      , min ( ta.performed_at_ts )  as start_ts
      , count ( * )                 as activity_count
    from
      ta
    group by
      ta.ticket_id
  ) t
  left outer join
  ( select
        ta.ticket_id
      , max ( ta.performed_at_ts ) as end_ts
    from
      ta
    where
      ta.complete_status_flag = True
    group by
      ta.ticket_id
  ) te
    on t.ticket_id = te.ticket_id
;

-- insert ticket activity
insert into freshdesk_ticket_activity (
    ticket_id
  , performed_at_ts
  , status_id
)
select
    a.ticket_id
  , datetime ( a.performed_at ) as performed_at_ts
  , s.status_id
from
  stg_activity a
  join
  freshdesk_status s
    on a.status = s.status_desc
;
