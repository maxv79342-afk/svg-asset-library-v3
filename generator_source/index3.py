import json,sys,os,re
OUT=sys.argv[1]
M=json.load(open(os.path.join(OUT,'manifest.json')))
items=[];anims={}
for m in M:
    if 'anim' in m:
        a=anims.get(m['anim'])
        if not a:
            a=dict(c=m['cat'],s=m['sub'],n=m['anim'].split('/')[-1],p=m['path'],f=0,fps=m.get('fps',24),pat=re.sub(r'_\d\d\.svg$','_{}.svg',m['path']))
            anims[m['anim']]=a; items.append(a)
        a['f']+=1
    else:
        d=dict(c=m['cat'],s=m['sub'],n=m['name'],p=m['path'])
        if m.get('sheet'): d['sh']=1
        items.append(d)
data=json.dumps(items,separators=(',',':'),ensure_ascii=False)
html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>SVG Asset Library v3 – browser</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{--bg:#141826;--card:#1F2537;--ink:#ECE4D6;--mut:#8A93A8;--acc:#E9A23B}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 Inter,Segoe UI,Tahoma,Arial,sans-serif;display:flex;min-height:100vh}
aside{width:290px;flex:none;background:#0F121C;padding:20px 14px;position:sticky;top:0;height:100vh;overflow:auto}
h1{font-size:21px;margin:0 0 2px}small{color:var(--mut)}
.cat{margin-top:16px;font-weight:800;color:var(--acc);text-transform:uppercase;font-size:12px;letter-spacing:.12em;cursor:pointer}
.sub{display:block;width:100%;text-align:left;background:none;border:0;color:var(--ink);padding:5px 10px;border-radius:8px;cursor:pointer;font:inherit;font-size:14px}
.sub:hover,.sub.on{background:#222941}.sub span{float:right;color:var(--mut)}
main{flex:1;padding:20px 26px;min-width:0}
.bar{display:flex;gap:10px;align-items:center;margin-bottom:18px;flex-wrap:wrap}
input[type=search]{flex:1;min-width:220px;background:var(--card);border:1px solid #2C3550;color:var(--ink);padding:10px 14px;border-radius:10px;font:inherit}
.bgb{background:var(--card);border:1px solid #2C3550;color:var(--ink);padding:9px 12px;border-radius:10px;cursor:pointer;font:inherit}
.bgb.on{border-color:var(--acc)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:12px}
.it{background:var(--card);border-radius:12px;padding:10px;color:var(--ink);display:flex;flex-direction:column;gap:6px;border:1px solid transparent;cursor:pointer;position:relative}
.it:hover{border-color:var(--acc)}
.th{height:150px;border-radius:8px;display:flex;align-items:center;justify-content:center;overflow:hidden}
.th img{max-width:100%;max-height:100%}
.it.sheet{grid-column:span 2}.it.sheet .th{height:220px}
.nm{font-size:13px;word-break:break-all}.nm b{color:var(--acc);font-size:11px;display:block}
.badge{position:absolute;top:14px;left:14px;background:var(--acc);color:#141826;font-size:11px;font-weight:800;padding:2px 7px;border-radius:20px}
body.light .th,body.light .stage{background:#EFEAE0}body.dark .th,body.dark .stage{background:#1A2033}
body.check .th,body.check .stage{background:repeating-conic-gradient(#ccc 0 25%,#fff 0 50%) 0 0/20px 20px}
#more{margin:20px auto;display:block}
.modal{position:fixed;inset:0;background:#000b;display:none;align-items:center;justify-content:center;z-index:9}
.modal.on{display:flex}.box{background:var(--card);border-radius:16px;padding:18px;width:min(92vw,1100px);max-height:94vh;display:flex;flex-direction:column;gap:12px}
.stage{flex:1;min-height:52vh;border-radius:10px;display:flex;align-items:center;justify-content:center;overflow:hidden}
.stage img{max-width:100%;max-height:70vh}
.ctl{display:flex;gap:12px;align-items:center;flex-wrap:wrap}.ctl a{color:var(--acc)}
</style></head><body class="dark">
<aside><h1>SVG Asset Library <span style="color:var(--acc)">v3</span></h1><small id="count"></small><div id="nav"></div></aside>
<main><div class="bar"><input type="search" id="q" placeholder="Search: walk, tattoo, bed, car, hijab, cat, gym, samovar..."><button class="bgb on" data-b="dark">Dark</button><button class="bgb" data-b="light">Light</button><button class="bgb" data-b="check">Transparent</button><label><input type="checkbox" id="sh"> sheets</label><label><input type="checkbox" id="an"> animations only</label></div>
<div class="grid" id="grid"></div><button class="bgb" id="more">Show more</button></main>
<div class="modal" id="mod"><div class="box"><div class="stage" id="stage"><img id="big"></div><div class="ctl" id="ctl"></div></div></div>
<script>
const M=__DATA__;
const pad=n=>String(n).padStart(2,'0');
const fr=(it,i)=>it.pat.replace('{}',pad(i+1));
let cur={c:null,s:null},q='',lim=240;
const nav=document.getElementById('nav'),grid=document.getElementById('grid');
const groups={};M.forEach(m=>{(groups[m.c]=groups[m.c]||{});groups[m.c][m.s]=(groups[m.c][m.s]||0)+(m.f||1)});
document.getElementById('count').textContent=M.reduce((a,m)=>a+(m.f||1),0).toLocaleString()+' SVG files';
for(const c in groups){const h=document.createElement('div');h.className='cat';h.textContent=c;h.onclick=()=>{cur={c,s:null};lim=240;draw()};nav.appendChild(h);
 for(const s in groups[c]){const b=document.createElement('button');b.className='sub';b.innerHTML=s+'<span>'+groups[c][s]+'</span>';b.onclick=()=>{cur={c,s};lim=240;draw()};nav.appendChild(b)}}
let timers=[];
function card(m){const a=document.createElement('div');a.className='it'+(m.sh?' sheet':'');
 a.innerHTML='<div class="th"><img loading="lazy" src="'+m.p+'"></div><div class="nm"><b>'+m.s+'</b>'+m.n+'</div>'+(m.f?'<span class="badge">▶ '+m.f+'f</span>':'');
 if(m.f){const img=a.querySelector('img');let t=null,i=0;a.onmouseenter=()=>{t=setInterval(()=>{i=(i+1)%m.f;img.src=fr(m,i)},1000/m.fps)};a.onmouseleave=()=>{clearInterval(t);img.src=m.p}}
 a.onclick=()=>open_(m);return a}
function draw(){grid.innerHTML='';const sh=document.getElementById('sh').checked,an=document.getElementById('an').checked;
 const L=M.filter(m=>(!cur.c||m.c==cur.c)&&(!cur.s||m.s==cur.s)&&(sh||!m.sh||cur.s)&&(!an||m.f)&&(!q||(m.n+' '+m.s+' '+m.p).toLowerCase().includes(q)));
 L.slice(0,lim).forEach(m=>grid.appendChild(card(m)));document.getElementById('more').style.display=L.length>lim?'block':'none'}
document.getElementById('more').onclick=()=>{lim+=240;draw()};
document.getElementById('q').oninput=e=>{q=e.target.value.toLowerCase();lim=240;draw()};
document.getElementById('sh').onchange=draw;document.getElementById('an').onchange=draw;
document.querySelectorAll('[data-b]').forEach(b=>b.onclick=()=>{document.body.className=b.dataset.b;document.querySelectorAll('[data-b]').forEach(x=>x.classList.toggle('on',x==b))});
const mod=document.getElementById('mod'),big=document.getElementById('big'),ctl=document.getElementById('ctl');let play=null;
mod.onclick=e=>{if(e.target==mod){mod.classList.remove('on');clearInterval(play)}};
function open_(m){mod.classList.add('on');big.src=m.p;clearInterval(play);
 if(!m.f){ctl.innerHTML='<b>'+m.n+'</b> <a href="'+m.p+'" download>download SVG</a> <span style="color:var(--mut)">'+m.p+'</span>';return}
 const pre=[];for(let i=0;i<m.f;i++){const im=new Image();im.src=fr(m,i);pre.push(im)}
 let i=0,fps=m.fps,run=true;
 ctl.innerHTML='<b>'+m.n+'</b> <button class="bgb" id="pp">Pause</button> fps <input type="range" id="fps" min="4" max="60" value="'+fps+'"> <span id="fv">'+fps+'</span> frame <input type="range" id="sc" min="0" max="'+(m.f-1)+'" value="0"> <span id="fi">1/'+m.f+'</span> <label><input type="checkbox" id="pg"> ping-pong</label> <a href="'+m.p+'" download>frame 1</a>';
 let dir=1;const step=()=>{const pg=document.getElementById('pg').checked;if(pg){if(i+dir>=m.f||i+dir<0)dir=-dir;i+=dir}else i=(i+1)%m.f;show()};
 const show=()=>{big.src=fr(m,i);document.getElementById('sc').value=i;document.getElementById('fi').textContent=(i+1)+'/'+m.f};
 const go=()=>{clearInterval(play);if(run)play=setInterval(step,1000/fps)};go();
 document.getElementById('pp').onclick=e=>{run=!run;e.target.textContent=run?'Pause':'Play';go()};
 document.getElementById('fps').oninput=e=>{fps=+e.target.value;document.getElementById('fv').textContent=fps;go()};
 document.getElementById('sc').oninput=e=>{run=false;document.getElementById('pp').textContent='Play';clearInterval(play);i=+e.target.value;show()};}
draw();
</script></body></html>'''
open(os.path.join(OUT,'index.html'),'w').write(html.replace('__DATA__',data))
print('index items',len(items),'anims',len(anims),'bytes',len(html)+len(data))
