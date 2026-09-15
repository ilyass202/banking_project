{% snapshot customers_snapshot %}
{{
    config(
        target = 'ANALYTICS',
        unique_key = 'customer_id',
        strategy = 'check',
        check_cols = ['first_name', 'last_name', 'email', 'created_at']
    )
}}
select * from {{ref('stg_customers')}}
{% endsnapshot %}