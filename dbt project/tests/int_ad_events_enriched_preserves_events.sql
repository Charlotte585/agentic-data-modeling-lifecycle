-- Compare counts per event, so missing and extra events cannot cancel out.
with input_counts as (
    select event_id, count(*) as event_count
    from {{ ref('int_ad_events_identity_resolved') }}
    group by event_id
),

output_counts as (
    select event_id, count(*) as event_count
    from {{ ref('int_ad_events_enriched') }}
    group by event_id
)

select
    coalesce(i.event_id, o.event_id) as event_id,
    i.event_count as input_count,
    o.event_count as output_count
from input_counts as i
full outer join output_counts as o on i.event_id = o.event_id
where i.event_count is null
   or o.event_count is null
   or i.event_count <> o.event_count
