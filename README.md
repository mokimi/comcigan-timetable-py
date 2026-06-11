컴시간 시간표를 JSON으로 반환합니다.

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
  "region": "",
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
        "subject": "체육",
        "teacher": "유덕*",
        "text": "체육",
        "changed": false
      },
      {
        "period": 2,
        "subject": "도덕B",
        "teacher": "서민*",
        "text": "도덕B",
        "changed": true
      },
      {
        "period": 3,
        "subject": "정보",
        "teacher": "지영*",
        "text": "정보",
        "changed": false
      },
      {
        "period": 4,
        "subject": "정보",
        "teacher": "지영*",
        "text": "정보",
        "changed": false
      },
      {
        "period": 5,
        "subject": "과학",
        "teacher": "김송*",
        "text": "과학",
        "changed": false
      },
      {
        "period": 6,
        "subject": "영어B",
        "teacher": "이지*",
        "text": "영어B",
        "changed": true
      },
      {
        "period": 7,
        "subject": "국어A",
        "teacher": "노가*",
        "text": "국어A",
        "changed": false
      }
    ],
    "화": [
      {
        "period": 1,
        "subject": "미술",
        "teacher": "박서*",
        "text": "미술",
        "changed": false
      },
      {
        "period": 2,
        "subject": "수학",
        "teacher": "정광*",
        "text": "수학",
        "changed": false
      },
      {
        "period": 3,
        "subject": "스포츠",
        "teacher": "박서*",
        "text": "스포츠",
        "changed": false
      },
      {
        "period": 4,
        "subject": "기가",
        "teacher": "강수*",
        "text": "기가",
        "changed": false
      },
      {
        "period": 5,
        "subject": "국어A",
        "teacher": "노가*",
        "text": "국어A",
        "changed": false
      },
      {
        "period": 6,
        "subject": "영어A",
        "teacher": "유경*",
        "text": "영어A",
        "changed": false
      },
      {
        "period": 7,
        "subject": "사회B",
        "teacher": "최계*",
        "text": "사회B",
        "changed": false
      }
    ],
    "수": [
      {
        "period": 1,
        "subject": "사회A",
        "teacher": "이서*",
        "text": "사회A",
        "changed": false
      },
      {
        "period": 2,
        "subject": "음악",
        "teacher": "김효*",
        "text": "음악",
        "changed": false
      },
      {
        "period": 3,
        "subject": "도덕A",
        "teacher": "강진*",
        "text": "도덕A",
        "changed": true
      },
      {
        "period": 4,
        "subject": "과학",
        "teacher": "김송*",
        "text": "과학",
        "changed": true
      },
      {
        "period": 5,
        "subject": "자국어",
        "teacher": "이정*",
        "text": "자국어",
        "changed": false
      },
      {
        "period": 6,
        "subject": "자수학",
        "teacher": "정광*",
        "text": "자수학",
        "changed": false
      }
    ],
    "목": [],
    "금": [
      {
        "period": 1,
        "subject": "사회A",
        "teacher": "이서*",
        "text": "사회A",
        "changed": false
      },
      {
        "period": 2,
        "subject": "수학",
        "teacher": "정광*",
        "text": "수학",
        "changed": false
      },
      {
        "period": 3,
        "subject": "체육",
        "teacher": "유덕*",
        "text": "체육",
        "changed": true
      }
    ]
  }
}
```
