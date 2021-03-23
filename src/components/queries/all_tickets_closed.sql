SELECT 
ticket_id,
number,
ost_department.`name` as dept,
ost_ticket.created,
est_duedate,
ost_ticket.closed,
ost_thread.id as thread_id
FROM ost_ticket
INNER JOIN ost_thread ON ost_thread.object_id = ost_ticket.ticket_id
LEFT JOIN ost_sla ON ost_sla.id = ost_ticket.sla_id
INNER JOIN ost_department ON ost_ticket.dept_id = ost_department.id 
WHERE status_id = 3 and YEAR(NOW()) = YEAR(ost_ticket.created) and MONTH(NOW()) = MONTH(ost_ticket.created)
-- WHERE status_id = 3 and YEAR(NOW()) = YEAR(ost_ticket.created)
-- WHERE status_id = 3
ORDER BY number DESC
LIMIT 5