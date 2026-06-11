# comcigan-timetable-py

컴시간 시간표를 JSON으로 반환합니다.

## get_school_code

학교명을 이용해 학교 정보를 조회합니다.

```python
from comcigan import get_school_code

print(get_school_code("내포중학교"))
```

반환 예시

```json
[
  {
    "region_code": 24966,
    "region": "충남",
    "school_name": "내포중학교",
    "school_code": 44589
  }
]
```

## get_timetable

학교명 또는 학교코드를 이용해 시간표를 조회합니다.

```python
data = get_timetable(
    school_name="내포중학교",
    grade=1,
    class_num=6
)

print(data)
```

또는

```python
data = get_timetable(
    school_code=44589,
    grade=1,
    class_num=6
)

print(data)
```

반환 구조

```json
{
  "ok": true,
  "school": "내포중학교",
  "school_code": 44589,
  "region": "충남",
  "grade": 1,
  "class_num": 6,
  "week_num": 0,
  "start_date": "2026-06-08",
  "school_year": 2026,
  "timetable": {
    "월": [
      {
        "period": 1,
        "subject": "체육",
        "teacher": "유덕*",
        "text": "체육",
        "changed": false
      }
    ],
    "화": [...],
    "수": [...],
    "목": [...],
    "금": [...]
  }
}
```
