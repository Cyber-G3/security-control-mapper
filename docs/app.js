const findings = [
  {id:'SCM-REP-001',type:'branch-protection-disabled',title:'Branch protection disabled',domain:'repository-security',severity:'HIGH',remediation:'Enable protected-branch rules appropriate to the repository change-control model.',evidence:['Branch protection configuration','Change approval workflow'],refs:[['ISO/IEC 27001:2022','A.8.32','Change management','SUPPORTING'],['NIS2','Article 21(2)(e)','Security in acquisition, development and maintenance','CONTEXTUAL'],['SOC 2','CC8.1','Change management','SUPPORTING'],['ENS','mp.sw.2','Aceptación y puesta en servicio','CONTEXTUAL']]},
  {id:'SCM-REP-002',type:'required-pr-reviews-disabled',title:'Required PR reviews disabled',domain:'repository-security',severity:'HIGH',remediation:'Require independent review before changes can be merged.',evidence:['Pull-request approval rules','Reviewer assignment evidence'],refs:[['ISO/IEC 27001:2022','A.8.32','Change management','SUPPORTING'],['SOC 2','CC8.1','Change management','SUPPORTING'],['ENS','op.acc.3','Segregación de funciones y tareas','CONTEXTUAL']]},
  {id:'SCM-SEC-001',type:'secret-scanning-disabled',title:'Secret scanning disabled',domain:'secrets',severity:'HIGH',remediation:'Enable secret scanning or an equivalent detective control and define credential rotation handling.',evidence:['Secret scanning configuration','Credential management procedure'],refs:[['ISO/IEC 27001:2022','A.5.17','Authentication information','SUPPORTING'],['ENS','op.acc.4','Proceso de gestión de derechos de acceso','CONTEXTUAL']]},
  {id:'SCM-VUL-001',type:'critical-vulnerability-overdue',title:'Critical vulnerability remediation overdue',domain:'vulnerability-management',severity:'CRITICAL',remediation:'Prioritize remediation or documented risk treatment for overdue critical vulnerabilities.',evidence:['Vulnerability record','Remediation evidence','Risk acceptance if applicable'],refs:[['ISO/IEC 27001:2022','A.8.8','Management of technical vulnerabilities','SUPPORTING'],['NIS2','Article 21(2)(e)','Security in acquisition, development and maintenance','CONTEXTUAL']]},
  {id:'SCM-IAM-001',type:'mfa-not-enforced',title:'Multi-factor authentication not enforced',domain:'identity-access',severity:'HIGH',remediation:'Enforce MFA for applicable identities, with stronger requirements for privileged access.',evidence:['MFA enforcement policy','Identity-provider configuration'],refs:[['ISO/IEC 27001:2022','A.8.5','Secure authentication','SUPPORTING'],['NIS2','Article 21(2)(j)','Multi-factor authentication','DIRECT']]},
  {id:'SCM-PAM-001',type:'privileged-access-not-reviewed',title:'Privileged access not periodically reviewed',domain:'privileged-access',severity:'HIGH',remediation:'Establish periodic privileged-access review and evidence reviewer decisions.',evidence:['Privileged access inventory','Access review record'],refs:[['ISO/IEC 27001:2022','A.8.2','Privileged access rights','SUPPORTING'],['SOC 2','CC6.3','Access authorization','SUPPORTING']]},
  {id:'SCM-LOG-001',type:'security-logging-disabled',title:'Security logging disabled or insufficient',domain:'logging-monitoring',severity:'HIGH',remediation:'Enable security-relevant logging and define retention, monitoring and alerting requirements.',evidence:['Logging configuration','Retention configuration','Alerting evidence'],refs:[['ISO/IEC 27001:2022','A.8.15','Logging','SUPPORTING'],['NIS2','Article 21(2)(b)','Incident handling','CONTEXTUAL']]},
  {id:'SCM-BCK-001',type:'backup-restore-not-tested',title:'Backup restoration not tested',domain:'backup-recovery',severity:'HIGH',remediation:'Perform and evidence restoration testing at a frequency aligned to service criticality.',evidence:['Backup configuration','Restore test record','Recovery result'],refs:[['ISO/IEC 27001:2022','A.8.13','Information backup','SUPPORTING'],['NIS2','Article 21(2)(c)','Business continuity and crisis management','CONTEXTUAL']]},
  {id:'SCM-IR-001',type:'incident-plan-not-tested',title:'Incident response plan not tested',domain:'incident-response',severity:'MEDIUM',remediation:'Run an incident-response exercise and capture lessons, actions and ownership.',evidence:['Incident response plan','Exercise record','Improvement actions'],refs:[['ISO/IEC 27001:2022','A.5.24','Incident management planning and preparation','SUPPORTING'],['NIS2','Article 21(2)(b)','Incident handling','CONTEXTUAL']]},
  {id:'SCM-TPR-001',type:'critical-supplier-not-assessed',title:'Critical supplier security risk not assessed',domain:'third-party-risk',severity:'HIGH',remediation:'Perform a risk-based supplier security assessment and document treatment decisions.',evidence:['Supplier inventory','Risk assessment','Due-diligence evidence'],refs:[['ISO/IEC 27001:2022','A.5.19','Information security in supplier relationships','SUPPORTING'],['NIS2','Article 21(2)(d)','Supply chain security','CONTEXTUAL']]}
];

