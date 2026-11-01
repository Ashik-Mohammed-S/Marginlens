const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const root=path.join(__dirname,'..'),data=JSON.parse(fs.readFileSync(path.join(root,'site/dist/data.json'),'utf8'));
const elements={};
function el(s){return elements[s]??=( {value:({'#month':'2026-08','#region':'All','#category':'All','#price':'0','#cost':'0','#volume':'0'})[s]??'',textContent:'',innerHTML:'',style:{},addEventListener(){},classList:{toggle(){}}});}
const ctx=vm.createContext({console,Intl,Date,Math,Number,String,Object,Set,JSON,URL,Blob,document:{querySelector:el,querySelectorAll:()=>[]},fetch:()=>new Promise(()=>{}),location:{hash:''},window:{},testData:data,setTimeout});
vm.runInContext(fs.readFileSync(path.join(root,'site/dist/app.js'),'utf8'),ctx);
vm.runInContext('DATA=testData;',ctx);
const run=s=>vm.runInContext(s,ctx);
// Exact values independently checked against SQLite mart_sales for August 2026.
assert.equal(run('totals(filtered()).rev'),9961124);
assert.equal(run('totals(filtered()).profit'),4191404);
assert.equal(run("esc('<img onerror=alert(1)>')"),'&lt;img onerror=alert(1)&gt;');
for(const view of ['overview','drivers','exceptions','forecast','quality','brief']){
  run(`view='${view}';render();`);assert.ok(el('#app').innerHTML.length>100);
}
el('#month').value='2026-10';run("view='overview';render();");assert.match(el('#app').innerHTML,/Incomplete/);assert.match(el('#app').innerHTML,/Unavailable/);
run("view='drivers';render();");assert.match(el('#app').innerHTML,/unavailable/);
el('#month').value='2026-09';run("view='drivers';render();");assert.match(el('#app').innerHTML,/\$0\.00/);
el('#region').value='West';el('#category').value='Personal care';
const subset=run('totals(filtered()).rev');assert.ok(subset>0&&subset<9961074);
run("query='nonexistent';view='exceptions';render();");assert.match(el('#app').innerHTML,/No exceptions/);
run("view='forecast';render();");const base=el('#scenario-value').textContent;el('#price').value='5';run('scenario()');assert.notEqual(el('#scenario-value').textContent,base);
console.log('Dashboard checks: PASS (six views, known SQL totals, filters, missing costs, bridge, escaping, empty state, scenario)');
