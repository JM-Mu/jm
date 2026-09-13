# -*- coding: utf-8 -*-
import json, re
from collections import Counter

raw = open(r'C:\Users\27498\Doubao\chats\2026-09-13\new-chat-1\doc_dump.txt', encoding='utf-8').read().split('\n')
lines = [l.strip() for l in raw if l.strip()]

chapters = {"工业机器人","通讯","PLC","人机界面","相机"}
qtype_labels = ["选择题","填空","判断","解答题","简述题","程序题"]

# 1) 按"题号行"切块；题号行：行首 数字 + (. ， 、 : 或空格) + 内容
num_re = re.compile(r'^(\d{1,3})(?:\s*[.．、，:：]|\s{1,2})\s*(\S.*)$')
is_label = lambda s: s in chapters or s in qtype_labels

blocks = []  # each: {'ch','type','stem','rest':[lines]}
cur_ch=None; cur_tp=None
buf=None
for line in lines:
    if line in chapters:
        cur_ch=line;
        if buf: blocks.append(buf); buf=None
        continue
    if line in qtype_labels:
        if line.startswith("填空"): cur_tp="blank"
        elif line.startswith("判断"): cur_tp="judge"
        elif line.startswith("选择"): cur_tp="choice"
        elif line.startswith("简述") or line.startswith("解答"): cur_tp="essay"
        elif line.startswith("程序"): cur_tp="program"
        if buf: blocks.append(buf); buf=None
        continue
    m=num_re.match(line)
    if m:
        if buf: blocks.append(buf)
        buf={'ch':cur_ch,'tp':cur_tp,'num':m.group(1),'stem':m.group(2),'rest':[]}
    else:
        # 判断题章节里无题号的整行题（如"工业相机按..."）
        if buf is None and cur_tp=="judge" and re.search(r'[（(]\s*(X|x|×|√|对|错误|错|正确)\s*[）)]',line):
            buf={'ch':cur_ch,'tp':cur_tp,'num':'?','stem':line,'rest':[]}
        elif buf is not None:
            buf['rest'].append(line)
if buf: blocks.append(buf)

def norm(s): return re.sub(r'\s+',' ',s).strip()

questions=[]
cid=0
def nid():
    global cid; cid+=1; return f"q{cid:04d}"

opt_re=re.compile(r'^([A-D])[\.．、\s]?\s*(.+)$')

for b in blocks:
    ch,tp = b['ch'],b['tp']
    stem=b['stem']; rest=b['rest']
    # 选项与答案在rest中
    opts={}; ansline=None; other=[]
    for r in rest:
        mo=opt_re.match(r)
        if mo and not re.match(r'^\d',r) and len(r)<40:
            opts[mo.group(1)]=norm(mo.group(2)); continue
        ma=re.match(r'^(正确答案|正常答案)\s*[:：]\s*(.*)$',r)
        if ma:
            ansline=norm(ma.group(2)); continue
        other.append(r)
    # 判断题：stem或rest中带对错标记
    mjudge=re.search(r'[（(]\s*(X|x|×|√|对|正确|错误|错)\s*[）)]', stem)
    if tp=="judge" and mjudge:
        tag=mjudge.group(1)
        q=re.sub(r'[（(]\s*(X|x|×|√|对|正确|错误|错)\s*[）)]','',stem).strip()
        questions.append({"id":nid(),"chapter":ch,"type":"judge","q":norm(q),
                          "ans":"T" if tag in ("√","对","正确") else "F"})
        continue
    # 选择题：有单字母答案 + 至少2个选项
    if ansline and re.match(r'^[A-D](\b|\.|$)', ansline) and len(opts)>=2:
        am=re.search(r'[A-D]',ansline)
        questions.append({"id":nid(),"chapter":ch,"type":"choice","q":norm(stem),
                          "opts":{k:opts[k] for k in sorted(opts)},"ans":am.group(0)})
        continue
    # 填空题：有"正确答案"文本，无选项
    if ansline and len(opts)==0:
        questions.append({"id":nid(),"chapter":ch,"type":"blank","q":norm(stem),"ans":ansline})
        continue
    # 简答/程序题：stem + 后续答
    if tp in ("essay","program"):
        ans=norm(" ".join(other))
        ans=re.sub(r'^(答[：:]?|答)','',ans).strip()
        if tp=="essay" and ans:
            questions.append({"id":nid(),"chapter":ch,"type":"essay","q":norm(stem),"ans":ans})
        continue
    # 兜底：judge标记缺失但按judge
    if tp=="judge":
        questions.append({"id":nid(),"chapter":ch,"type":"judge","q":norm(stem),"ans":""})

cnt=Counter((q["chapter"],q["type"]) for q in questions)
for k in sorted(cnt): print(k,cnt[k])
print("TOTAL",len(questions))
# 异常检查
print("--- choice 缺答案 ---")
for q in questions:
    if q["type"]=="choice" and not q.get("ans"): print(" ",q["id"],q["q"][:40])
print("--- judge 缺答案 ---")
for q in questions:
    if q["type"]=="judge" and not q.get("ans"): print(" ",q["id"],q["q"][:40])

json.dump(questions, open(r'C:\Users\27498\Doubao\chats\2026-09-13\new-chat-1\questions.json','w',encoding='utf-8'),
          ensure_ascii=False, indent=1)
