 {% snapshot accounts_snapshot %}
 {{
    config(
        target = 'ANALYTICS',
        unique_key = 'account_id',
        strategy = 'check';
        check_cols = ['customer_id', 'account_type', 'currency', 'created_at']
    )
 }}
 select * from {{ref('stg_customers')}}
 {% endsnapshot %}