const sectors = {
  general:{label:'General',adjustment:0,priority:[]},
  'saas-technology':{label:'SaaS / Technology',adjustment:5,priority:['repository-security','vulnerability-management','secrets']},
  'cloud-provider':{label:'Cloud Provider',adjustment:10,priority:['privileged-access','logging-monitoring','backup-recovery']},
  'financial-services':{label:'Financial Services',adjustment:10,priority:['privileged-access','third-party-risk','incident-response']},
  'healthcare-life-sciences':{label:'Healthcare / Life Sciences',adjustment:10,priority:['identity-access','backup-recovery','third-party-risk']},
  'public-sector':{label:'Public Sector',adjustment:8,priority:['identity-access','logging-monitoring','incident-response']},
  'critical-infrastructure':{label:'Critical Infrastructure',adjustment:15,priority:['backup-recovery','incident-response','third-party-risk']},
  'manufacturing-industrial':{label:'Manufacturing / Industrial',adjustment:8,priority:['vulnerability-management','backup-recovery','third-party-risk']},
  'professional-services':{label:'Professional Services',adjustment:3,priority:['identity-access','third-party-risk','secrets']}
};

const severityScore={LOW:10,MEDIUM:30,HIGH:55,CRITICAL:75};
const assetScore={LOW:0,MEDIUM:8,HIGH:15,CRITICAL:22};
const dataScore={PUBLIC:0,INTERNAL:4,CONFIDENTIAL:9,RESTRICTED:14};
const serviceScore={LOW:0,MEDIUM:5,HIGH:10,CRITICAL:15};
const priorityRank={CRITICAL:4,HIGH:3,MEDIUM:2,LOW:1};

function contextualRisk(finding){
  const sector=sectors[document.querySelector('#sector').value];
  let score=severityScore[finding.severity]+assetScore[asset.value]+dataScore[data.value]+serviceScore[service.value]+sector.adjustment;
  const reasons=[`severity:${finding.severity.toLowerCase()}`,`sector:${document.querySelector('#sector').value}`];
  if(sector.priority.includes(finding.domain)){score+=7;reasons.push('sector_priority_domain');}
  if(internet.checked){score+=12;reasons.push('internet_exposed');}
  if(active.checked){score+=20;reasons.push('active_exploitation');}
  if(compensating.checked){score-=12;reasons.push('compensating_controls');}
  score=Math.max(0,Math.min(100,score));
  const priority=score>=85?'CRITICAL':score>=65?'HIGH':score>=40?'MEDIUM':'LOW';
  return {score,priority,reasons};
}

