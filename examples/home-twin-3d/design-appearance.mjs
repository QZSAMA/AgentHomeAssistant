import * as THREE from './vendor/three.module.js';

// All floor maps represent one square metre. Keep their material color white;
// the photographed palette is already baked into these local canvas drawings.
function canvas(size=1024) {
  const surface=document.createElement('canvas');surface.width=surface.height=size;
  return [surface,surface.getContext('2d')];
}
function texture(surface,repeat=true) {
  const map=new THREE.CanvasTexture(surface);
  map.colorSpace=THREE.SRGBColorSpace;
  if(repeat)map.wrapS=map.wrapT=THREE.RepeatWrapping;
  map.repeat.set(1,1);map.anisotropy=8;
  return map;
}
function random(seed=1) {
  let n=seed>>>0;
  return ()=>{n=(Math.imul(n,1664525)+1013904223)>>>0;return n/4294967296;};
}
function mod(n,m){return ((n%m)+m)%m;}

function plank(ctx,x,y,length,width,vertical,seed) {
  const rnd=random(seed),light=Math.round(3+rnd()*12);
  ctx.save();ctx.translate(x,y);if(vertical)ctx.rotate(Math.PI/2);
  ctx.fillStyle=`rgb(${211+light},${189+light},${158+light})`;
  ctx.fillRect(0,0,length,width);
  ctx.beginPath();ctx.rect(.7,.7,length-1.4,width-1.4);ctx.clip();
  // Long, slightly wavy fibres run along each plank, never across the joint.
  for(let i=0;i<34;i++){
    const yy=rnd()*width,amp=1+rnd()*3;
    ctx.beginPath();ctx.moveTo(-3,yy);
    ctx.bezierCurveTo(length*.3,yy+amp,length*.65,yy-amp,length+3,yy+amp*.3);
    ctx.strokeStyle=`rgba(99,65,30,${.035+rnd()*.075})`;
    ctx.lineWidth=.4+rnd()*.65;ctx.stroke();
  }
  for(let i=0;i<9;i++){
    const xx=rnd()*length,yy=rnd()*width;
    ctx.beginPath();ctx.ellipse(xx,yy,8+rnd()*28,.6+rnd()*1.4,0,0,Math.PI*2);
    ctx.strokeStyle='rgba(102,67,29,.035)';ctx.lineWidth=.5;ctx.stroke();
  }
  ctx.restore();
  ctx.save();ctx.translate(x,y);if(vertical)ctx.rotate(Math.PI/2);
  ctx.strokeStyle='rgba(100,76,46,.30)';ctx.lineWidth=.85;
  ctx.strokeRect(.45,.45,length-.9,width-.9);ctx.restore();
}

export function createFloorTexture(kind='wood') {
  const [surface,ctx]=canvas(),s=surface.width;
  if(kind==='herringbone'){
    ctx.fillStyle='#c7af8c';ctx.fillRect(0,0,s,s);
    // Two perpendicular rectangles form an L. Translating the L by (L,L)
    // and (-W,W) tiles the plane; after 45° rotation their repeat is exactly
    // 0.5 m vertically and 0.125 m horizontally in this 1 m square map.
    const width=s/(Math.SQRT2*8),length=width*4;
    ctx.save();ctx.rotate(Math.PI/4);
    for(let row=-6;row<=6;row++)for(let col=-16;col<=16;col++){
      const x=row*length-col*width,y=row*length+col*width;
      const seed=mod(row,2)*751+mod(col,8)*97+31;
      plank(ctx,x,y,length,width,false,seed);
      plank(ctx,x+length+width,y,length,width,true,seed+443);
    }
    ctx.restore();
  }else if(kind==='tile'){
    ctx.fillStyle='#dfdfd8';ctx.fillRect(0,0,s,s);
    const rnd=random(731);
    for(let i=0;i<12000;i++){
      const v=130+Math.floor(rnd()*90);
      ctx.fillStyle=`rgba(${v},${v},${v-5},.035)`;
      ctx.fillRect(rnd()*s,rnd()*s,1+rnd()*4,1+rnd()*2);
    }
    ctx.strokeStyle='#c3c3ba';ctx.lineWidth=3;ctx.strokeRect(1.5,1.5,s-3,s-3);
    ctx.strokeStyle='rgba(255,255,255,.35)';ctx.lineWidth=1;
    ctx.strokeRect(4,4,s-8,s-8);
  }else{
    ctx.fillStyle='#cbb08b';ctx.fillRect(0,0,s,s);
    for(let row=0;row<5;row++)for(let col=-1;col<2;col++){
      plank(ctx,col*s+(row%2)*s*.5,row*s/5,s,s/5,false,113+row*29+mod(col,2)*431);
    }
  }
  return texture(surface);
}

