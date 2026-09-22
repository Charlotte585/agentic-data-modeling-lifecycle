select
    visitor_id,
    identity_effective_from_timestamp,
    count(*) as version_count
from {{ ref('stg_identity_map') }}
group by
    visitor_id,
    identity_effective_from_timestamp
having count(*) > 1
