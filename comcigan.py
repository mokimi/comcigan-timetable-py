import base64
import json
import re
from urllib import parse

import requests


COMCIGAN_HOST = "http://comci.net:4082"

SCHOOL_NAME = "내포중학교"
SCHOOL_CODE = 44589
GRADE = 1
CLASS_NUM = 6
WEEK_NUM = 0

REGION = "충남"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


class ComciganError(Exception):
    pass


def get_text(url, encoding="utf-8"):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.encoding = encoding
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise ComciganError(f"요청 실패: {e}") from e


def get_comcigan_info():
    html = get_text(f"{COMCIGAN_HOST}/st", encoding="euc-kr")

    path_matches = re.findall(r"\./([0-9]+\?[0-9]+l)", html)
    code0_matches = re.findall(r"sc_data\('([0-9]+)_", html)

    if not path_matches:
        raise ComciganError("컴시간 API 경로를 찾지 못했습니다.")

    if not code0_matches:
        raise ComciganError("code0를 찾지 못했습니다.")

    return {
        "comcigan_string": "/" + path_matches[0],
        "code0": code0_matches[0],
    }


def search_school(keyword, comcigan_string):
    encoded = parse.quote(keyword, encoding="euc-kr")
    url = f"{COMCIGAN_HOST}{comcigan_string}{encoded}"

    text = get_text(url, encoding="utf-8").strip("\x00")

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ComciganError("학교 검색 응답 JSON 파싱 실패") from e

    return data.get("학교검색", [])


def fetch_raw_timetable(info, week_num=0):
    payload = f"{info['code0']}_{SCHOOL_CODE}_0_{week_num + 1}"
    encoded = base64.b64encode(payload.encode("utf-8")).decode("utf-8")

    base_path = info["comcigan_string"].split("?")[0]
    url = f"{COMCIGAN_HOST}{base_path}?{encoded}"

    text = get_text(url, encoding="utf-8")

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ComciganError("JSON 응답을 찾지 못했습니다.")

    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError as e:
        raise ComciganError("시간표 응답 JSON 파싱 실패") from e


def decode_code(code, subjects, teachers):
    changed = False

    if isinstance(code, str):
        if code.startswith(">"):
            changed = True
            code = code[1:]

        if not code.isdigit():
            return empty_period(changed)

        code = int(code)

    if not code:
        return empty_period(changed)

    subject_index = code // 1000
    teacher_index = code % 100

    subject = subjects[subject_index] if 0 <= subject_index < len(subjects) else f"과목#{subject_index}"
    teacher = teachers[teacher_index] if 0 <= teacher_index < len(teachers) else f"교사#{teacher_index}"

    return {
        "period": "",
        "subject": subject,
        "teacher": teacher,
        "text": subject,
        "changed": changed,
    }


def empty_period(changed=False):
    return {
        "period": "",
        "subject": "",
        "teacher": "",
        "text": "",
        "changed": changed,
    }


def get_timetable(week_num=0):
    info = get_comcigan_info()
    raw = fetch_raw_timetable(info, week_num=week_num)

    try:
        teachers = raw["자료446"]
        subjects = raw["자료492"]
        table = raw["자료147"]
        class_data = table[GRADE][CLASS_NUM]
    except KeyError as e:
        raise ComciganError(f"필수 데이터가 없습니다: {e}") from e
    except IndexError as e:
        raise ComciganError("학년/반 시간표 데이터를 찾지 못했습니다.") from e

    days = ["월", "화", "수", "목", "금"]
    result = {}

    for day_name, day_data in zip(days, class_data[1:]):
        periods = []

        if isinstance(day_data, list):
            for period_index, code in enumerate(day_data[1:], start=1):
                item = decode_code(code, subjects, teachers)
                item["period"] = period_index
                periods.append(item)

        result[day_name] = periods

    return {
        "ok": True,
        "school": SCHOOL_NAME,
        "region": REGION,
        "grade": GRADE,
        "class_num": CLASS_NUM,
        "week_num": week_num,
        "start_date": raw.get("시작일", ""),
        "school_year": raw.get("학년도", ""),
        "days": days,
        "timetable": result,
    }


if __name__ == "__main__":
    try:
        timetable = get_timetable(WEEK_NUM)
        print(json.dumps(timetable, ensure_ascii=False, indent=2))
    except ComciganError as e:
        print(json.dumps({
            "ok": False,
            "error": str(e),
        }, ensure_ascii=False, indent=2))