export function createWovenTexture() {
  const [surface,ctx]=canvas(512);ctx.fillStyle='#d9dbd6';ctx.fillRect(0,0,512,512);
  const rnd=random(183);
  for(let y=0;y<512;y+=4)for(let x=0;x<512;x+=4){
    const bright=208+Math.floor(rnd()*38),over=((x+y)/4)%2===0;
    ctx.fillStyle=`rgb(${bright},${bright},${bright-2})`;
    ctx.fillRect(x+(over?0:1),y+(over?1:0),over?4:2,over?2:4);
  }
  ctx.globalAlpha=.16;ctx.strokeStyle='#ffffff';ctx.lineWidth=.5;
  for(let n=0;n<512;n+=4){ctx.beginPath();ctx.moveTo(n+.5,0);ctx.lineTo(n+.5,512);ctx.stroke();}
  ctx.globalAlpha=1;return texture(surface);
}

export function createRugTexture() {
  const [surface,ctx]=canvas();const s=surface.width;
  ctx.fillStyle='#f1eee2';ctx.fillRect(0,0,s,s);
  const cells=[
    [.02,.06,.11,.33,'#1c2624'],[.14,.06,.24,.08,'#e0bd35'],
    [.40,.04,.10,.19,'#afc9c3'],[.52,.06,.16,.09,'#bf3928'],
    [.72,.04,.12,.30,'#f3d25e'],[.86,.06,.11,.38,'#6dabb1'],
    [.04,.43,.12,.12,'#d94731'],[.18,.25,.16,.07,'#92b6b4'],
    [.27,.53,.10,.23,'#d9b63c'],[.44,.37,.21,.09,'#e7c7a1'],
    [.67,.51,.14,.13,'#202927'],[.84,.61,.13,.11,'#d23958'],
    [.04,.76,.12,.20,'#90c8c5'],[.21,.86,.24,.10,'#e8bb39'],
    [.50,.80,.10,.16,'#21302c'],[.64,.88,.19,.07,'#2d9263'],
  ];
  for(const [x,y,w,h,c] of cells){ctx.fillStyle=c;ctx.fillRect(x*s,y*s,w*s,h*s);}
  const rnd=random(729);
  for(let i=0;i<16000;i++){
    ctx.fillStyle=i%2?'rgba(255,255,255,.13)':'rgba(85,74,51,.07)';
    ctx.fillRect(rnd()*s,rnd()*s,1+rnd()*2,.65);
  }
  ctx.strokeStyle='#dedbce';ctx.lineWidth=8;ctx.strokeRect(4,4,s-8,s-8);
  return texture(surface,false);
}

