with source as (

    select *
    from {{ source('raw', 'ad_events') }}

),

renamed as (

    select
        trim(cast(event_id as varchar)) as event_id,
        cast(event_timestamp at time zone 'UTC' as timestamp) as event_timestamp,
        lower(trim(cast(raw_event_type as varchar))) as event_type,
        trim(cast(visitor_id as varchar)) as visitor_id,
        trim(cast(campaign_id as varchar)) as campaign_id,
        trim(cast(ad_id as varchar)) as ad_id,
        trim(cast(creative_id as varchar)) as creative_id,
        trim(cast(placement_id as varchar)) as placement_id,
        lower(trim(cast(device_type as varchar))) as device_type
    from source

)

select *
from renamed
