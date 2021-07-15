SELECT 
ost_thread_event.`timestamp`,
CONCAT(ost_staff.firstname, ' ', ost_staff.lastname) as username,
ost_thread_event.staff_id,
ost_event.`name` as 'event',
ost_department.name as dept,
pdept_t.pdept
FROM ost_thread_event 
INNER JOIN ost_event ON ost_event.id = ost_thread_event.event_id
INNER JOIN ost_department ON ost_department.id = ost_thread_event.dept_id
INNER JOIN (SELECT A.pid, B.`name` AS pdept FROM (SELECT pid FROM ost_department) A
INNER JOIN ost_department B ON A.pid = B.id GROUP BY pid) pdept_t ON ost_department.pid = pdept_t.pid
-- INNER JOIN ost_staff ON ost_staff.staff_id = ost_thread_event.uid
INNER JOIN ost_staff ON ost_staff.staff_id = ost_thread_event.staff_id
where thread_id = {} ORDER BY TIMESTAMP ASC