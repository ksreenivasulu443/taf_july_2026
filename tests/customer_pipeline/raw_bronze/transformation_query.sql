SELECT *
FROM bronze.CustomerLanding
WHERE SourceFileName IN (
    SELECT SourceFileName
    FROM (
        SELECT TOP (1)
            SourceFileName
        FROM bronze.CustomerLanding
        GROUP BY SourceFileName
        ORDER BY MAX(InsertDate) DESC
    ) AS LatestFile
)