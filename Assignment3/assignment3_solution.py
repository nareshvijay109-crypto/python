"""
SIMATS Online Programming Lab - Python Programming
Assignment 3: Lists, Tuples, Dictionaries, Sets and Nested Data
Student: Naresh Vijay R | Register No: 1972260060D
Python 3.10+ | Standard library only
Run: python assignment3_solution.py
Q6 and Q7 are model solutions inferred from the available titles/context.
"""
from collections import defaultdict
import re

def moving_average_naive(values, window=7):
    if window <= 0: raise ValueError("window must be positive")
    return [sum(values[i:i+window])/window for i in range(len(values)-window+1)]

def moving_average_running(values, window=7):
    if window <= 0: raise ValueError("window must be positive")
    if len(values) < window: return []
    total=sum(values[:window]); result=[total/window]
    for i in range(window,len(values)):
        total += values[i]-values[i-window]
        result.append(total/window)
    return result

def rainfall_report(readings):
    weeks=[sum(readings[i:i+7]) for i in range(0,len(readings),7)]
    return {"weekly_totals":weeks,
            "wettest_week_index":weeks.index(max(weeks)) if weeks else None,
            "driest_week_index":weeks.index(min(weeks)) if weeks else None,
            "moving_average":moving_average_running(readings),
            "dry_day_indices":[i for i,x in enumerate(readings) if x==0]}

def correct_grid(rows,cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]

def tuple_key_demo():
    stops={(13.0827,80.2707):"Chennai Central",(13.0418,80.2341):"T. Nagar"}
    return stops[(13.0418,80.2341)]

def frequencies(texts,stop):
    counts={}
    for text in texts:
        for word in re.findall(r"[a-zA-Z]+",text.lower()):
            if word not in stop: counts[word]=counts.get(word,0)+1
    return counts

def top(counts,k):
    return sorted(counts.items(),key=lambda p:(-p[1],p[0]))[:k]

def group_by_district(records):
    grouped=defaultdict(list)
    for district,crop,complaint in records:
        grouped[district].append({"crop":crop,"complaint":complaint})
    return dict(grouped)

def elective_report(ai,iot,all_students):
    return sorted(ai & iot),sorted(ai ^ iot),sorted(all_students-(ai|iot))

def clean_loop(readings):
    c=[]; f=[]
    for x in readings:
        if -50<=x<=50: c.append(x); f.append(x*9/5+32)
    alarms=[i for i,x in enumerate(readings) if -50<=x<=50 and not 2<=x<=8]
    return c,f,alarms

def clean_comprehension(readings):
    c=[x for x in readings if -50<=x<=50]
    f=[x*9/5+32 for x in readings if -50<=x<=50]
    alarms=[i for i,x in enumerate(readings) if -50<=x<=50 and not 2<=x<=8]
    return c,f,alarms

def clean_map_filter(readings):
    c=list(filter(lambda x:-50<=x<=50,readings))
    f=list(map(lambda x:x*9/5+32,c))
    alarms=[i for i,x in enumerate(readings) if -50<=x<=50 and not 2<=x<=8]
    return c,f,alarms

# Q6 model solution: nested timetable structure.
TIMETABLE={
 "12675":{"name":"Chennai Egmore - Coimbatore Intercity",
          "stops":[("Chennai Egmore","06:00","06:05"),("Katpadi","08:00","08:02"),
                   ("Salem","10:30","10:32"),("Coimbatore","12:45","12:45")],
          "running_days":{"Mon","Tue","Wed","Thu","Fri","Sat"}}
}
def find_train(number): return TIMETABLE.get(str(number))
def trains_on(day):
    return [n for n,d in TIMETABLE.items() if day.title() in d["running_days"]]
def station_matches(station):
    result=[]
    for number,data in TIMETABLE.items():
        for name,arrival,departure in data["stops"]:
            if name.lower()==station.lower():
                result.append((number,data["name"],arrival,departure))
    return result

# Q7 model solution: match normalized phone or case-insensitive email.
def normalize_phone(phone):
    digits=re.sub(r"\\D","",phone or "")
    return digits[2:] if len(digits)==12 and digits.startswith("91") else digits
def merge_contacts(*groups):
    merged=[]; phone_index={}; email_index={}
    for group in groups:
        for c in group:
            item={k:(c.get(k) or "").strip() for k in ("name","phone","email")}
            phone=normalize_phone(item["phone"]); email=item["email"].lower()
            idx=phone_index.get(phone) if phone else None
            if idx is None and email: idx=email_index.get(email)
            if idx is None:
                idx=len(merged); merged.append(item)
            else:
                for key in ("name","phone","email"):
                    if not merged[idx].get(key) and item.get(key): merged[idx][key]=item[key]
            p=normalize_phone(merged[idx]["phone"]); e=merged[idx]["email"].lower()
            if p: phone_index[p]=idx
            if e: email_index[e]=idx
    return sorted(merged,key=lambda x:x["name"].lower())

if __name__=="__main__":
    print("Q1 running average:",moving_average_running([1,2,3,4,5,6,7,8]))
    print("Q2 grid:",correct_grid(3,4))
    calls=["seeds not received seeds delayed","fertiliser price high","seeds price high subsidy not received"]
    print("Q3 top:",top(frequencies(calls,{"not","high"}),3))
    ai={"192311001","192311004","192311007","192311009"}
    iot={"192311002","192311004","192311009","192311010"}
    universe={f"1923110{i:02d}" for i in range(1,11)}
    print("Q4:",elective_report(ai,iot,universe))
    print("Q5:",clean_comprehension([4,9,52,-55,7,1]))
    print("Q6:",find_train("12675"))
    print("Q7:",merge_contacts(
      [{"name":"Arun","phone":"+91 98765 43210","email":"arun@mail.com"}],
      [{"name":"Arun Kumar","phone":"9876543210","email":""}]))
