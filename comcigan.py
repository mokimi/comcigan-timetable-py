import base64
import json
import re
from urllib import parse

import requests


COMCIGAN_HOST = "http://comci.net:4082"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_text(url, encoding="utf-8"):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.encoding = encoding
    response.raise_for_status()
    return response.text


def get_comcigan_info():
    html = get_text(f"{COMCIGAN_HOST}/st", encoding="euc-kr")

    path_matches = re.findall(r"\./([0-9]+\?[0-9]+l)", html)
    code0_matches = re.findall(r"sc_data\('([0-9]+)_", html)

    if not path_matches:
        raise RuntimeError("컴시간 API 경로를 찾지 못했습니다.")

    if not code0_matches:
        raise RuntimeError("code0를 찾지 못했습니다.")

    return {
        "comcigan_string": "/" + path_matches[0],
        "code0": code0_matches[0],
    }


def search_school(keyword, comcigan_string=None):
    if comcigan_string is None:
        comcigan_string = get_comcigan_info()["comcigan_string"]

    encoded = parse.quote(keyword, encoding="euc-kr")
    url = f"{COMCIGAN_HOST}{comcigan_string}{encoded}"

    text = get_text(url, encoding="utf-8").strip("\x00")
    data = json.loads(text)

    schools = []

    for school in data.get("학교검색", []):
        schools.append({
            "region_code": school[0],
            "region": school[1],
            "school_name": school[2],
            "school_code": school[3],
        })

    return schools


def fetch_raw_timetable(info, school_code, week_num=0):
    payload = f"{info['code0']}_{school_code}_0_{week_num + 1}"
    encoded = base64.b64encode(payload.encode("utf-8")).decode("utf-8")

    base_path = info["comcigan_string"].split("?")[0]
    url = f"{COMCIGAN_HOST}{base_path}?{encoded}"

    text = get_text(url, encoding="utf-8")

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise RuntimeError("JSON 응답을 찾지 못했습니다.")

    return json.loads(text[start:end + 1])


def decode_code(code, subjects, teachers):
    changed = False

    if isinstance(code, str):
        if code.startswith(">"):
            changed = True
            code = code[1:]

        if not code.isdigit():
            return None

        code = int(code)

    if not code:
        return None

    subject_index = code // 1000
    teacher_index = code % 100

    subject = subjects[subject_index]
    teacher = teachers[teacher_index]

    return {
        "period": "",
        "subject": subject,
        "teacher": teacher,
        "text": subject,
        "changed": changed,
    }


def get_timetable(
    grade,
    class_num,
    school_name=None,
    school_code=None,
    week_num=0,
):
    if school_name is None and school_code is None:
        raise ValueError("school_name 또는 school_code 중 하나는 필요합니다.")

    info = get_comcigan_info()
    region = ""

    if school_code is None:
        schools = search_school(school_name, info["comcigan_string"])

        if not schools:
            raise ValueError("학교를 찾을 수 없습니다.")

        school = schools[0]
        region = school["region"]
        school_name = school["school_name"]
        school_code = school["school_code"]

    raw = fetch_raw_timetable(
        info=info,
        school_code=school_code,
        week_num=week_num,
    )

    if "자료446" not in raw or "자료492" not in raw or "자료147" not in raw:
        raise RuntimeError(f"시간표 데이터를 찾지 못했습니다. 응답 키: {list(raw.keys())}")

    teachers = raw["자료446"]
    subjects = raw["자료492"]
    table = raw["자료147"]

    class_data = table[grade][class_num]

    days = ["월", "화", "수", "목", "금"]
    timetable = {}

    for day_name, day_data in zip(days, class_data[1:]):
        periods = []

        if isinstance(day_data, list):
            for period_index, code in enumerate(day_data[1:], start=1):
                item = decode_code(code, subjects, teachers)

                if item:
                    item["period"] = period_index
                    periods.append(item)

        timetable[day_name] = periods

    return {
        "ok": True,
        "school": school_name,
        "school_code": school_code,
        "region": region,
        "grade": grade,
        "class_num": class_num,
        "week_num": week_num,
        "start_date": raw.get("시작일"),
        "school_year": raw.get("학년도"),
        "timetable": timetable,
    }


if __name__ == "__main__":
    data = get_timetable(
        school_name="내포중학교",
        grade=1,
        class_num=6,
    )

    print(json.dumps(data, ensure_ascii=False, indent=2))