export function bedParts(w,d,h) {
  if(![w,d,h].every(v=>Number.isFinite(v)&&v>0))throw new RangeError('Bed dimensions must be positive');
  const headDepth=Math.min(.075,d*.04),headHeight=Math.max(.9,h*1.7);
  const base=h*.30,mattress=h*.55,cover=h*.15;
  const innerWidth=w*.96,innerDepth=d-headDepth-.035;
  const pillowWidth=Math.min(.6,(innerWidth-.08)/2),pillowDepth=Math.min(.38,d*.2);
  return [
    {size:[w,base,d-headDepth],position:[0,base/2,headDepth/2],role:'wood'},
    {size:[w,headHeight,headDepth],position:[0,headHeight/2,-d/2+headDepth/2],role:'wood'},
    {size:[innerWidth,mattress,innerDepth],position:[0,base+mattress/2,headDepth/2],role:'fabric'},
    {size:[innerWidth,cover,innerDepth*.69],position:[0,h-cover/2,innerDepth*.155+headDepth/2],role:'linen'},
    ...[-1,1].map(side=>({size:[pillowWidth,.115,pillowDepth],position:[side*(pillowWidth+.045)/2,h+.0575,-d/2+headDepth+.035+pillowDepth/2],role:'white'})),
  ];
}

function monitorTexture(seed) {
  const [surface,ctx]=canvas(512),rnd=random(seed);
  const sky=ctx.createLinearGradient(0,0,512,512);
  sky.addColorStop(0,'#162842');sky.addColorStop(.5,'#3c2466');sky.addColorStop(1,'#207e92');
  ctx.fillStyle=sky;ctx.fillRect(0,0,512,512);
  for(let i=0;i<7;i++){
    ctx.beginPath();ctx.moveTo(-30,400-i*35);
    ctx.bezierCurveTo(100,80+rnd()*150,300,440-rnd()*160,560,20+i*32);
    ctx.lineWidth=16+i*8;ctx.strokeStyle=['#72dbda','#3d8bc1','#cd79cd'][i%3];ctx.globalAlpha=.26;ctx.stroke();
  }
  ctx.globalAlpha=.9;ctx.fillStyle='#e7f2f0';
  for(let i=0;i<48;i++){const x=rnd()*512,y=rnd()*512;ctx.fillRect(x,y,1.5,1.5);}
  ctx.globalAlpha=1;return texture(surface,false);
}

