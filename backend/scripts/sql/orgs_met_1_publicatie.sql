-- Organisaties die maar 1 algoritme hebben gepubliceerd. En welke algoritme hebben ze gepubliceerd?
select 
    od.name, 
    a.lars, 
    av.name
from algoritme a
join algoritme_version av on av.state='PUBLISHED' and language='NLD' and av.algoritme_id=a.id
join organisation o on o.id=a.organisation_id 
join organisation_details od on od.language='NLD' and od.organisation_id=o.id
join (
    select a.organisation_id as organisation_id 
    --select av.name, organisation_id 
    from algoritme a 
    join algoritme_version av on av.algoritme_id=a.id 
    where av.state='PUBLISHED' and av.language='NLD'
    group by a.organisation_id 
    having count(a.organisation_id)=1
    order by a.organisation_id 
) ids on ids.organisation_id=a.organisation_id
;