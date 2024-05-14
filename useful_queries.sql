-- SELECT name, setCode, CAST(number as INTEGER) FROM cards WHERE number NOT LIKE '%★%' OR NOT NULL AND setCode="10E";
SELECT DISTINCT row_number() over (order by '') as "#", name, number, setCode, type, rarity FROM cards WHERE printf("%d", number) = number;

-- SELECT COUNT(DISTINCT number, setCode) as distinct_cols FROM cards;
-- SELECT TOTAL(number) + TOTAL(setCode)
-- SELECT name, number, setCode FROM cards GROUP BY name ORDER BY setCode, number;
SELECT setCode, COUNT(*), MAX(CAST(number as INTEGER)) FROM cards WHERE printf("%d", number) = number GROUP BY setCode;

SELECT DISTINCT name, number FROM cards WHERE setCode="AJMP";
SELECT DISTINCT rarity FROM cards;