const sector=document.querySelector('#sector'),framework=document.querySelector('#framework'),priority=document.querySelector('#priority'),domain=document.querySelector('#domain'),asset=document.querySelector('#asset'),data=document.querySelector('#data'),service=document.querySelector('#service'),internet=document.querySelector('#internet'),active=document.querySelector('#active'),compensating=document.querySelector('#compensating'),search=document.querySelector('#search'),portfolio=document.querySelector('#portfolio'),detail=document.querySelector('#detail');

Object.entries(sectors).forEach(([value,item])=>sector.add(new Option(item.label,value)));
[...new Set(findings.map(f=>f.domain))].sort().forEach(value=>domain.add(new Option(value.replaceAll('-',' '),value)));

function filteredPortfolio(){
  const q=search.value.trim().toLowerCase();
  return findings.map(f=>({...f,risk:contextualRisk(f)})).filter(f=>{
    if(priority.value&&f.risk.priority!==priority.value)return false;
    if(domain.value&&f.domain!==domain.value)return false;
    if(framework.value&&!f.refs.some(r=>r[0]===framework.value))return false;
    if(q&&!`${f.title} ${f.domain} ${f.evidence.join(' ')}`.toLowerCase().includes(q))return false;
    return true;
  }).sort((a,b)=>priorityRank[b.risk.priority]-priorityRank[a.risk.priority]||b.risk.score-a.risk.score||a.title.localeCompare(b.title));
}

function render(){
  const items=filteredPortfolio();
  document.querySelector('#kpi-total').textContent=items.length;
  document.querySelector('#kpi-critical').textContent=items.filter(x=>x.risk.priority==='CRITICAL').length;
  document.querySelector('#kpi-high').textContent=items.filter(x=>x.risk.priority==='HIGH').length;
  document.querySelector('#kpi-average').textContent=items.length?Math.round(items.reduce((s,x)=>s+x.risk.score,0)/items.length):0;
  portfolio.innerHTML=items.map((f,i)=>`<button class="finding-row" data-index="${i}"><span><strong>${f.title}</strong><small>${f.id} · ${f.domain}</small></span><span class="risk ${f.risk.priority.toLowerCase()}">${f.risk.priority}<b>${f.risk.score}</b></span></button>`).join('')||'<p class="notice">No findings match the current filters.</p>';
  portfolio.querySelectorAll('.finding-row').forEach((el)=>el.addEventListener('click',()=>renderDetail(items[Number(el.dataset.index)])));
  if(items.length)renderDetail(items[0]);
}

function renderDetail(f){
  detail.innerHTML=`<div class="detail-head"><div><h3>${f.title}</h3><p class="notice">${f.id} · ${f.domain}</p></div><span class="risk ${f.risk.priority.toLowerCase()}">${f.risk.priority}<b>${f.risk.score}</b></span></div>
  <div class="detail-grid"><article><h4>Why prioritized</h4><ul>${f.risk.reasons.map(x=>`<li>${x}</li>`).join('')}</ul></article><article><h4>Remediation</h4><p>${f.remediation}</p></article><article><h4>Evidence expected</h4><ul>${f.evidence.map(x=>`<li>${x}</li>`).join('')}</ul></article></div>
  <h4>Supporting framework references</h4><div class="refs">${f.refs.filter(r=>!framework.value||r[0]===framework.value).map(r=>`<article class="ref"><strong>${r[0]} · ${r[1]}</strong><span>${r[2]}</span><em>${r[3]}</em></article>`).join('')||'<p class="notice">No references for the selected framework.</p>'}</div>
  <p class="notice">Sector context tunes prioritization only. Framework references indicate supporting relevance and do not establish legal applicability or compliance.</p>`;
}

[sector,framework,priority,domain,asset,data,service,internet,active,compensating,search].forEach(el=>el.addEventListener(el===search?'input':'change',render));
sector.value='general';
render();
