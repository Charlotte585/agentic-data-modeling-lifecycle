select *
from {{ ref('stg_identity_map') }}
where (
    identity_type = 'anonymous'
    and (
        customer_id is not null
        or account_id is not null
        or account_status is not null
    )
)
or (
    identity_type in ('verified', 'verified_customer')
    and (
        customer_id is null
        or account_id is null
    )
)
