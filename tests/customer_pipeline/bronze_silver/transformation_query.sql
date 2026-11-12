SELECT
    CustomerID,
    UPPER(TRIM(CustomerName)) AS CustomerName,
    LOWER(TRIM(Email)) AS Email,
    LTRIM(RTRIM(PhoneNumber)) AS PhoneNumber,
    ISNULL(UPPER(City), 'UNKNOWN') AS City,
    ISNULL(UPPER(StateName), 'UNKNOWN') AS StateName,
    SourceFileName,
    InsertDate,
    HashKey
FROM bronze.CustomerLanding
where CustomerID is not null
and SourceFileName IN (
    SELECT SourceFileName
    FROM (
        SELECT TOP (1)
            SourceFileName
        FROM bronze.CustomerLanding
        GROUP BY SourceFileName
        ORDER BY MAX(InsertDate) DESC
    ) AS LatestFile
)