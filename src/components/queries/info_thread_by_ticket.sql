SELECT 
ost_thread_event.`timestamp`,
ost_thread_event.username,
ost_thread_event.staff_id,
ost_event.`name` as 'event',
ost_department.name as dept,
pdept_t.pdept
FROM ost_thread_event 
INNER JOIN ost_event ON ost_event.id = ost_thread_event.event_id
INNER JOIN ost_department ON ost_department.id = ost_thread_event.dept_id
INNER JOIN (SELECT A.pid, B.`name` AS pdept FROM (SELECT pid FROM ost_department) A
INNER JOIN ost_department B ON A.pid = B.id GROUP BY pid) pdept_t ON ost_department.pid = pdept_t.pid
where thread_id = {} ORDER BY TIMESTAMP ASC