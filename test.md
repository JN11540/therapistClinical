# 修復：刪除個案時 ForeignKeyViolationError

## 問題
刪除 patient 時出現：
```
ForeignKeyViolationError: update or delete on table "patient" violates foreign key constraint
"treatment_patient_id_fkey" on table "treatment"
```

原因：`service/patient.py` 的 `delete` 方法直接刪除 patient，
但 treatment 表有 `patient_id` 外鍵指向 patient，導致違反約束。

## 刪除順序（依賴鏈）
```
patient
  └─ treatment          (FK: patient_id → patient)
       ├─ treatment_content  (FK: treatment_id → treatment)
       └─ treatment_result   (FK: treatment_id → treatment)
```

必須先刪子表再刪父表：
1. treatment_result（依 treatment_id）
2. treatment_content（依 treatment_id）
3. treatment（依 patient_id）
4. patient

## 修改內容

### `webServer/service/patient.py`

1. 新增 import：
```python
from crud.treatment import CRUDTreatment
from crud.treatment_content import CRUDTreatmentContent
from crud.treatment_result import CRUDTreatmentResult
```

2. `__init__` 加入：
```python
self.crud_treatment = CRUDTreatment()
self.crud_content = CRUDTreatmentContent()
self.crud_result = CRUDTreatmentResult()
```

3. 修改 `delete` 方法：
```python
async def delete(self, session: AsyncSession, patient_id: int):
    try:
        db_obj = await self.crud_patient.get(session, id=patient_id)
        if db_obj is None:
            return await HttpResponseMethod.not_found(
                message=f"Patient {patient_id} not found"
            )
        treatments = await self.crud_treatment.get_multi(session, patient_id=patient_id)
        for t in treatments:
            await self.crud_result.delete_by_treatment_id(session, t.id)
            await self.crud_content.delete_by_treatment_id(session, t.id)
            await self.crud_treatment.delete(session, db_obj=t)
        await self.crud_patient.delete(session, db_obj=db_obj)
        return await HttpResponseMethod.ok(
            message=f"Patient {patient_id} deleted successfully",
        )
    except Exception as e:
        return await HttpResponseMethod.internal_server_error(message=str(e))
```
