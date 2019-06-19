with activity_ranked as
( select
    ta.ticket_id
  , s.status_desc
  , ta.performed_at_ts
  , row_number() over ( partition by ta.ticket_id order by ta.performed_at_ts ) as activity_rank
  --, row_number() over ( partition by ta.ticket_id, s.status_desc order by ta.performed_at_ts ) as activity_status_rank
from
  freshdesk_ticket_activity ta
  join
  freshdesk_status s
    on ta.status_id = s.status_id
)
select
    ticket_id
  , time_spent_open
  , time_spent_waiting_on_customer
  , time_spent_waiting_for_response
  , (julianday(end_ts) - julianday(start_ts))*1440            as time_to_resolution
  , (julianday(first_response_ts) - julianday(start_ts))*1440 as time_to_first_response
from
  ( select
      t.ticket_id
    , t.start_ts
    , t.end_ts
    , min ( a.next_activity_ts )                                                              as first_response_ts
    , sum ( case when a.status_desc = 'Open' then next_activity_minutes end )                 as time_spent_open
    , sum ( case when a.status_desc = 'Waiting On Customer' then next_activity_minutes end )  as time_spent_waiting_on_customer
    , sum ( case when a.status_desc = 'Pending' then next_activity_minutes end )              as time_spent_waiting_for_response
  from
    freshdesk_ticket t
    join
    ( select
        ar.ticket_id
      , ar.status_desc
      , ar.activity_rank
      , ar.activity_status_rank
      , ar.performed_at_ts
      , ar2.performed_at_ts                                                           as next_activity_ts
      , case when ar2.performed_at_ts is not null then
             (julianday(ar2.performed_at_ts) - julianday(ar.performed_at_ts))*1440
        end                                                                           as next_activity_minutes
    from
      activity_ranked ar
      left outer join
      activity_ranked ar2
        on ar.ticket_id = ar2.ticket_id
        and ar.activity_rank = ar2.activity_rank - 1
    ) a
      on t.ticket_id = a.ticket_id
  group by
      t.ticket_id
    , t.start_ts
    , t.end_ts
  ) q
;
