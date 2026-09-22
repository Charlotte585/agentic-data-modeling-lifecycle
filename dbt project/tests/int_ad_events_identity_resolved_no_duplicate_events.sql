select
    event_id,
    count(*) as event_count
from {{ ref('int_ad_events_identity_resolved') }}
group by event_id
having count(*) > 1
