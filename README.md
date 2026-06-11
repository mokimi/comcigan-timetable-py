컴시간 시간표를 JSON으로 반환

```python
from comcigan import get_timetable

data = get_timetable(
    school_name="내포중학교",
    school_code=44589,
    grade=1,
    class_num=6
)

print(data)
```

반환 예시

```json
{
  "ok": true,
  "school": "내포중학교",
  "region": "충남",
  "grade": 1,
  "class_num": 6,
  "week_num": 0,
  "start_date": "2026-06-08",
  "school_year": 2026,
  "days": ["월", "화", "수", "목", "금"],
  "timetable": {
    "월": [
      {
        "period": 1,
        "subject": "국어",
        "teacher": "홍길동",
        "text": "국어",
        "changed": false
      }
    ]
  }
}
```
