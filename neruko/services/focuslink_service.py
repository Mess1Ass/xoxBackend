from neruko.models.focuslink import (
    insert_folink, find_all, update_folink, delete_folink, find_by_date_and_title
)


def insert_focuslink(date, title, links):
    exist = find_by_date_and_title(date, title)
    if exist:
        return {"error": "已存在相同时间以及相同地点的记录"}, 400
    try:
        res = insert_folink(date, title, links), 200
        return res
    except Exception as e:
        return {"error": str(e)}, 500
    
def find_all_data():
    try:
        res = find_all(), 200
        return res
    except Exception as e:
        return {"error": str(e)}, 500
    
def update_focuslink(_id, date, title, links):
    exist = find_by_date_and_title(date, title)
    if not exist:
        return {"error": "不存在该记录，请刷新页面"}, 400
    try:
        res = update_folink(_id, date, title, links), 200
        return res
    except Exception as e:
        return {"error": str(e)}, 500
    
def delete_focuslink(_id):
    try:
        res = delete_folink(_id), 200
        return res
    except Exception as e:
        return {"error": str(e)}, 500