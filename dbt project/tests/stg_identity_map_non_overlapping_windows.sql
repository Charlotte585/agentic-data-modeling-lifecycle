with ordered_identity_history as (

    select
        visitor_id,
        identity_effective_from_timestamp,
        identity_effective_to_timestamp,
        lag(identity_effective_to_timestamp) over (
            partition by visitor_id
            order by identity_effective_from_timestamp
        ) as prior_identity_effective_to_timestamp
    from {{ ref('stg_identity_map') }}

)

select *
from ordered_identity_history
where identity_effective_from_timestamp < prior_identity_effective_to_timestamp
