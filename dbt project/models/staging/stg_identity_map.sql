with source as (

    select *
    from {{ source('raw', 'identity_map') }}

),

renamed as (

    select
        trim(cast(visitor_id as varchar)) as visitor_id,
        trim(cast(customer_id as varchar)) as customer_id,
        trim(cast(account_id as varchar)) as account_id,
        lower(trim(cast(identity_type as varchar))) as identity_type,
        lower(trim(cast(account_status as varchar))) as account_status,
        cast(effective_from at time zone 'UTC' as timestamp)
            as identity_effective_from_timestamp,
        cast(effective_to at time zone 'UTC' as timestamp)
            as identity_effective_to_timestamp
    from source

)

select *
from renamed
