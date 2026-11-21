import test from 'node:test';
import assert from 'node:assert/strict';

const api = await import('../state.mjs').catch(error => {
  if (error.code === 'ERR_MODULE_NOT_FOUND') return {};
  throw error;
});
const fixture = [
  {id:'living-main',name:'客厅主灯',roomId:'living',position:[3.4,2.6,5.25],entityId:null},
  {id:'dining-pendant',name:'餐厅吊灯',roomId:'dining',position:[8.2,2.2,5.5],entityId:null},
  {id:'studio-main',name:'电竞房主灯',roomId:'studio',position:[3.38,2.6,8.45],entityId:null},
  {id:'studio-desk',name:'电竞房桌面灯',roomId:'studio',position:[2.4,1.2,9.3],entityId:null},
];
const values = store => Object.values(store.getState().devices).map(item=>item.brightness);
function store(options) {
  assert.equal(typeof api.createStore,'function','createStore must be implemented');
  return api.createStore(fixture,options);
}
function memoryStorage(initial={}) {
  const data = new Map(Object.entries(initial));
  return {data,getItem:key=>data.get(key)??null,setItem:(key,value)=>data.set(key,value)};
}

test('starts in explicitly simulated home mode with the agreed brightness',()=>{
  const s=store();
  assert.equal(s.getState().mode,'simulation');
  assert.equal(s.getState().scene,'home');
  assert.equal(s.getState().selectedId,null);
  assert.deepEqual(values(s),[100,75,65,45]);
  assert.ok(Object.values(s.getState().devices).every(d=>d.on));
});

test('toggle restores the last nonzero level after dimming to zero',()=>{
  const s=store();
  s.setBrightness('living-main',32);
  s.setBrightness('living-main',0);
  assert.deepEqual(s.getState().devices['living-main'],{on:false,brightness:0});
  s.toggle('living-main');
  assert.deepEqual(s.getState().devices['living-main'],{on:true,brightness:32});
  s.toggle('living-main');
  s.toggle('living-main');
  assert.equal(s.getState().devices['living-main'].brightness,32);
  assert.equal(s.getState().scene,'custom');
});

test('movie, away, and home scenes affect every light consistently',()=>{
  const s=store();
  s.applyScene('movie');
  assert.deepEqual(values(s),[15,0,0,10]);
  assert.equal(s.getState().devices['dining-pendant'].on,false);
  s.applyScene('away');
  assert.deepEqual(values(s),[0,0,0,0]);
  s.toggle('studio-main');
  assert.equal(s.getState().devices['studio-main'].brightness,65);
  s.applyScene('home');
  assert.deepEqual(values(s),[100,75,65,45]);
  assert.equal(s.getState().scene,'home');
});

test('brightness clamps finite numbers and rejects strings and nonfinite input',()=>{
  const s=store();
  s.setBrightness('living-main',130);
  assert.equal(s.getState().devices['living-main'].brightness,100);
  s.setBrightness('living-main',-4);
  assert.equal(s.getState().devices['living-main'].brightness,0);
  s.setBrightness('living-main',27.4);
  assert.equal(s.getState().devices['living-main'].brightness,27);
  for(const bad of [NaN,Infinity,-Infinity,'50',null,undefined,{},true]) s.setBrightness('living-main',bad);
  assert.equal(s.getState().devices['living-main'].brightness,27);
});

test('unknown device IDs and scene names have no effect or notification',()=>{
  const s=store();let notifications=0;s.subscribe(()=>notifications++);
  const before=s.getState();
  for(const id of ['missing','__proto__','constructor',null,{},undefined]){
    s.toggle(id);s.select(id);s.setBrightness(id,30);
  }
  s.applyScene('unknown');
  assert.deepEqual(s.getState(),before);
  assert.equal(notifications,0);
});

test('selection can be cleared and does not change the light scene',()=>{
  const s=store();s.select('living-main');
  assert.equal(s.getState().selectedId,'living-main');
  assert.equal(s.getState().scene,'home');
  s.select(null);assert.equal(s.getState().selectedId,null);
});

