{% macro generate_trip_id() %}
    {{ dbt_utils.generate_surrogate_key([
        "pickup_datetime",
        "dropoff_datetime",
        "vendor_id",
        "rate_code_id",
        "pickup_location_id",
        "dropoff_location_id",
        "trip_distance",
        "total_amount"
        "fare_amount",
    ]) }}
{% endmacro %}
