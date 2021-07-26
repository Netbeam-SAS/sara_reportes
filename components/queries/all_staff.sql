select CONCAT(firstname,' ',lastname) as staff
from ost_staff
WHERE dept_id <> 8
ORDER BY dept_id DESC, staff