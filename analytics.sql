CREATE VIEW top_conditions_by_deaths AS
SELECT condition, icd10_codes, SUM(covid_19_deaths) AS total_deaths
FROM texas_covid
GROUP BY 1, 2
ORDER BY 3 DESC
LIMIT 10;

CREATE VIEW age_group_most_deaths AS
SELECT age_group,
ROUND((SUM(covid_19_deaths) * 100.0 / SUM(SUM(covid_19_deaths)) OVER ())::numeric, 2) AS pct_of_deaths
FROM texas_covid
GROUP BY 1
ORDER BY 2 DESC;

CREATE VIEW total_deaths_by_condition AS
SELECT condition_group, SUM(covid_19_deaths) AS total_deaths
FROM texas_covid
GROUP BY 1
ORDER BY 2 DESC;

CREATE VIEW condition_mention_ratio AS 
WITH death_ratio AS (
	SELECT condition, SUM(covid_19_deaths) AS total_deaths, SUM(number_of_mentions) AS number_of_mentions
	FROM texas_covid
	GROUP BY 1
	)
SELECT condition, ROUND(((dr.number_of_mentions / dr.total_deaths))::numeric, 2) AS ratio
FROM death_ratio AS dr
ORDER BY ratio DESC;