{% macro generate_trip_id() %}

{{ dbt_utils.generate_surrogate_key([
   'vendor_id',
   'pickup_datetime',
   'dropoff_datetime',
   'pickup_location_id',
   'dropoff_location_id',
   'fare_amount',
   'trip_distance',
   'service_type'
   ])
}}

{% endmacro %}