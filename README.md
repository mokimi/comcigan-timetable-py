# Comcigan Timetable Parser

컴시간 알리미 웹 데이터를 이용해 특정 학교/학년/반의 시간표를 JSON 형태로 가져오는 파이썬 코드입니다.

## 기능

* 학교 시간표 조회
* 요일별 시간표 정리
* 과목명, 교사명 추출
* 변경된 수업 여부 표시
* JSON 형태 출력

## 설치

```bash
pip install -r requirements.txt
```

## 실행

```bash
python comcigan.py
```

## 출력 예시

```json
{
  "ok": true,
  "school": "내포중학교",
  "region": "충남",
  "grade": 1,
  "class_num": 6,
  "week_num": 0,
  "days": ["월", "화", "수", "목", "금"],
  "timetable": {
    "월": [
      {
        "period": 1,
        "subject": "국어",
        "teacher": "교사명",
        "text": "국어",
        "changed": false
      }
    ]
  }
}
```

## 설정값

코드 상단에서 아래 값을 수정할 수 있습니다.

```python
SCHOOL_NAME = "내포중학교"
SCHOOL_CODE = 44589
GRADE = 1
CLASS_NUM = 6
WEEK_NUM = 0
```

## 주의사항

이 코드는 컴시간 알리미 웹 응답 구조를 파싱하는 방식입니다.
컴시간 사이트 구조가 변경되면 정상 동작하지 않을 수 있습니다.

또한 학교명, 학교코드, 학년, 반 정보는 개인이나 학급을 추정할 수 있는 정보가 될 수 있으므로 공개 저장소에 올릴 때 주의가 필요합니다.

## 라이선스

개인 학습 및 프로젝트 용도로 자유롭게 사용할 수 있습니다.
