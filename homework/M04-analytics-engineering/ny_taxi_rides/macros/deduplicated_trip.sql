{% macro deduplicate_trips(relation, pk_column) %}

with ranked as (
    select
        *,
        row_number() over (partition by {{ pk_column }} order by pickup_datetime desc) as rn
    from {{ relation }}
)

select *
from ranked
where rn = 1

{% endmacro %}
