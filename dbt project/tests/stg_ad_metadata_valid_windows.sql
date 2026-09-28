select *
from {{ ref('stg_ad_metadata') }}
where ad_version_start_timestamp is null
   or ad_version_end_timestamp is null
   or ad_version_start_timestamp >= ad_version_end_timestamp