// The profile owns every world position. Decorative furniture never changes
// house.walls/rooms/openings, nor the user's accepted sofa orientation.
export function addDesignerDecor({root,house,profile={},materials={}}) {
  const group=new THREE.Group();group.name='designer-decor';root.add(group);
  const geometries=new Set(),ownedMaterials=new Set(),maps=new Set(),highPieces=[],reactive=[];
  const palette=profile.palette||{};
  const color=(key,fallback)=>palette[key]||fallback;
  const ownMap=map=>{maps.add(map);return map;};
  function material(value,extra={}){
    const m=new THREE.MeshStandardMaterial({color:value,roughness:.76,...extra});ownedMaterials.add(m);return m;
  }
  function mesh(parent,geometry,m,position=[0,0,0]){
    geometries.add(geometry);const o=new THREE.Mesh(geometry,m);o.position.set(...position);
    o.castShadow=true;o.receiveShadow=true;parent.add(o);return o;
  }
  const box=(p,size,m,pos)=>mesh(p,new THREE.BoxGeometry(...size),m,pos);
  const sphere=(p,scale,m,pos)=>{const o=mesh(p,new THREE.SphereGeometry(1,24,16),m,pos);o.scale.set(...scale);return o;};
  const cylinder=(p,top,bottom,height,m,pos)=>mesh(p,new THREE.CylinderGeometry(top,bottom,height,28),m,pos);
  function rod(p,a,b,r,m){
    const va=new THREE.Vector3(...a),vb=new THREE.Vector3(...b),dir=vb.clone().sub(va);
    const o=cylinder(p,r,r,dir.length(),m,va.clone().add(vb).multiplyScalar(.5).toArray());
    o.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),dir.normalize());return o;
  }

  for(const cfg of profile.decor||[]){
    if(!cfg||!Number.isFinite(cfg.x)||!Number.isFinite(cfg.z))continue;
    // Wall-mounted glass belongs to scene's wallStyles replacement. Never add
    // a second partition here, even if an older profile lists it as decor.
    if(cfg.type==='glass-partition')continue;
    const part=new THREE.Group();part.name=cfg.id||cfg.type;
    part.position.set(cfg.x,0,cfg.z);part.rotation.y=cfg.rotation||0;
    part.userData.provenance=cfg.provenance||'设计参考装饰示意';group.add(part);
    const w=Math.max(.05,cfg.width||.6),d=Math.max(.02,cfg.depth||.6),h=Math.max(.02,cfg.height||.8);
    if(cfg.type==='rug'){
      const m=material('#ffffff',{map:ownMap(createRugTexture()),roughness:1});
      const o=mesh(part,new THREE.PlaneGeometry(w,d),m,[0,h,0]);
      o.rotation.x=-Math.PI/2;o.castShadow=false;
    }else if(cfg.type==='accent-chair'){
      const map=ownMap(createWovenTexture());map.repeat.set(2,2);
      const fabric=material(cfg.color||color('blueFabric','#4d7e91'),{map,roughness:.96});
      const base=material(color('darkWood','#292620'));
      cylinder(part,w*.31,w*.34,h*.09,base,[0,h*.11,0]);
      sphere(part,[w*.49,h*.19,d*.48],fabric,[0,h*.43,-d*.04]);
      const back=sphere(part,[w*.46,h*.32,d*.19],fabric,[0,h*.68,d*.28]);back.rotation.x=-.24;
      for(const x of [-1,1])sphere(part,[w*.09,h*.14,d*.27],fabric,[x*w*.4,h*.48,d*.02]);
    }else if(cfg.type==='floor-lamp'){
      const red=material(cfg.color||color('redAccent','#bd3024'),{roughness:.31,metalness:.35});
      const steel=material(color('metal','#a8aba5'),{roughness:.29,metalness:.75});
      cylinder(part,w*.44,w*.46,.035,red,[0,.025,0]);
      const pivot=[0,h*.65,0],elbow=[w*.05,h*.96,0],tip=[w*1.18,h*.78,w*.1];
      rod(part,[0,.04,0],pivot,.012,steel);
      for(const offset of [-.018,.018]){
        rod(part,[pivot[0]+offset,pivot[1],pivot[2]],[elbow[0]+offset,elbow[1],elbow[2]],.008,steel);
        rod(part,[elbow[0]+offset,elbow[1],elbow[2]],[tip[0]+offset,tip[1],tip[2]],.008,steel);
      }
      for(const point of [pivot,elbow,tip])sphere(part,[.025,.025,.025],red,point);
      const shade=mesh(part,new THREE.CylinderGeometry(w*.24,w*.39,h*.145,32,1,true),red,[tip[0],tip[1]-h*.075,tip[2]]);
      shade.rotation.z=.18;
      const bulb=material('#fff0cd',{emissive:'#ffdc98',emissiveIntensity:.6,roughness:.2});
      const lightFace=mesh(part,new THREE.CircleGeometry(w*.34,32),bulb,[tip[0]-.015,tip[1]-h*.145,tip[2]]);
      lightFace.rotation.x=Math.PI/2;lightFace.castShadow=false;
      reactive.push({material:bulb,deviceId:cfg.deviceId||'living-main',intensity:.6});
    }else if(cfg.type==='monitors'){
      const metal=material(color('metal','#a8aba5'),{roughness:.33,metalness:.55});
      const bezel=material('#252d32',{roughness:.42}),keys=material('#e6e9e3');
      const displayWidth=Math.min(.72,w*.3),displayHeight=displayWidth*.625;
      const positions=Array.isArray(cfg.offsets)&&cfg.offsets.length?cfg.offsets:[-w*.34,w*.34];
      positions.forEach((x,index)=>{
        const centerY=h+.38;
        box(part,[displayWidth,displayHeight+.045,.045],bezel,[x,centerY,0]);
        const screenMap=ownMap(monitorTexture(983+index*331));
        const screenMat=material('#ffffff',{map:screenMap,emissiveMap:screenMap,emissive:'#ffffff',emissiveIntensity:.65,roughness:.35,side:THREE.DoubleSide});
        const screen=mesh(part,new THREE.PlaneGeometry(displayWidth-.022,displayHeight),screenMat,[x,centerY+.012,-.024]);
        screen.rotation.y=Math.PI;screen.castShadow=false;screen.userData.designerScreen=true;
        reactive.push({material:screenMat,deviceId:cfg.deviceId||'studio-desk',intensity:.85,screen:true});
        box(part,[.042,.19,.042],metal,[x,h+.16,.015]);
        box(part,[.25,.012,.17],metal,[x,h+.012,-.015]);
        box(part,[displayWidth*.85,.017,.145],keys,[x,h+.013,-d*.85]);
        const vertices=[];
        for(let col=1;col<12;col++){const xx=x-displayWidth*.425+col*displayWidth*.85/12;vertices.push(xx,h+.023,-d*.85-.068,xx,h+.023,-d*.85+.068);}
        for(let row=1;row<4;row++){const z=-d*.85-.0725+row*.145/4;vertices.push(x-displayWidth*.425,h+.023,z,x+displayWidth*.425,h+.023,z);}
        const linesGeometry=new THREE.BufferGeometry();linesGeometry.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));geometries.add(linesGeometry);
        const lineMat=new THREE.LineBasicMaterial({color:'#a8b1ad',transparent:true,opacity:.6});ownedMaterials.add(lineMat);
        part.add(new THREE.LineSegments(linesGeometry,lineMat));
        sphere(part,[.03,.018,.048],keys,[x+displayWidth*.57,h+.025,-d*.85]);
      });
    }else if(cfg.type==='studio-panels'){
      const side=w/6,triHeight=side*Math.sqrt(3)/2;
      const pattern=[[-2.5,0,0],[-2,1,0],[-1.5,0,1],[-1,-1,1],[-.5,0,0],[0,0,1],[.5,-1,1],[1,0,0],[1.5,0,1],[2,1,0],[2.5,0,1]];
      pattern.forEach(([col,row,flipped],index)=>{
        const shape=new THREE.Shape();shape.moveTo(-side*.47,-triHeight/3);shape.lineTo(side*.47,-triHeight/3);shape.lineTo(0,triHeight*2/3);shape.closePath();
        const faceColor=index<5?'#e4f7fa':index>6?'#f4d1ed':'#ecdbf3';
        const m=material(faceColor,{emissive:faceColor,emissiveIntensity:.8,roughness:.5,side:THREE.DoubleSide});
        const o=mesh(part,new THREE.ExtrudeGeometry(shape,{depth:d,bevelEnabled:true,bevelSegments:1,steps:1,bevelSize:.004,bevelThickness:.003}),m,[col*side,h+row*triHeight*.78,-d]);
        if(flipped)o.rotation.z=Math.PI;o.userData.designerPanel=true;
        reactive.push({material:m,deviceId:cfg.deviceId||'studio-desk',intensity:1});
      });
      highPieces.push(part);
    }
  }

  let disposed=false;
  return {
    setCutaway(value){if(!disposed)for(const piece of highPieces)piece.visible=!value;},
    applyState(state){
      if(disposed)return;
      for(const item of reactive){
        const device=state?.devices?.[item.deviceId];
        const level=device?(device.on?Math.max(0,Math.min(100,Number(device.brightness)||0))/100:0):1;
        item.material.emissiveIntensity=item.intensity*level;
        if(item.screen)item.material.color.set(level>0?'#ffffff':'#030506');
      }
    },
    dispose(){
      if(disposed)return;disposed=true;root.remove(group);
      geometries.forEach(g=>g.dispose());maps.forEach(t=>t.dispose());ownedMaterials.forEach(m=>m.dispose());
      group.clear();
    },
  };
}
