import json,sys,os
OUT=sys.argv[1]; R=json.load(open(os.path.join(OUT,'10_puppet_rigs','rigs_all.json')))
for k in list(R):
    if 'viewBoxes' not in R[k]: R.pop(k)
html='''<!doctype html><html><head><meta charset="utf-8"><title>Puppet rig demo – SVG Asset Library v3</title>
<style>body{margin:0;background:#141826;color:#ECE4D6;font:14px Inter,Segoe UI,Tahoma,sans-serif;display:flex;height:100vh}
#side{width:320px;padding:16px;background:#0F121C;overflow:auto}#stage{flex:1;position:relative;overflow:hidden;background:radial-gradient(#2A3148,#141826)}
.b{position:absolute;left:0;top:0;width:0;height:0}.b>img{position:absolute;pointer-events:none}
label{display:block;margin:6px 0 0;color:#8A93A8;font-size:12px}input[type=range]{width:100%}select,button{width:100%;padding:7px;margin-top:4px;background:#1F2537;color:#ECE4D6;border:1px solid #2C3550;border-radius:8px}
h2{font-size:17px;margin:0 0 8px}.ground{position:absolute;left:0;right:0;height:2px;background:#5A6480}</style></head><body>
<div id="side"><h2>Puppet rig demo</h2><small>Separate body parts + rig.json, animated live (no frame files). Same parts work in After Effects / Spine / Moho / Rive / GSAP.</small>
<label>Character</label><select id="ch"></select><label>Motion</label><select id="mo"><option>walk</option><option>run</option><option>wave</option><option>idle</option><option>dance</option><option>manual (sliders)</option></select>
<label>Speed</label><input type="range" id="sp" min="0.2" max="2.5" step="0.05" value="1"><label>Expression</label><select id="ex"></select><label>Near hand</label><select id="hn"></select><label>Far hand</label><select id="hf"></select><div id="sl"></div></div>
<div id="stage"><div class="ground" style="top:78%"></div></div>
<script>
const R=__DATA__;const J=['upper_arm_near','forearm_near','upper_arm_far','forearm_far','thigh_near','shin_near','foot_near','thigh_far','shin_far','foot_far','head'];
const ang={};J.forEach(j=>ang[j]=0);let P={},ck=Object.keys(R)[0],t0=performance.now();
const ch=document.getElementById('ch');Object.keys(R).forEach(k=>ch.add(new Option(k,k)));
const sl=document.getElementById('sl');J.forEach(j=>{sl.insertAdjacentHTML('beforeend','<label>'+j+'</label><input type="range" min="-150" max="150" value="0" id="s_'+j+'">');});
function img(part,dx,dy){const v=R[ck].viewBoxes[part];const i=document.createElement('img');i.src=ck+'/'+part+'.svg';i.style.left=(v[0]-dx)+'px';i.style.top=(v[1]-dy)+'px';i.style.width=v[2]+'px';i.style.height=v[3]+'px';return i}
function bone(name,parent,at,part,z,dx=0,dy=0){const d=document.createElement('div');d.className='b';d.style.left=at[0]+'px';d.style.top=at[1]+'px';d.style.zIndex=z;if(part)d.appendChild(img(part,dx,dy));parent.appendChild(d);P[name]=d;return d}
function build(){const st=document.getElementById('stage');st.querySelectorAll('.root').forEach(e=>e.remove());P={};const B=R[ck].bones;
 const root=document.createElement('div');root.className='b root';st.appendChild(root);P.root=root;
 const tor=bone('torso',root,[0,0],null,0);const ti=img('torso',0,0);ti.style.zIndex=5;tor.appendChild(ti);
 const hp=B.head.pivot_in_part;const hd=bone('head',tor,B.head.attach,'head_'+document.getElementById('ex').value,6,-hp[0],-hp[1]);
 for(const s of['far','near']){const z=s=='far'?1:10;
  const ua=bone('upper_arm_'+s,tor,B['upper_arm_'+s].attach,'upper_arm_'+s,s=='far'?2:12);
  const fa=bone('forearm_'+s,ua,[0,B['upper_arm_'+s].length],'forearm_'+s,1);
  bone('hand_'+s,fa,[0,B['forearm_'+s].length],'hand_'+document.getElementById(s=='near'?'hn':'hf').value,2);
  const th=bone('thigh_'+s,tor,B['thigh_'+s].attach,'thigh_'+s,s=='far'?1:4);
  const sh=bone('shin_'+s,th,[0,B['thigh_'+s].length],'shin_'+s,1);
  bone('foot_'+s,sh,[0,B['shin_'+s].length],'foot_'+s,2);}
 resize()}
function resize(){const st=document.getElementById('stage');const H=st.clientHeight;const B=R[ck].bones;const legs=B.thigh_near.length+B.shin_near.length+7;const sc=H*.55/(legs+260);
 P.root.style.left=(st.clientWidth/2)+'px';P.root.style.top=(H*.78-legs*sc*1.6)+'px';P.root.style.transform='scale('+(sc*1.6)+')'}
function fill(sel,arr,v){sel.innerHTML='';arr.forEach(a=>sel.add(new Option(a,a)));if(v)sel.value=v}
function setup(){const vb=R[ck].viewBoxes;fill(document.getElementById('ex'),Object.keys(vb).filter(k=>k.startsWith('head_')).map(k=>k.slice(5)),'happy');
 const hs=Object.keys(vb).filter(k=>k.startsWith('hand_')).map(k=>k.slice(5));fill(document.getElementById('hn'),hs,'relax');fill(document.getElementById('hf'),hs,'relax');build()}
ch.onchange=()=>{ck=ch.value;setup()};['ex','hn','hf'].forEach(i=>document.getElementById(i).onchange=build);window.onresize=resize;
function pose(t,m){const s=Math.sin(t),c=Math.cos(t),a={};const kn=x=>6+44*Math.pow(Math.max(0,x),1.4);
 if(m=='walk'){a.thigh_near=26*s;a.shin_near=-kn(c);a.thigh_far=-26*s;a.shin_far=-kn(-c);const sl=Math.sin(t-.55);a.upper_arm_near=-24*sl;a.forearm_near=18+10*Math.max(0,-sl);a.upper_arm_far=24*sl;a.forearm_far=18+10*Math.max(0,sl);a.head=-2+1.6*Math.sin(2*t+.9);a.bob=-3.5*Math.abs(c)}
 else if(m=='run'){const k=x=>18+88*Math.pow(Math.max(0,x),1.1);a.thigh_near=44*s+6;a.shin_near=-k(c);a.thigh_far=-44*s+6;a.shin_far=-k(-c);const sl=Math.sin(t-.35);a.upper_arm_near=-48*sl+6;a.forearm_near=82;a.upper_arm_far=48*sl+6;a.forearm_far=82;a.bob=-9*Math.abs(Math.sin(t+.2));a.lean=12}
 else if(m=='wave'){const w=Math.sin(t*2);a.upper_arm_near=148;a.forearm_near=-38+26*w;a.upper_arm_far=-6;a.forearm_far=14;a.head=-4+1.5*w}
 else if(m=='idle'){a.upper_arm_near=8+2.4*Math.sin(t+.4);a.forearm_near=14+3*s;a.upper_arm_far=-8+2*Math.sin(t+.8);a.forearm_far=16+3*s;a.head=-1+1.4*Math.sin(t+.6);a.lean=1.2*s}
 else if(m=='dance'){const s2=Math.sin(2*t),c2=Math.cos(2*t);a.upper_arm_near=140*Math.max(0,s2)+20;a.forearm_near=20+40*Math.max(0,-s2);a.upper_arm_far=140*Math.max(0,-s2)+20;a.forearm_far=20+40*Math.max(0,s2);a.thigh_near=10*s2+6;a.shin_near=-(10+24*Math.max(0,c2));a.thigh_far=-10*s2-6;a.shin_far=-(10+24*Math.max(0,-c2));a.lean=-2+7*s2;a.head=-6+5*Math.sin(2*t+.8);a.bob=-6*Math.abs(c2)}
 return a}
function tick(now){const m=document.getElementById('mo').value,sp=+document.getElementById('sp').value;const t=(now-t0)/1000*sp*2*Math.PI;let a;
 if(m.startsWith('manual')){a={};J.forEach(j=>a[j]=+document.getElementById('s_'+j).value)}else a=pose(t,m);
 J.forEach(j=>{if(P[j])P[j].style.transform='rotate('+(-(a[j]||0))+'deg)'});
 if(P.torso)P.torso.style.transform='translateY('+(a.bob||0)+'px) rotate('+(-(a.lean||0))+'deg)';
 requestAnimationFrame(tick)}
setup();requestAnimationFrame(tick);
</script></body></html>'''
open(os.path.join(OUT,'10_puppet_rigs','puppet_demo.html'),'w').write(html.replace('__DATA__',json.dumps(R,separators=(',',':'))))
print('ok',len(R))
