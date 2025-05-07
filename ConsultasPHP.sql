SELECT superhero.superhero_name, superpower.power_name, hero_attribute.attribute_value AS velocidad
FROM superhero
JOIN hero_attribute ON superhero.id = hero_attribute.hero_id
JOIN attribute ON hero_attribute.attribute_id = attribute.id
JOIN hero_power ON superhero.id = hero_power.hero_id
JOIN superpower ON hero_power.power_id = superpower.id
WHERE attribute.attribute_name = 'velocidad'
ORDER BY hero_attribute.attribute_value DESC
LIMIT 5;

SELECT superhero.superhero_name, GROUP_CONCAT(DISTINCT attribute.attribute_name ORDER BY attribute.attribute_name ASC) AS atributos
FROM superhero
JOIN hero_attribute ON superhero.id = hero_attribute.hero_id
JOIN attribute ON hero_attribute.attribute_id = attribute.id
GROUP BY superhero.superhero_name
ORDER BY superhero.superhero_name ASC;

FROM superpower
JOIN hero_power ON superpower.id = hero_power.power_id
GROUP BY superpower.power_name
ORDER BY frecuencia DESC
LIMIT 5;
