import {createHouseView,BULB_SVG} from './scene.mjs';
import {createStore,exportEntityMapping} from './state.mjs';

const $=id=>document.getElementById(id);
async function readJSON(url){const response=await fetch(url);if(!response.ok)throw new Error(`${url} (${response.status})`);return response.json();}
const [house,deviceData,designProfile]=await Promise.all([readJSON('./data/house.json'),readJSON('./data/devices.json'),readJSON('./data/design-style.json')]);
const devices=Array.isArray(deviceData)?deviceData:deviceData.devices;
let storage=null;try{storage=localStorage;}catch{/* The sample still works if storage is blocked. */}
const store=createStore(devices,{storage});
let night=false,toastTimer,currentViewName='overview';
const roomNames=Object.fromEntries(house.rooms.map(r=>[r.id,r.name]));
const rows=new Map();
for(const device of devices){
  const row=document.createElement('div');row.className='device-row';
  const select=document.createElement('button');select.className='device-select';select.dataset.deviceSelect=device.id;select.setAttribute('aria-label',`调节${device.name}`);
  const icon=document.createElement('span');icon.className='device-icon';icon.innerHTML=BULB_SVG;
  const text=document.createElement('span');const name=document.createElement('span');name.className='device-name';name.textContent=device.name;const meta=document.createElement('span');meta.className='device-meta';text.append(name,meta);select.append(icon,text);
  select.addEventListener('click',()=>store.select(device.id));
  const toggle=document.createElement('button');toggle.className='device-toggle';toggle.dataset.deviceToggle=device.id;toggle.setAttribute('role','switch');toggle.setAttribute('aria-label',`${device.name}开关`);toggle.addEventListener('click',()=>{store.select(device.id);store.toggle(device.id)});
  row.append(select,toggle);$('device-list').append(row);rows.set(device.id,{row,select,toggle,meta});
}
const viewOptions={canvas:$('scene'),container:$('viewport'),roomLayer:$('room-labels'),lampLayer:$('lamp-labels'),house,devices,onLamp:id=>{store.select(id);store.toggle(id)}};
let view=createHouseView({...viewOptions,profile:designProfile});
const sceneInfo={home:['回家场景','客餐厅与电竞房灯光开启'],movie:['观影场景','降低环境亮度，保留柔和灯光'],away:['离家场景','所有模拟灯光已关闭'],custom:['自定义','按你的设置调整灯光']};
function render(state){
  $('on-count').textContent=String(Object.values(state.devices).filter(s=>s.on).length);
  for(const device of devices){const s=state.devices[device.id],els=rows.get(device.id);els.row.classList.toggle('on',s.on);els.row.classList.toggle('selected',state.selectedId===device.id);els.toggle.setAttribute('aria-checked',String(s.on));els.select.setAttribute('aria-pressed',String(state.selectedId===device.id));els.meta.textContent=`${roomNames[device.roomId]||device.roomId} · ${s.on?`${s.brightness}%`:'已关闭'}`;}
  const selected=devices.find(d=>d.id===state.selectedId);
  $('selected-name').textContent=selected?.name||'选择一盏灯';$('brightness').disabled=!selected;
  const brightness=selected?state.devices[selected.id].brightness:0;$('brightness').value=brightness;$('brightness-value').innerHTML=`${brightness}<span>%</span>`;
  $('current-scene').textContent=sceneInfo[state.scene][0];$('scene-description').textContent=sceneInfo[state.scene][1];
  document.querySelectorAll('[data-scene]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.scene===state.scene)));
  view.applyState(state);
}
store.subscribe(render);if(!store.getState().selectedId)store.select(devices[0].id);render(store.getState());
$('brightness').addEventListener('input',e=>{const id=store.getState().selectedId;if(id)store.setBrightness(id,Number(e.target.value));});
document.querySelectorAll('[data-scene]').forEach(button=>button.addEventListener('click',()=>store.applyScene(button.dataset.scene)));
const viewTitles={overview:['全屋视图','01'],top:['平面视图','02'],living:['客餐厅','03'],studio:['电竞房','04'],bedroom:['次卧','05']};
function selectView(name){currentViewName=name;view.setView(name);document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===name)));$('view-title').replaceChildren(document.createTextNode(viewTitles[name][0]));const no=document.createElement('span');no.textContent=viewTitles[name][1];$('view-title').append(no);}
document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>selectView(b.dataset.view)));
$('reset-camera').addEventListener('click',()=>selectView('overview'));
$('cutaway').addEventListener('change',e=>view.setCutaway(e.target.checked));
$('cad-overlay').addEventListener('change',e=>view.setCad(e.target.checked));
$('room-label-toggle').addEventListener('change',e=>view.setLabels(e.target.checked));
$('designer-mode').addEventListener('change',e=>{
  view.dispose();view=createHouseView({...viewOptions,profile:e.target.checked?designProfile:null});
  view.setNight(night);view.setCutaway($('cutaway').checked);view.setCad($('cad-overlay').checked);view.setLabels($('room-label-toggle').checked);view.setView(currentViewName,false);view.applyState(store.getState());
  document.body.dataset.designer=String(e.target.checked);
});
$('lighting-mode').addEventListener('click',()=>{night=!night;view.setNight(night);document.querySelector('.stage').classList.toggle('night',night);$('lighting-mode').setAttribute('aria-pressed',String(night));$('lighting-mode-label').textContent=night?'日间':'夜景';});
function toast(message){clearTimeout(toastTimer);$('toast').textContent=message;$('toast').classList.add('visible');toastTimer=setTimeout(()=>$('toast').classList.remove('visible'),2600);}
$('reset-state').addEventListener('click',()=>{store.reset();toast('已恢复回家场景');});
function download(data,filename){const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=filename;a.click();setTimeout(()=>URL.revokeObjectURL(url),2000);}
$('export-mapping').addEventListener('click',()=>{download(exportEntityMapping(devices),'wuhan-device-mapping.json');toast('已导出待绑定的设备映射');});
$('source-open').addEventListener('click',()=>$('source-dialog').showModal());$('source-close').addEventListener('click',()=>$('source-dialog').close());
$('source-dialog').addEventListener('click',e=>{if(e.target===$('source-dialog')){const r=e.target.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)e.target.close();}});
$('assumptions').replaceChildren();for(const note of [...house.meta.assumptions,...designProfile.limitations]){const li=document.createElement('li');li.textContent=note;$('assumptions').append(li);}
$('design-open').addEventListener('click',()=>$('design-dialog').showModal());$('design-close').addEventListener('click',()=>$('design-dialog').close());
document.body.dataset.designer='true';
$('loading').hidden=true;document.body.dataset.ready='true';
window.addEventListener('pagehide',()=>{store.dispose();view.dispose();clearTimeout(toastTimer)},{once:true});
