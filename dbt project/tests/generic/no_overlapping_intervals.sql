{% test no_overlapping_intervals(model, entity_column, start_column, end_column) %}

with ordered_versions as (
    select
        {{ entity_column }} as entity_id,
        {{ start_column }} as version_start,
        {{ end_column }} as version_end,
        max({{ end_column }}) over (
            partition by {{ entity_column }}
            order by {{ start_column }}, {{ end_column }}
            rows between unbounded preceding and 1 preceding
        ) as prior_max_end
    from {{ model }}
)

select *
from ordered_versions
where version_start < prior_max_end

{% endtest %}
