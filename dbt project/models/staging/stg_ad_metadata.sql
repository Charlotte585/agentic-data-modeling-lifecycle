with source as (

    select *
    from {{ source('raw', 'ad_metadata') }}

),

renamed as (

    select
        trim(cast(ad_id as varchar)) as ad_id,
        trim(cast(ad_name as varchar)) as ad_name,
        trim(cast(campaign_id as varchar)) as campaign_id,
        trim(cast(creative_id as varchar)) as creative_id,
        trim(cast(creative_name as varchar)) as creative_name,
        lower(trim(cast(marketing_channel as varchar))) as marketing_channel,
        lower(trim(cast(ad_status as varchar))) as ad_status,
        cast(ad_version_start_timestamp at time zone 'UTC' as timestamp)
            as ad_version_start_timestamp,
        cast(ad_version_end_timestamp at time zone 'UTC' as timestamp)
            as ad_version_end_timestamp
    from source

)

select *
from renamed
