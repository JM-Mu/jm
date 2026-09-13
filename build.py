# -*- coding: utf-8 -*-
import json, base64

qs = json.load(open(r'C:\Users\27498\Doubao\chats\2026-09-13\new-chat-1\questions.json', encoding='utf-8'))

KEY = 0x5A
def enc(s):
    b = s.encode('utf-8')
    return base64.b64encode(bytes(x ^ KEY for x in b)).decode()

# 精简题库：只保留前端需要的字段，答案编码
out = []
for q in qs:
    item = {"id": q["id"], "ch": q["chapter"], "t": q["type"], "q": q["q"], "a": enc(q["ans"])}
    if q["type"] == "choice":
        item["o"] = q["opts"]
    out.append(item)

bank_js = "const BANK=" + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ";"

HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>机电设备安装与调试 · 答题</title>
<style>
:root{
  --bg:#f4f6fb; --card:#fff; --ink:#1f2733; --sub:#6b7686;
  --brand:#2f6fed; --brand2:#1f56c4; --ok:#16a34a; --bad:#dc2626;
  --line:#e6eaf2; --soft:#eef3ff;
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft YaHei",sans-serif;
  background:var(--bg);color:var(--ink);line-height:1.6}
.wrap{max-width:760px;margin:0 auto;padding:14px}
header.top{position:sticky;top:0;z-index:9;background:linear-gradient(135deg,#2f6fed,#1f56c4);
  color:#fff;padding:14px 16px;box-shadow:0 2px 10px rgba(31,86,196,.25)}
header.top h1{margin:0;font-size:17px;font-weight:700}
header.top .sub{font-size:12px;opacity:.85;margin-top:2px}
.btn{display:inline-block;border:none;border-radius:10px;padding:11px 16px;font-size:15px;
  cursor:pointer;background:var(--brand);color:#fff;font-weight:600;transition:.15s}
.btn:active{transform:scale(.97)}
.btn.ghost{background:#eef3ff;color:var(--brand2)}
.btn.danger{background:#fff0f0;color:var(--bad)}
.btn.big{width:100%;padding:14px;font-size:16px;margin-top:8px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin-bottom:12px}
.row{display:flex;gap:10px;align-items:center}
.muted{color:var(--sub);font-size:13px}
.chip{display:inline-block;font-size:12px;padding:2px 9px;border-radius:20px;background:var(--soft);color:var(--brand2);margin-right:6px}
.prog{height:8px;background:#e6eaf2;border-radius:6px;overflow:hidden;margin:8px 0}
.prog>i{display:block;height:100%;background:linear-gradient(90deg,#2f6fed,#38bdf8);transition:width .3s}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
@media(max-width:480px){.grid{grid-template-columns:1fr}}
.ch{border:1px solid var(--line);border-radius:12px;padding:13px;background:#fff;cursor:pointer}
.ch:hover{border-color:var(--brand)}
.ch .name{font-weight:700;font-size:15px}
.ch .meta{font-size:12px;color:var(--sub);margin-top:3px}
.opt{display:block;width:100%;text-align:left;border:1.5px solid var(--line);background:#fff;
  border-radius:11px;padding:12px 14px;margin:9px 0;font-size:15px;cursor:pointer}
.opt:hover{border-color:var(--brand)}
.opt .k{display:inline-block;width:24px;height:24px;line-height:24px;text-align:center;border-radius:50%;
  background:var(--soft);color:var(--brand2);font-weight:700;margin-right:9px;font-size:13px}
.opt.right{border-color:var(--ok);background:#eafaf0}
.opt.right .k{background:var(--ok);color:#fff}
.opt.wrong{border-color:var(--bad);background:#fdeeee}
.opt.wrong .k{background:var(--bad);color:#fff}
.opt.dim{opacity:.55}
.opt:disabled{cursor:default}
.ansbox{margin-top:12px;border-radius:11px;padding:12px 14px;font-size:14px;display:none}
.ansbox.show{display:block}
.ansbox.ok{background:#eafaf0;color:#11663a}
.ansbox.no{background:#fdeeee;color:#991b1b}
.ansbox.ref{background:#f1f5ff;color:#23406e;border:1px dashed #b9cdf5}
input[type=text]{width:100%;padding:12px 14px;font-size:16px;border:1.5px solid var(--line);
  border-radius:11px;outline:none}
input[type=text]:focus{border-color:var(--brand)}
label.f{display:block;font-size:13px;color:var(--sub);margin:12px 0 4px}
.switch{display:flex;justify-content:space-between;align-items:center;padding:11px 0;border-bottom:1px dashed var(--line)}
.hidden{display:none!important}
.qmeta{font-size:12px;color:var(--sub)}
.qtext{font-size:17px;font-weight:600;margin:10px 0 4px;white-space:pre-wrap}
.pill{font-size:12px;padding:2px 8px;border-radius:6px;background:#eef3ff;color:var(--brand2)}
.pill.err{background:#fdeeee;color:var(--bad)}
.pill.done{background:#eafaf0;color:var(--ok)}
nav.qnav{display:flex;gap:8px;margin-top:14px}
nav.qnav .btn{flex:1}
.stat{display:flex;gap:10px;text-align:center;margin:6px 0 14px}
.stat>div{flex:1;background:#fff;border:1px solid var(--line);border-radius:12px;padding:10px}
.stat b{display:block;font-size:20px;color:var(--brand2)}
.stat span{font-size:12px;color:var(--sub)}
.list-item{display:flex;justify-content:space-between;align-items:center;padding:11px 4px;border-bottom:1px solid var(--line);cursor:pointer}
.list-item:hover{background:#f7f9ff}
.tag{font-size:11px;padding:1px 7px;border-radius:5px;background:#eef3ff;color:var(--brand2)}
.toast{position:fixed;left:50%;bottom:30px;transform:translateX(-50%);background:#222;color:#fff;
  padding:10px 18px;border-radius:22px;font-size:14px;opacity:0;transition:.25s;z-index:99;pointer-events:none}
.toast.show{opacity:.95}
</style>
</head>
<body>
<header class="top">
  <h1 id="hdTitle">机电设备 · 答题</h1>
  <div class="sub" id="hdSub">记住错题，跨设备同步</div>
</header>
<div class="wrap">

  <!-- 首页 -->
  <section id="v-home">
    <div class="card">
      <div class="row" style="justify-content:space-between">
        <b>我的总进度</b><span class="muted" id="pct"></span>
      </div>
      <div class="prog"><i id="pbar" style="width:0%"></i></div>
      <div class="stat">
        <div><b id="stDone">0</b><span>已做</span></div>
        <div><b id="stRight">0</b><span>答对</span></div>
        <div><b id="stWrong">0</b><span>错题</span></div>
      </div>
    </div>

    <div class="card">
      <div class="muted" style="margin-bottom:8px">按章节练习</div>
      <div class="grid" id="chGrid"></div>
    </div>

    <div class="card">
      <button class="btn big ghost" onclick="startRandom()">随机练习（全部未做）</button>
      <button class="btn big" onclick="startWrong()">错题重练（<span id="wrongCnt">0</span>）</button>
      <button class="btn big ghost" onclick="showView('v-set')">⚙ 同步与设置</button>
    </div>
  </section>

  <!-- 答题页 -->
  <section id="v-quiz" class="hidden">
    <div class="card">
      <div class="row" style="justify-content:space-between">
        <span class="chip" id="qCh"></span>
        <span class="qmeta" id="qProg"></span>
      </div>
      <div class="qtext" id="qText"></div>
      <div id="opts"></div>
      <div id="blankBox" class="hidden">
        <input type="text" id="blankInput" placeholder="输入你的答案" onkeydown="if(event.key==='Enter')checkBlank()">
        <button class="btn" style="margin-top:8px" onclick="checkBlank()">提交答案</button>
      </div>
      <div id="essayBox" class="hidden">
        <button class="btn ghost" onclick="revealEssay()">显示参考答案</button>
      </div>
      <div class="ansbox" id="ansbox"></div>
      <div id="essayRate" class="hidden" style="margin-top:10px">
        <div class="muted" style="margin-bottom:6px">这题你掌握了吗？</div>
        <button class="btn" onclick="rateEssay(true)" style="background:#16a34a">记住了</button>
        <button class="btn ghost danger" onclick="rateEssay(false)" style="margin-left:8px">没记住</button>
      </div>
    </div>
    <nav class="qnav">
      <button class="btn ghost" onclick="prevQ()">上一题</button>
      <button class="btn ghost" onclick="showView('v-home')">退出</button>
      <button class="btn" onclick="nextQ()">下一题</button>
    </nav>
  </section>

  <!-- 错题列表 -->
  <section id="v-wrong" class="hidden">
    <div class="card">
      <div class="row" style="justify-content:space-between">
        <b>错题本</b>
        <button class="btn ghost" onclick="showView('v-home')">返回</button>
      </div>
      <div id="wrongList" style="margin-top:8px"></div>
    </div>
  </section>

  <!-- 设置 -->
  <section id="v-set" class="hidden">
    <div class="card">
      <div class="row" style="justify-content:space-between">
        <b>GitHub 跨设备同步</b>
        <button class="btn ghost" onclick="showView('v-home')">返回</button>
      </div>
      <p class="muted">把答题进度存在你自己的 GitHub 仓库里（progress.json）。在别的设备上填入同样的设置即可拉回进度。</p>
      <label class="f">GitHub 用户名</label>
      <input type="text" id="cfgOwner" placeholder="例如：yourname">
      <label class="f">仓库名（如 quiz ）</label>
      <input type="text" id="cfgRepo" placeholder="your-repo">
      <label class="f">分支（默认 main）</label>
      <input type="text" id="cfgBranch" value="main">
      <label class="f">Personal Access Token（需 repo / public_repo 权限）</label>
      <input type="password" id="cfgToken" placeholder="ghp_xxxxx">
      <div class="row" style="margin-top:12px">
        <button class="btn" onclick="pushNow()">立即上传进度</button>
        <button class="btn ghost" onclick="pullNow()">立即下载进度</button>
      </div>
      <div class="muted" id="syncStatus" style="margin-top:8px"></div>
    </div>
    <div class="card">
      <b>本地数据</b>
      <div class="switch"><span>导出备份文件</span><button class="btn ghost" onclick="exportLocal()">导出</button></div>
      <div class="switch"><span>导入备份文件</span><button class="btn ghost" onclick="document.getElementById('impFile').click()">选择文件</button>
        <input type="file" id="impFile" accept="application/json" style="display:none" onchange="importLocal(event)"></div>
      <div class="switch"><span>清空本机进度</span><button class="btn danger" onclick="resetLocal()">清空</button></div>
    </div>
  </section>

</div>
<div class="toast" id="toast"></div>

<script>
__BANK__

// ---------- 工具 ----------
const KEY=0x5A;
function dec(s){const b=atob(s).split('').map(c=>c.charCodeAt(0)^KEY);
  return new TextDecoder().decode(new Uint8Array(b));}
function $(id){return document.getElementById(id)}
function toast(t){const e=$('toast');e.textContent=t;e.classList.add('show');
  clearTimeout(e._t);e._t=setTimeout(()=>e.classList.remove('show'),1800);}

const CHMAP={};
BANK.forEach(q=>{CHMAP[q.ch]=(CHMAP[q.ch]||0)+1;});

// ---------- 进度存储 ----------
const LK='jdquiz.progress.v1';
let P=JSON.parse(localStorage.getItem(LK)||'{"state":{},"wrong":[],"mastered":[],"updatedAt":0}');
function saveLocal(){localStorage.setItem(LK,JSON.stringify(P));P.updatedAt=Date.now();}
function qdone(id){return !!P.state[id];}
function isWrong(id){return P.wrong.includes(id);}

// ---------- 视图切换 ----------
function showView(v){
  ['v-home','v-quiz','v-wrong','v-set'].forEach(x=>$(x).classList.add('hidden'));
  $(v).classList.remove('hidden');
  if(v==='v-home') renderHome();
  if(v==='v-set') fillCfg();
  window.scrollTo(0,0);
}

// ---------- 首页 ----------
function renderHome(){
  const total=BANK.length, done=Object.keys(P.state).length;
  let right=0; Object.values(P.state).forEach(s=>{if(s.correct)right++;});
  $('pct').textContent=done+' / '+total+' 题';
  $('pbar').style.width=(done/total*100)+'%';
  $('stDone').textContent=done;
  $('stRight').textContent=right;
  $('stWrong').textContent=P.wrong.length;
  $('wrongCnt').textContent=P.wrong.length;
  const g=$('chGrid');g.innerHTML='';
  Object.keys(CHMAP).forEach(ch=>{
    const list=BANK.filter(q=>q.ch===ch);
    const dn=list.filter(q=>P.state[q.id]).length;
    const d=document.createElement('div');d.className='ch';
    d.innerHTML=`<div class="name">${ch}</div><div class="meta">${dn}/${list.length} 已做</div>`;
    d.onclick=()=>startChapter(ch);
    g.appendChild(d);
  });
}

// ---------- 出题 ----------
let cur={list:[],idx:0,answered:false};
function buildList(filter){return BANK.filter(filter).map(q=>q.id);}
function startChapter(ch){
  cur.list=buildList(q=>q.ch===ch); cur.idx=0; showQ();
}
function startRandom(){
  cur.list=buildList(q=>!P.state[q.id]);
  if(!cur.list.length){toast('没有未做的题目啦');return;}
  cur.idx=0; showQ();
}
function startWrong(){
  cur.list=P.wrong.slice();
  if(!cur.list.length){toast('错题本是空的');showView('v-home');return;}
  cur.idx=0; showQ();
}
function byId(id){return BANK.find(q=>q.id===id);}

function showQ(){
  showView('v-quiz');
  cur.answered=false;
  const q=byId(cur.list[cur.idx]);
  $('qCh').textContent=q.ch+' · '+({choice:'选择题',judge:'判断题',blank:'填空题',essay:'简答题'})[q.t];
  $('qProg').textContent=(cur.idx+1)+' / '+cur.list.length;
  $('qText').textContent=q.q;
  const box=$('opts');box.innerHTML='';
  $('blankBox').classList.add('hidden');
  $('essayBox').classList.add('hidden');
  $('essayRate').classList.add('hidden');
  $('ansbox').className='ansbox';$('ansbox').innerHTML='';
  if(q.t==='choice'){
    Object.keys(q.o).sort().forEach(k=>{
      const b=document.createElement('button');b.className='opt';
      b.innerHTML=`<span class="k">${k}</span><span></span>`;
      b.querySelector('span:last-child').textContent=q.o[k];
      b.onclick=()=>pickChoice(q,k,b);
      box.appendChild(b);
    });
  }else if(q.t==='judge'){
    [['对（√）','T'],['错（×）','F']].forEach(([txt,val])=>{
      const b=document.createElement('button');b.className='opt';
      b.innerHTML=`<span class="k">${val==='T'?'√':'×'}</span><span></span>`;
      b.querySelector('span:last-child').textContent=txt;
      b.onclick=()=>pickJudge(q,val,b);
      box.appendChild(b);
    });
  }else if(q.t==='blank'){
    $('blankBox').classList.remove('hidden');
    $('blankInput').value='';$('blankInput').focus();
  }else if(q.t==='essay'){
    $('essayBox').classList.remove('hidden');
  }
}

function record(q,correct){
  P.state[q.id]={done:true,correct:lastCorrect(correct),ts:Date.now()};
  // correct 一旦答对就记 true（掌握后不再当错题）
  if(correct){
    P.state[q.id].correct=true;
    P.wrong=P.wrong.filter(x=>x!==q.id);
  }else{
    if(!P.wrong.includes(q.id))P.wrong.push(q.id);
  }
  saveLocal(); scheduleSync();
}
function lastCorrect(c){return c;}

function pickChoice(q,k,btn){
  if(cur.answered)return;cur.answered=true;
  const ans=dec(q.a);
  const opts=[...$('opts').children];
  opts.forEach(b=>b.disabled=true);
  const right=(k===ans);
  if(right){btn.classList.add('right');}
  else{btn.classList.add('wrong');
    opts.forEach(b=>{if(b.querySelector('.k').textContent===ans)b.classList.add('right');});}
  showAns(right,'正确答案：'+ans);
  record(q,right);
}
function pickJudge(q,val,btn){
  if(cur.answered)return;cur.answered=true;
  const ans=dec(q.a);
  const opts=[...$('opts').children];
  opts.forEach(b=>b.disabled=true);
  const right=(val===ans);
  if(right){btn.classList.add('right');}
  else{btn.classList.add('wrong');
    opts.forEach(b=>{if(b.querySelector('.k').textContent===ans)b.classList.add('right');});}
  showAns(right,right?'回答正确':'正确答案：'+(ans==='T'?'对（√）':'错（×）'));
  record(q,right);
}
function norm(s){return (s||'').toString().toLowerCase().replace(/[\s，。、,.;；:：()（）]/g,'');}
function checkBlank(){
  const q=byId(cur.list[cur.idx]);
  if(cur.answered)return;cur.answered=true;
  const user=$('blankInput').value;
  const ans=dec(q.a);
  const right=norm(user)===norm(ans)||norm(ans).includes(norm(user))&&norm(user).length>=2||norm(user).includes(norm(ans))&&norm(ans).length>=2;
  showAns(right,'参考答案：'+ans);
  record(q,right);
}
function revealEssay(){
  const q=byId(cur.list[cur.idx]);
  $('essayRate').classList.remove('hidden');
  showAnsRef('参考答案：'+dec(q.a));
  P.state[q.id]={done:true,correct:false,ts:Date.now()};
  saveLocal(); scheduleSync();
}
function rateEssay(know){
  const q=byId(cur.list[cur.idx]);
  if(know){P.mastered.push(q.id);P.wrong=P.wrong.filter(x=>x!==q.id);P.state[q.id].correct=true;}
  else{if(!P.wrong.includes(q.id))P.wrong.push(q.id);}
  saveLocal();scheduleSync();
  toast(know?'已记为掌握':'已加入错题');
  nextQ();
}
function showAns(ok,text){
  const b=$('ansbox');b.className='ansbox show '+(ok?'ok':'no');b.textContent=text;
}
function showAnsRef(text){const b=$('ansbox');b.className='ansbox show ref';b.textContent=text;}
function prevQ(){if(cur.idx>0){cur.idx--;showQ();}}
function nextQ(){if(cur.idx<cur.list.length-1){cur.idx++;showQ();}else{toast('本组完成！');showView('v-home');}}

// ---------- GitHub 同步 ----------
const CK='jdquiz.cfg.v1';
function getCfg(){try{return JSON.parse(localStorage.getItem(CK)||'{}');}catch(e){return{};}}
function fillCfg(){const c=getCfg();
  $('cfgOwner').value=c.owner||'';$('cfgRepo').value=c.repo||'';
  $('cfgBranch').value=c.branch||'main';$('cfgToken').value=c.token||'';
  $('syncStatus').textContent='上次同步：'+(c.syncedAt?new Date(c.syncedAt).toLocaleString():'从未');
}
function saveCfg(){
  const c={owner:$('cfgOwner').value.trim(),repo:$('cfgRepo').value.trim(),
    branch:$('cfgBranch').value.trim()||'main',token:$('cfgToken').value.trim(),
    syncedAt:getCfg().syncedAt||0};
  localStorage.setItem(CK,JSON.stringify(c));return c;
}
function api(c,method,content,sha){
  const url=`https://api.github.com/repos/${c.owner}/${c.repo}/contents/progress.json`;
  const body={message:'sync progress',branch:c.branch,content:btoa(unescape(encodeURIComponent(JSON.stringify(content))))};
  if(sha)body.sha=sha;
  return fetch(url,{method,headers:{'Authorization':'token '+c.token,'Accept':'application/vnd.github+json'},
    body:JSON.stringify(body)}).then(r=>r.json());
}
function merge(local,remote){
  const s=Object.assign({},remote.state,local.state);
  // 一旦答对保留 correct
  Object.keys(s).forEach(k=>{if(local.state[k]&&local.state[k].correct)s[k].correct=true;});
  return {state:s,
    wrong:[...new Set([...(remote.wrong||[]),...local.wrong])],
    mastered:[...new Set([...(remote.mastered||[]),...local.mastered])],
    updatedAt:Math.max(local.updatedAt,remote.updatedAt||0)};
}
async function pullNow(){
  const c=saveCfg();
  if(!c.owner||!c.repo||!c.token){toast('请先填写仓库信息和Token');return;}
  $('syncStatus').textContent='正在下载…';
  try{
    const r=await fetch(`https://api.github.com/repos/${c.owner}/${c.repo}/contents/progress.json?ref=${c.branch}`,
      {headers:{'Authorization':'token '+c.token}});
    if(r.status===404){$('syncStatus').textContent='仓库中还没有进度文件，点上传创建';return;}
    const j=await r.json();
    const remote=JSON.parse(decodeURIComponent(escape(atob(j.content))));
    P=merge(P,remote);
    localStorage.setItem(LK,JSON.stringify(P));
    c.syncedAt=Date.now();localStorage.setItem(CK,JSON.stringify(c));
    $('syncStatus').textContent='已同步 '+new Date().toLocaleString();toast('下载成功');renderHome();
  }catch(e){$('syncStatus').textContent='下载失败：'+e.message;}
}
async function pushNow(){
  const c=saveCfg();
  if(!c.owner||!c.repo||!c.token){toast('请先填写仓库信息和Token');return;}
  $('syncStatus').textContent='正在上传…';
  try{
    // 先取 sha
    let sha=null;
    const g=await fetch(`https://api.github.com/repos/${c.owner}/${c.repo}/contents/progress.json?ref=${c.branch}`,
      {headers:{'Authorization':'token '+c.token}});
    if(g.ok){const gj=await g.json();sha=gj.sha;}
    P.updatedAt=Date.now();
    await api(c,'PUT',P,sha);
    c.syncedAt=Date.now();localStorage.setItem(CK,JSON.stringify(c));
    $('syncStatus').textContent='已上传 '+new Date().toLocaleString();toast('上传成功');
  }catch(e){$('syncStatus').textContent='上传失败：'+e.message;}
}
let syncT=null;
function scheduleSync(){clearTimeout(syncT);syncT=setTimeout(()=>{const c=getCfg();
  if(c.owner&&c.repo&&c.token)pushNow().catch(()=>{});},3000);}

// ---------- 导入导出 ----------
function exportLocal(){
  const blob=new Blob([JSON.stringify(P,null,2)],{type:'application/json'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);
  a.download='progress-backup.json';a.click();
}
function importLocal(ev){
  const f=ev.target.files[0];if(!f)return;
  const rd=new FileReader();
  rd.onload=()=>{try{P=JSON.parse(rd.result);saveLocal();toast('导入成功');renderHome();}catch(e){toast('文件格式错误');}};
  rd.readAsText(f);
}
function resetLocal(){
  if(confirm('确定清空本机所有答题进度？')){
    P={state:{},wrong:[],mastered:[],updatedAt:0};
    localStorage.setItem(LK,JSON.stringify(P));renderHome();toast('已清空');
  }
}

// 启动
renderHome();
// 有配置则自动拉取
(function(){const c=getCfg();if(c.owner&&c.repo&&c.token)pullNow();})();
</script>
</body>
</html>
"""

html = HTML.replace("__BANK__", bank_js)
out_path = r'C:\Users\27498\Doubao\chats\2026-09-13\new-chat-1\index.html'
open(out_path, 'w', encoding='utf-8').write(html)
print('written', out_path, len(html), 'bytes; questions', len(out))
