const fs=require('node:fs');const vm=require('node:vm');const assert=require('node:assert/strict');
const source=fs.readFileSync('assets/redesign.js','utf8');
function fixture(locale,query,clinicName){
 const elements={};let opened=[];
 const select=(values,value=values[0])=>({options:values.map(v=>({value:v,textContent:v})),value,listeners:{},addEventListener(e,fn){this.listeners[e]=fn},get selectedIndex(){return this.options.findIndex(o=>o.value===this.value)},reportValidity(){this.invalid=true}});
 elements['#clinic']=select(['','Surface CITOS','Surface Setiabudi'],clinicName);
 elements['#interest']=select(['general','Clear','Tone','Texture','Calm','Tighten','Enhance']);
 elements['#visit-type']=select(['first','followup','return']);
 elements['#preferred-time']=select(['flexible','morning','afternoon','evening'],'afternoon');
 elements['#preferred-date']={value:'2026-11-05'};
 elements['#booking-form']={addEventListener(e,fn){this[e]=fn}};
 const context={document:{body:{dataset:{locale}},title:'Tone · Surface Skin Habit',querySelector:s=>elements[s]||null,querySelectorAll:()=>[],addEventListener(){}},location:{search:query,origin:'https://stevetsurface.github.io',pathname:'/surface-skin-habit-website/en/tone.html'},localStorage:{getItem:()=>null,setItem(){}},window:{open:(...args)=>opened.push(args)},URLSearchParams,Intl,Date,encodeURIComponent,matchMedia:()=>({matches:false})};
 vm.runInNewContext(source,context);
 return {elements,opened,submit(){elements['#booking-form'].submit({preventDefault(){}})}};
}
const en=fixture('en','?concern=TONE&visit=followup','Surface CITOS');
assert.equal(en.elements['#interest'].value,'Tone');assert.equal(en.elements['#visit-type'].value,'followup');en.submit();assert.equal(en.opened.length,1);const message=new URL(en.opened[0][0]).searchParams.get('text');assert.match(message,/Surface CITOS/);assert.match(message,/2026-11-05/);assert.match(message,/followup/);assert.match(message,/appointment request/);assert.match(message,/\/surface-skin-habit-website\/en\/tone.html/);
const empty=fixture('en','', '');empty.submit();assert.equal(empty.opened.length,0);assert.equal(empty.elements['#clinic'].invalid,true);
const id=fixture('id','?concern=CLEAR&visit=return','Surface Setiabudi');id.submit();assert.match(new URL(id.opened[0][0]).searchParams.get('text'),/Belum merupakan booking terkonfirmasi/);
console.log('Booking handoff checks passed: deep links, clinic/date/context, request wording, required clinic, Indonesian.');
