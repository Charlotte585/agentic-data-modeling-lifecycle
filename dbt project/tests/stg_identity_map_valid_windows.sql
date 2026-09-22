select *
from {{ ref('stg_identity_map') }}
where identity_effective_from_timestamp is null
    or identity_effective_to_timestamp is null
    or identity_effective_from_timestamp >= identity_effective_to_timestamp
