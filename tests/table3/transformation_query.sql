SELECT  customer_id AS SNO,
        name,
        nvl(email,'unkwn@gmail.com') as email,
        phone
FROM [bronze].[Customer_bronze]
where customer_id > 103