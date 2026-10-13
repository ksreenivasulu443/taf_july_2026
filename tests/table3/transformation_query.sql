SELECT  customer_id AS SNO,
        name,
        email,
        phone
FROM [bronze].[Customer_bronze]
where customer_id > 103