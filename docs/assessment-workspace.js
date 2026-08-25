(()=>{
const KEY='spectrasec-control-assessments-v1';
const $=s=>document.querySelector(s);
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let observations=[];
function load(){try{observations=JSON.parse(localStorage.getItem(KEY)||'[]');if(!Array.isArray(observations)) observations=[];}catch{observations=[];}render();}
function save(){localStorage.setItem(KEY,JSON.stringify(observations));render();}
function download(name,type,text){const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([text],{type}));a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);}
function refsForFinding(id){const f=(window.findings||[]).find(x=>x.finding_id===id);return f?.refs||[];}
function render(){const root=$('#manual-observations');if(!root)return;$('#manual-count').textContent=`${observations.length} observation${observations.length===1?'':'s'}`;root.innerHTML=observations.length?observations.map((o,i)=>`<article class="manual-row"><div><strong>${esc(o.title)}</strong><small>${esc(o.asset||'Unspecified asset')} · ${esc(o.status)} · ${esc(o.owner||'No owner')}</small></div><span>${refsForFinding(o.findingId).length} mapped refs</span><button class="secondary-button" data-remove="${i}" type="button">Remove</button></article>`).join(''):'<p class="notice">No manual observations yet. Add a control observation below or import a generic JSON/CSV assessment.</p>';root.querySelectorAll('[data-remove]').forEach(b=>b.onclick=()=>{observations.splice(Number(b.dataset.remove),1);save();});}
function init(){const form=$('#manual-assessment-form');if(!form)return;
form.addEventListener('submit',e=>{e.preventDefault();const fd=new FormData(form),findingId=fd.get('findingId'),catalog=(window.findings||[]).find(x=>x.finding_id===findingId);observations.push({id:crypto.randomUUID?crypto.randomUUID():String(Date.now()),findingId,title:catalog?.title||fd.get('title')||findingId,status:fd.get('status'),asset:fd.get('asset'),owner:fd.get('owner'),evidence:fd.get('evidence'),evidenceDate:fd.get('evidenceDate'),notes:fd.get('notes'),createdAt:new Date().toISOString()});save();form.reset();});
$('#export-assessment-json').onclick=()=>download('spectrasec-assessment.json','application/json',JSON.stringify({version:'1.0',exportedAt:new Date().toISOString(),observations},null,2));
$('#export-assessment-csv').onclick=()=>{const cols=['findingId','title','status','asset','owner','evidence','evidenceDate','notes'];const q=v=>'"'+String(v??'').replaceAll('"','""')+'"';download('spectrasec-assessment.csv','text/csv',cols.join(',')+'\n'+observations.map(o=>cols.map(c=>q(o[c])).join(',')).join('\n'));};
$('#reset-assessment').onclick=()=>{if(confirm('Clear all locally saved manual observations?')){observations=[];save();}};
const sel=$('#manual-finding');(window.findings||[]).forEach(f=>sel.add(new Option(`${f.title} (${f.finding_id})`,f.finding_id)));
load();}
window.addEventListener('load',()=>setTimeout(init,0));
})();