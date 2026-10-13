SELECT  customer_id,
        name,
        email,
        phone
FROM [bronze].[Customer_bronze]
where customer_id > 103