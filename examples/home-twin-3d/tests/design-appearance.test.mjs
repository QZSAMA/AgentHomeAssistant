import test from 'node:test';
import assert from 'node:assert/strict';
import {existsSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';

const moduleUrl=new URL('../design-appearance.mjs',import.meta.url);
const available=existsSync(moduleUrl);
const appearance=available?await import(moduleUrl):null;

test('designer appearance module is available',()=>{
  assert.ok(appearance,'Implement the independent designer appearance module');
});

for(const [w,d,h] of [[1.5,2,.52],[1.8,2,.52],[.9,1.9,.45]]){
  test(`bed parts stay inside ${w} × ${d} m footprint`,{skip:!available},()=>{
    const parts=appearance.bedParts(w,d,h);
    assert.ok(parts.length>=4,'Frame, mattress, headboard and linen are represented');
    for(const part of parts){
      assert.equal(part.size.length,3);
      assert.equal(part.position.length,3);
      assert.ok(part.size.every(n=>Number.isFinite(n)&&n>0));
      assert.ok(['wood','fabric','linen','white'].includes(part.role));
      const [sx,sy,sz]=part.size,[x,y,z]=part.position;
      assert.ok(x-sx/2>=-w/2-1e-9&&x+sx/2<=w/2+1e-9,`${part.role} crosses a side wall`);
      assert.ok(z-sz/2>=-d/2-1e-9&&z+sz/2<=d/2+1e-9,`${part.role} crosses the head/foot wall`);
      assert.ok(y-sy/2>=-1e-9,`${part.role} extends below the floor`);
    }
    const head=parts.find(p=>p.position[2]<-d*.35&&p.size[1]>h);
    assert.ok(head,'Headboard sits on the negative-z end within the footprint');
  });
}

function withCanvasDocument(fn){
  const previous=globalThis.document;
  globalThis.document={createElement(){
    const ctx=new Proxy({createLinearGradient(){return {addColorStop(){}};}},{get(target,key){return key in target?target[key]:(()=>{});}});
    return {width:0,height:0,getContext(){return ctx;}};
  }};
  try{return fn();}finally{if(previous===undefined)delete globalThis.document;else globalThis.document=previous;}
}

test('floor maps preserve metre UV scale and baked color space',{skip:!available},()=>withCanvasDocument(()=>{
  for(const kind of ['herringbone','tile','wood']){
    const map=appearance.createFloorTexture(kind);
    assert.equal(map.isCanvasTexture,true);assert.equal(map.colorSpace,THREE.SRGBColorSpace);
    assert.equal(map.wrapS,THREE.RepeatWrapping);assert.deepEqual(map.repeat.toArray(),[1,1]);map.dispose();
  }
}));

test('decor uses configured positions, responds to studio state, and cleans up',{skip:!available},()=>withCanvasDocument(()=>{
  assert.equal(typeof appearance.addDesignerDecor,'function');
  const root=new THREE.Group();
  const profile={decor:[
    {id:'rug-test',type:'rug',x:2,z:3,width:2,depth:2,height:.02},
    {id:'screens-test',type:'monitors',x:4,z:5,width:2.3,depth:.28,height:.92},
    {id:'panels-test',type:'studio-panels',x:4,z:6,width:2,depth:.035,height:1.85},
  ]};
  const api=appearance.addDesignerDecor({root,house:{},profile,materials:{}});
  const group=root.getObjectByName('designer-decor');assert.ok(group);
  assert.deepEqual(group.getObjectByName('rug-test').position.toArray(),[2,0,3]);
  const panels=group.getObjectByName('panels-test');
  api.setCutaway(true);assert.equal(panels.visible,false);
  api.setCutaway(false);assert.equal(panels.visible,true);
  const screens=[];group.traverse(o=>{if(o.userData.designerScreen)screens.push(o);});
  assert.equal(screens.length,2);
  api.applyState({devices:{'studio-desk':{on:false,brightness:0}}});
  assert.ok(screens.every(o=>o.material.emissiveIntensity===0));
  api.applyState({devices:{'studio-desk':{on:true,brightness:80}}});
  assert.ok(screens.every(o=>o.material.emissiveIntensity>0));
  api.dispose();assert.equal(root.children.length,0);
}));
