with ad_events as (

    select *
    from {{ ref('stg_ad_events') }}

),

identity_history as (

    select
        visitor_id,
        customer_id,
        account_id,
        case
            when identity_type = 'verified' then 'verified_customer'
            else identity_type
        end as identity_type,
        account_status,
        identity_effective_from_timestamp,
        identity_effective_to_timestamp
    from {{ ref('stg_identity_map') }}

),

resolved as (

    select
        e.event_id,
        e.event_timestamp,
        e.event_type,
        e.visitor_id,
        e.campaign_id,
        e.ad_id,
        e.creative_id,
        e.placement_id,
        e.device_type,
        i.customer_id,
        i.account_id,
        i.identity_type,
        i.account_status,
        i.identity_effective_from_timestamp,
        i.identity_effective_to_timestamp,
        i.identity_effective_from_timestamp is not null
            as identity_record_matched_flag,
        coalesce(
            i.identity_type = 'verified_customer'
                and i.customer_id is not null
                and i.account_id is not null,
            false
        ) as identity_resolved_flag
    from ad_events as e
    left join identity_history as i
        on e.visitor_id = i.visitor_id
        and e.event_timestamp >= i.identity_effective_from_timestamp
        and e.event_timestamp < i.identity_effective_to_timestamp

)

select *
from resolved