test('state snapshots and subscriber snapshots cannot mutate internal state',()=>{
  const s=store();const snapshot=s.getState();
  snapshot.devices['living-main'].brightness=3;snapshot.mode='live';
  assert.equal(s.getState().devices['living-main'].brightness,100);
  let otherSnapshot;
  s.subscribe(v=>{v.devices['living-main'].brightness=7;});
  s.subscribe(v=>{otherSnapshot=v;});
  s.toggle('living-main');
  assert.equal(s.getState().devices['living-main'].brightness,0);
  assert.equal(otherSnapshot.devices['living-main'].brightness,0);
  assert.equal(s.getState().mode,'simulation');
});

test('subscribers receive changes only and unsubscribe and disposal stop delivery',()=>{
  const s=store();let calls=0;const off=s.subscribe(()=>calls++);
  s.applyScene('home');assert.equal(calls,0);
  s.select('living-main');assert.equal(calls,1);
  s.select('living-main');assert.equal(calls,1);
  off();s.toggle('living-main');assert.equal(calls,1);
  s.subscribe(()=>calls++);const before=s.getState();s.dispose();
  s.toggle('living-main');s.applyScene('away');s.reset();
  assert.deepEqual(s.getState(),before);assert.equal(calls,1);
});

test('persists only the versioned demo key and restores remembered brightness',()=>{
  const storage=memoryStorage({'unrelated-key':'keep'});const s=store({storage});
  s.setBrightness('living-main',36);s.toggle('living-main');s.select('studio-main');
  assert.deepEqual([...storage.data.keys()].sort(),['unrelated-key','wuhan-twin-demo-v1']);
  const restored=store({storage});
  assert.equal(restored.getState().selectedId,'studio-main');
  assert.deepEqual(restored.getState().devices['living-main'],{on:false,brightness:0});
  restored.toggle('living-main');assert.equal(restored.getState().devices['living-main'].brightness,36);
  assert.equal(storage.data.get('unrelated-key'),'keep');
});

test('invalid JSON, versions, live mode, and nonobject storage all fall back safely',()=>{
  for(const raw of ['{bad','null','[]','42',JSON.stringify({version:2,mode:'simulation'}),JSON.stringify({version:1,mode:'live',devices:{}})]){
    const s=store({storage:memoryStorage({'wuhan-twin-demo-v1':raw})});
    assert.equal(s.getState().mode,'simulation');assert.deepEqual(values(s),[100,75,65,45]);
  }
});

test('restore admits only known devices and valid state fields',()=>{
  const raw='{"version":1,"mode":"simulation","selectedId":"missing","scene":"away","devices":{"living-main":{"on":true,"brightness":44},"dining-pendant":{"on":true,"brightness":"99"},"studio-main":{"on":false,"brightness":20},"studio-desk":{"on":true,"brightness":999},"__proto__":{"polluted":true},"alien":{"on":true,"brightness":25}},"lastBrightness":{"living-main":-9,"dining-pendant":"40"}}';
  const s=store({storage:memoryStorage({'wuhan-twin-demo-v1':raw})});
  assert.deepEqual(values(s),[44,75,65,45]);
  assert.equal(s.getState().selectedId,null);assert.equal(s.getState().scene,'custom');
  assert.equal(s.getState().devices.alien,undefined);assert.equal({}.polluted,undefined);
  s.toggle('living-main');s.toggle('living-main');
  assert.equal(s.getState().devices['living-main'].brightness,44);
});

test('storage access failure does not break light controls',()=>{
  const storage={getItem(){throw new Error('blocked');},setItem(){throw new Error('quota');}};
  const s=store({storage});s.toggle('living-main');
  assert.equal(s.getState().devices['living-main'].on,false);
});

test('reset restores defaults and clears selected device',()=>{
  const s=store();s.select('living-main');s.applyScene('movie');s.reset();
  assert.deepEqual(values(s),[100,75,65,45]);
  assert.equal(s.getState().selectedId,null);assert.equal(s.getState().scene,'home');
});

test('mapping export remains explicitly disconnected with null entity IDs',()=>{
  assert.equal(typeof api.exportEntityMapping,'function','mapping exporter must be implemented');
  const source=structuredClone(fixture);source[0].entityId='light.accidental_real';
  const mapping=api.exportEntityMapping(source);
  assert.equal(mapping.mode,'simulation');assert.equal(mapping.connected,false);
  assert.equal(mapping.schemaVersion,1);
  assert.ok(mapping.devices.every(d=>d.entityId===null));
  assert.ok(mapping.devices.every(d=>d.provenance.includes('模拟')));
  mapping.devices[0].position[0]=999;
  assert.equal(source[0].position[0],3.4);
});
