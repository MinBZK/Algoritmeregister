-- Organisaties die nog geen algoritmes hebben gepubliceerd, maar wel een conceptversie hebben opgeslagen. En welke conceptversie? 
-- Which algorithm_versions have never been published before?
select 
    a.name, 
    a.organization as Organisatie, 
    a.create_dt as laatst_gewijzigd 
from algoritme_version a 
join (
    -- Get latest version of algorithms
    select max(create_dt) as max_create_dt, algoritme_id 
    from algoritme_version 
    where language='NLD' 
    group by algoritme_id
) 
j on j.algoritme_id=a.algoritme_id and a.create_dt=j.max_create_dt
where a.language='NLD' 
and published=false
-- Avoid algorithm_versions that have ever been published
and not exists (
    select ax.algoritme_id from algoritme_version ax join 
    action_history ah on ah.algoritme_version_id=ax.id and ah.operation='published' 
    where ax.algoritme_id=a.algoritme_id
    group by ax.algoritme_id
)
order by organization, create_dt desc
;