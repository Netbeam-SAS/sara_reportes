SELECT 
C.field_id, 
C.value 
FROM 
ost_form_entry A 
INNER JOIN ost_ticket B ON A.object_id = B.ticket_id 
INNER JOIN (SELECT * from ost_form_entry_values) C on A.id = C.entry_id 
WHERE A.object_type = "T" AND A.object_id = {}