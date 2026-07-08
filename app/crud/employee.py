from app.crud.base import CRUDBase
from app.models.employee import Employee

class CRUDEmployee(CRUDBase[Employee]):
    pass

employee_crud = CRUDEmployee(Employee)
