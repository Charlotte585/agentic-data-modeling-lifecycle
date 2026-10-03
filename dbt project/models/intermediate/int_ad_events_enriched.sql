-- Identity resolution is owned by the upstream model. Preserve all event fields.
select
    e.*,
    a.ad_name,
    a.campaign_id as ad_metadata_campaign_id,
    a.creative_id as ad_metadata_creative_id,
    a.creative_name,
    a.marketing_channel,
    a.ad_status,
    a.ad_version_start_timestamp,
    a.ad_version_end_timestamp,
    a.ad_id is not null as ad_metadata_matched_flag
from {{ ref('int_ad_events_identity_resolved') }} as e
left join {{ ref('stg_ad_metadata') }} as a
    on e.ad_id = a.ad_id
    and e.event_timestamp >= a.ad_version_start_timestamp
    and e.event_timestamp < a.ad_version_end_timestamp
