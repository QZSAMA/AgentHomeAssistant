import * as THREE from 'three';
import {OrbitControls} from './vendor/OrbitControls.js';
import {createFloorTexture,createWovenTexture,bedParts,addDesignerDecor} from './design-appearance.mjs';

export const BULB_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 17h6M9.5 20h5M8.5 13.5a5.5 5.5 0 1 1 7 0c-1.1.9-1.5 1.8-1.5 3.5h-4c0-1.7-.4-2.6-1.5-3.5Z"/></svg>';

export function createHouseView({canvas,container,roomLayer,lampLayer,house,devices,onLamp,profile=null}) {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const renderer = new THREE.WebGLRenderer({canvas,antialias:true,alpha:false});
  renderer.setPixelRatio(Math.min(devicePixelRatio,1.8));
  renderer.outputColorSpace=THREE.SRGBColorSpace;
  renderer.toneMapping=THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure=.92;
  renderer.shadowMap.enabled=true;
  renderer.shadowMap.type=THREE.PCFSoftShadowMap;
  const scene=new THREE.Scene();scene.background=new THREE.Color('#eae7df');
  const camera=new THREE.PerspectiveCamera(36,1,.08,120);
  const controls=new OrbitControls(camera,canvas);
  controls.enableDamping=!reduced;controls.dampingFactor=.12;
  controls.minDistance=2.4;controls.maxDistance=38;controls.maxPolarAngle=Math.PI*.49;
  controls.target.set(0,0,0);
  const xs=house.footprint.map(p=>p[0]),zs=house.footprint.map(p=>p[1]);
  const cx=(Math.min(...xs)+Math.max(...xs))/2,cz=(Math.min(...zs)+Math.max(...zs))/2;
  const root=new THREE.Group();root.position.set(-cx,0,-cz);scene.add(root);
  const mat=(color,extra={})=>new THREE.MeshStandardMaterial({color,roughness:.82,...extra});
  const m={wall:mat('#eee9de'),slab:mat('#b4b7a5'),floor:mat('#d9d5c8'),wood:mat('#ac8960'),oak:mat('#c8b08b'),fabric:mat('#b4bba4'),linen:mat('#e9e4d7'),dark:mat('#424d40'),metal:mat('#626f5e',{metalness:.45,roughness:.35}),counter:mat('#eeece3'),white:mat('#e6e7dd'),glass:mat('#9eb5a8',{transparent:true,opacity:.22,depthWrite:false,side:THREE.DoubleSide,roughness:.12}),windowFrame:mat('#81917c'),screen:mat('#29372d',{emissive:'#4e6653',emissiveIntensity:.25})};
  if(profile){m.wall.color.set(profile.palette.wall);m.oak.color.set(profile.palette.oak);m.wood.color.set(profile.palette.oak);m.dark.color.set(profile.palette.darkWood);m.white.color.set(profile.palette.white);m.windowFrame.color.set(profile.palette.oak);m.screen.color.set('#16191a');m.screen.emissive.set('#202c32');}
  const wovenTexture=profile?createWovenTexture():null;
  const ambient=new THREE.HemisphereLight('#fffaf2','#929b93',1.7);scene.add(ambient);
  const sun=new THREE.DirectionalLight('#fff6e6',2.6);sun.position.set(-8,16,8);sun.castShadow=true;
  sun.shadow.mapSize.set(2048,2048);Object.assign(sun.shadow.camera,{left:-12,right:12,top:12,bottom:-12,near:.5,far:40});sun.shadow.normalBias=.045;sun.shadow.bias=-.0003;scene.add(sun);
  const fill=new THREE.DirectionalLight('#ecf0ed',.7);fill.position.set(10,7,-10);scene.add(fill);
  const ground=new THREE.Mesh(new THREE.PlaneGeometry(160,160),new THREE.MeshBasicMaterial({color:'#eae7df',toneMapped:false}));
  ground.rotation.x=-Math.PI/2;ground.position.y=-.21;scene.add(ground);
  const groundShadow=new THREE.Mesh(new THREE.PlaneGeometry(40,40),new THREE.ShadowMaterial({color:'#3e4a34',opacity:.13}));groundShadow.rotation.x=-Math.PI/2;groundShadow.position.y=-.205;groundShadow.receiveShadow=true;scene.add(groundShadow);
  const wallMeshes=[],upperPieces=[],windowPieces=[],partitionPieces=[],tallFurniture=[],pickables=[],labels=[],lampViews=new Map();
  let disposed=false,night=false,cutaway=true,showLabels=true,transition=null,currentView='overview',lastState=null,frame=0;

  function box(parent,size,pos,material) {
    const mesh=new THREE.Mesh(new THREE.BoxGeometry(...size),material);
    mesh.position.set(...pos);mesh.castShadow=true;mesh.receiveShadow=true;parent.add(mesh);return mesh;
  }
  function cyl(parent,rt,rb,height,pos,material,segments=24) {
    const mesh=new THREE.Mesh(new THREE.CylinderGeometry(rt,rb,height,segments),material);mesh.position.set(...pos);mesh.castShadow=true;mesh.receiveShadow=true;parent.add(mesh);return mesh;
  }
  function softBox(parent,size,pos,material,radius=.045){
    const [w,h,d]=size,r=Math.min(radius,w/4,h/4,d/4),s=new THREE.Shape();
    s.moveTo(-w/2+r,-h/2+r);s.lineTo(w/2-r,-h/2+r);s.lineTo(w/2-r,h/2-r);s.lineTo(-w/2+r,h/2-r);s.closePath();
    const geometry=new THREE.ExtrudeGeometry(s,{depth:d-2*r,steps:1,bevelEnabled:true,bevelSegments:3,bevelSize:r,bevelThickness:r});geometry.translate(0,0,-d/2+r);
    const mesh=new THREE.Mesh(geometry,material);mesh.position.set(...pos);mesh.castShadow=true;mesh.receiveShadow=true;parent.add(mesh);return mesh;
  }
  function shape(points) {
    const s=new THREE.Shape();points.forEach(([x,z],i)=>i?s.lineTo(x,-z):s.moveTo(x,-z));s.closePath();return s;
  }
  function floor(points,material,y=.012) {
    const mesh=new THREE.Mesh(new THREE.ShapeGeometry(shape(points)),material);mesh.rotation.x=-Math.PI/2;mesh.position.y=y;mesh.receiveShadow=true;root.add(mesh);return mesh;
  }
  function segment(parent,a,b,width,height,material,base=0) {
    const dx=b[0]-a[0],dz=b[1]-a[1],len=Math.hypot(dx,dz);
    if(len<.001)return null;
    const mesh=box(parent,[len,height,width],[(a[0]+b[0])/2,base+height/2,(a[1]+b[1])/2],material);mesh.rotation.y=-Math.atan2(dz,dx);return mesh;
  }
  function addScalableWall(a,b,thickness,height,material=m.wall,base=0) {
    const mesh=segment(root,a,b,thickness,height,material,base);if(mesh)wallMeshes.push({mesh,height,base});return mesh;
  }
  const slab=new THREE.Mesh(new THREE.ExtrudeGeometry(shape(house.footprint),{depth:.18,bevelEnabled:false}),m.slab);slab.rotation.x=-Math.PI/2;slab.position.y=-.18;slab.receiveShadow=true;slab.castShadow=true;root.add(slab);
  const floorTextures=new Map();
  function floorTexture(kind){if(!floorTextures.has(kind))floorTextures.set(kind,createFloorTexture(kind));return floorTextures.get(kind);}
  if(profile){m.floor.color.set('#ffffff');m.floor.map=floorTexture('herringbone');}
  floor(house.footprint,m.floor,.001);
  const floorColors={living:'#d7c5a8',dining:'#d8d2bd',studio:'#b8bba6',master:'#d0c7b6',bedroom:'#cdc7b8',bathroom:'#c2cbc3','guest-bath':'#c2cbc3',kitchen:'#d6d6c9',entry:'#d6d3c6'};
  const roomMaterials=new Map();
  for(const room of house.rooms) {
    const style=profile?.roomStyles?.[room.id];
    const material=style?mat('#ffffff',{map:floorTexture(style.floor||'wood')}):mat(floorColors[room.id]||'#d4d5c8');roomMaterials.set(room.id,material);floor(room.polygon,material);
    const el=document.createElement('span');el.className='room-label'+(room.interactive?'':' context');el.textContent=room.name;roomLayer.append(el);
    // Keep labels away from the central light markers and primary furniture.
    const z=room.center[1]+(room.id==='studio'?-1.0:room.id==='living'?-.95:room.id==='dining'?.9:.12);
    labels.push({el,position:new THREE.Vector3(room.center[0]-cx,.08,z-cz)});
  }
  for(const wall of house.walls) {
    const style=profile?.wallStyles?.[wall.id];
    if(style?.kind==='wood-framed-glass'){
      addScalableWall(wall.a,wall.b,wall.thickness,style.baseHeight,m.wall);
      const top=new THREE.Group();root.add(top);partitionPieces.push(top);
      const wood=mat(style.frameColor),glass=mat('#bdcbc3',{transparent:true,opacity:.14,depthWrite:false,side:THREE.DoubleSide,roughness:.08});
      segment(top,wall.a,wall.b,.065,style.glassTop-style.baseHeight,glass,style.baseHeight);
      for(const y of [style.baseHeight,style.glassTop])segment(top,wall.a,wall.b,.19,.075,wood,y);
      for(let i=0;i<=3;i++)box(top,[.045,style.glassTop-style.baseHeight,.045],[wall.a[0]+(wall.b[0]-wall.a[0])*i/3,(style.glassTop+style.baseHeight)/2,wall.a[1]+(wall.b[1]-wall.a[1])*i/3],wood);
      const beam=segment(root,wall.a,wall.b,wall.thickness,wall.height-style.glassTop,m.wall,style.glassTop);upperPieces.push(beam);
    }else{
      const material=wall.kind==='glass'?m.glass:m.wall;
      addScalableWall(wall.a,wall.b,wall.thickness,wall.height,material);
    }
  }
  for(const opening of house.openings) {
    const {a,b,height,sill}=opening;const len=Math.hypot(b[0]-a[0],b[1]-a[1]);
    if(opening.kind==='window') {
      if(sill>0)addScalableWall(a,b,.20,sill,m.wall);
      const windowGroup=new THREE.Group();root.add(windowGroup);windowPieces.push(windowGroup);
      segment(windowGroup,a,b,.045,height,m.glass,sill);
      for(const y of [sill+.02,sill+height-.02])segment(windowGroup,a,b,.07,.045,m.windowFrame,y);
      const n=Math.max(1,Math.ceil(len/1.2));
      for(let i=0;i<=n;i++)box(windowGroup,[.045,height,.045],[a[0]+(b[0]-a[0])*i/n,sill+height/2,a[1]+(b[1]-a[1])*i/n],m.windowFrame);
      const remain=Math.max(0,2.65-sill-height);if(remain>.01){const header=segment(root,a,b,.20,remain,m.wall,sill+height);upperPieces.push(header);}
    } else {
      // Keep openings unblocked. Thresholds show location, not a verified door swing.
      const threshold=segment(root,a,b,.15,.018,m.oak,.015);threshold.castShadow=false;
      const header=segment(root,a,b,.13,2.65-height,m.wall,height);upperPieces.push(header);
    }
  }

  function legs(parent,w,d,h) {
    for(const x of [-w*.38,w*.38])for(const z of [-d*.35,d*.35])box(parent,[.045,h,.045],[x,h/2,z],m.dark);
  }
  for(const f of house.furniture||[]) {
    const group=new THREE.Group();group.position.set(f.x,0,f.z);group.rotation.y=-(f.rotation||0);root.add(group);
    const w=f.width,d=f.depth,h=f.height;
    const style=profile?.furnitureStyles?.[f.id]||{},finish=style.finish||{};
    const wood=finish.wood?mat(finish.wood):m.wood,fabric=finish.fabric?mat(finish.fabric,{map:wovenTexture,roughness:.94}):m.fabric;
    const front=finish.front?mat(finish.front):wood,body=finish.body?mat(finish.body):wood;
    if(h>1.5)tallFurniture.push({group,height:h});
    if(f.type==='sofa') {
      legs(group,w,d,.13);softBox(group,[w,.24,d],[0,.25,0],fabric);
      softBox(group,[w,.40,.15],[0,.57,d/2-.075],fabric);
      for(const x of [-w/2+.065,w/2-.065])softBox(group,[.13,.32,d],[x,.47,0],fabric);
      const count=3,seatW=(w-.3)/count;
      for(let i=0;i<count;i++){
        softBox(group,[seatW-.025,.14,d-.22],[-w/2+.15+seatW*(i+.5),.43,-.04],profile?fabric:m.linen);
        const cushion=softBox(group,[seatW-.07,.30,.13],[-w/2+.15+seatW*(i+.5),.66,d/2-.19],profile?fabric:m.linen);cushion.rotation.x=.08;
      }
      if(style.pillowColor){const pillow=softBox(group,[.38,.26,.12],[-w*.27,.62,.06],mat(style.pillowColor,{map:wovenTexture}));pillow.rotation.z=-.18;}
    } else if(['table','desk','bar'].includes(f.type)) {
      if(style.shape==='round-glass'){
        const glass=new THREE.MeshPhysicalMaterial({color:'#e5f2ed',transparent:true,opacity:.32,roughness:.08,metalness:.12,side:THREE.DoubleSide});
        const radius=Math.max(w,d)*.47;cyl(group,radius,radius,.024,[0,h,0],glass,64);
        for(const angle of [0,2.094,4.189])box(group,[.055,h-.02,.12],[Math.cos(angle)*radius*.6,(h-.02)/2,Math.sin(angle)*radius*.6],glass);
        const ring=new THREE.Mesh(new THREE.TorusGeometry(radius,.006,6,64),m.metal);ring.rotation.x=Math.PI/2;ring.position.y=h;group.add(ring);
      }else{
        box(group,[w,.07,d],[0,h-.035,0],wood);legs(group,w,d,h-.07);
      }
      if(f.id==='studio-bar'&&finish.front){box(group,[w*.22,h-.08,d*.82],[-w*.36,(h-.08)/2,d*.06],front);box(group,[w*.22,h-.08,d*.82],[w*.36,(h-.08)/2,d*.06],front);}
      if(f.id==='living-coffee'){cyl(group,.10,.10,.045,[-.25,h+.02,0],m.counter);box(group,[.25,.025,.18],[.22,h+.015,0],m.linen);}
      if(f.id==='dining-table'){cyl(group,.09,.10,.23,[0,h+.115,0],m.fabric);cyl(group,.035,.035,.26,[0,h+.32,0],m.dark,10);}
    } else if(f.type==='chair') {
      legs(group,w,d,.45);softBox(group,[w,.08,d],[0,.47,0],fabric);softBox(group,[w,h-.48,.06],[0,(h+.48)/2,-d/2+.03],fabric);
    } else if(f.type==='bed') {
      const bedMaterials={wood,fabric,linen:style.linenColor?mat(style.linenColor,{map:wovenTexture}):m.linen,white:m.white};
      for(const part of bedParts(w,d,h))softBox(group,part.size,part.position,bedMaterials[part.role],.025);
      if(style.headboardFabric)softBox(group,[w-.14,.37,.035],[0,.58,-d/2+.092],mat(style.headboardFabric,{map:wovenTexture}),.012);
    } else if(f.type==='wc') {
      cyl(group,w*.32,w*.24,h*.6,[0,h*.3,.08],m.white);
      const bowl=new THREE.Mesh(new THREE.SphereGeometry(w*.46,20,12),m.white);bowl.scale.set(1,.3,1.35);bowl.position.set(0,h*.64,.07);group.add(bowl);
      box(group,[w*.9,h*.8,d*.25],[0,h*.58,-d*.32],m.white);
    } else {
      const isWardrobe=f.type==='wardrobe';box(group,[w,h-.08,d],[0,(h-.08)/2+.05,0],profile?(finish.front?front:body):(isWardrobe?m.linen:m.oak));
      box(group,[w+.015,.045,d+.015],[0,h,0],style.counterColor?mat(style.counterColor):f.type==='kitchen'?m.counter:wood);
      if(style.upperCabinets){const upper=new THREE.Group();group.add(upper);partitionPieces.push(upper);box(upper,[w,.65,.32],[0,2.15,-d/2+.16],m.white);const strip=mat('#fff2d5',{emissive:'#ffd18a',emissiveIntensity:.5});box(upper,[w-.08,.012,.025],[0,1.82,-.01],strip);}
      const count=Math.max(1,Math.round(w/.55));
      for(let i=1;i<count;i++)box(group,[.006,h-.12,.008],[-w/2+w*i/count,h/2,d/2+.006],profile?mat('#b9b1a1'):m.wood);
      if(f.id==='kitchen-north'){
        box(group,[.60,.025,.40],[0,h+.03,0],m.dark);
        for(const x of [-.17,.17])cyl(group,.09,.09,.018,[x,h+.05,0],m.metal);
      }
      if(f.id==='kitchen-east'){
        box(group,[.40,.014,.50],[0,h+.028,0],m.metal);box(group,[.29,.015,.38],[0,h+.038,0],m.dark);
      }
      if(f.id==='living-media'){
        box(group,[1.50,.84,.04],[0,h+.55,-.06],m.dark);box(group,[1.43,.77,.008],[0,h+.55,-.034],m.screen);
        for(const x of [-.5,.5])box(group,[.04,.13,.16],[x,h+.065,0],m.dark);
      }
    }
  }
  const designerDecor=profile?addDesignerDecor({root,house,profile,materials:m}):null;
  // Local procedural grain is clipped by each floor mesh; no external texture requests.
  const tc=document.createElement('canvas');tc.width=128;tc.height=512;const tp=tc.getContext('2d');
  tp.fillStyle='#ffffff';tp.fillRect(0,0,128,512);
  for(let i=0;i<36;i++){tp.strokeStyle=`rgba(77,67,42,${.025+(i%4)*.009})`;tp.lineWidth=.6;tp.beginPath();tp.moveTo(4+i*3.5,0);tp.lineTo(4+i*3.5+Math.sin(i)*2,512);tp.stroke();}
  tp.strokeStyle='#bbb6a3';tp.lineWidth=1;tp.strokeRect(.5,.5,127,511);
  const woodTexture=new THREE.CanvasTexture(tc);woodTexture.wrapS=woodTexture.wrapT=THREE.RepeatWrapping;woodTexture.repeat.set(3.3,.6);woodTexture.colorSpace=THREE.SRGBColorSpace;
  for(const [id,material] of roomMaterials)if(!profile&&['living','master','bedroom','studio'].includes(id))material.map=woodTexture;

  const cadPositions=[];for(const ln of house.cadLines||[])cadPositions.push(ln.a[0],.045,ln.a[1],ln.b[0],.045,ln.b[1]);
  const cadGeo=new THREE.BufferGeometry();cadGeo.setAttribute('position',new THREE.Float32BufferAttribute(cadPositions,3));
  const cad=new THREE.LineSegments(cadGeo,new THREE.LineBasicMaterial({color:'#465b41',transparent:true,opacity:.65,depthTest:false}));cad.renderOrder=12;cad.visible=false;root.add(cad);

  const glowCanvas=document.createElement('canvas');glowCanvas.width=glowCanvas.height=128;
  const gp=glowCanvas.getContext('2d'),gradient=gp.createRadialGradient(64,64,1,64,64,64);
  gradient.addColorStop(0,'rgba(255,216,128,0.7)');gradient.addColorStop(.4,'rgba(255,202,105,0.32)');gradient.addColorStop(1,'rgba(255,190,90,0)');gp.fillStyle=gradient;gp.fillRect(0,0,128,128);
  const glowTexture=new THREE.CanvasTexture(glowCanvas);glowTexture.colorSpace=THREE.SRGBColorSpace;
  for(const device of devices) {
    const [x,y,z]=device.position;const fixture=new THREE.Group();fixture.position.set(x,y,z);root.add(fixture);
    const lightMaterial=mat('#f2dfb6',{emissive:'#ffca78',emissiveIntensity:.8});
    if(device.id==='studio-desk') {
      cyl(fixture,.09,.12,.045,[0,-.22,0],m.dark);box(fixture,[.025,.27,.025],[0,-.07,0],m.metal);
      cyl(fixture,.10,.15,.15,[0,.09,0],m.dark);cyl(fixture,.12,.12,.02,[0,.01,0],lightMaterial);
    } else {
      cyl(fixture,.19,.19,.065,[0,0,0],m.dark);cyl(fixture,.17,.17,.018,[0,-.038,0],lightMaterial);
      if(device.id==='dining-pendant')cyl(fixture,.012,.012,Math.max(.03,2.65-y),[0,(2.65-y)/2,0],m.dark,8);
    }
    const hit=new THREE.Mesh(new THREE.SphereGeometry(.32,10,8),new THREE.MeshBasicMaterial({visible:false}));hit.userData.deviceId=device.id;fixture.add(hit);pickables.push(hit);
    const light=new THREE.PointLight('#ffd38b',60,6.5,2);light.position.set(x,Math.min(2.2,y),z);root.add(light);
    const glow=new THREE.Mesh(new THREE.PlaneGeometry(device.id==='studio-desk'?1.4:3.0,device.id==='studio-desk'?1.4:3.0),new THREE.MeshBasicMaterial({map:glowTexture,transparent:true,opacity:.6,depthWrite:false,blending:THREE.AdditiveBlending}));glow.rotation.x=-Math.PI/2;glow.position.set(x,.035,z);root.add(glow);
    const el=document.createElement('button');el.type='button';el.className='lamp-label';el.dataset.lamp=device.id;el.dataset.tooltip=device.name;el.innerHTML=BULB_SVG;el.addEventListener('click',()=>onLamp(device.id));lampLayer.append(el);
    lampViews.set(device.id,{fixture,light,lightMaterial,glow,el,position:new THREE.Vector3(x-cx,y+.16,z-cz)});
  }

  const raycaster=new THREE.Raycaster();let pointerStart=null;
  function onPointerDown(e){if(e.button!==0)return;pointerStart={id:e.pointerId,x:e.clientX,y:e.clientY};transition=null;}
  function onPointerUp(e){
    if(!pointerStart||e.pointerId!==pointerStart.id)return;
    const dist=Math.hypot(e.clientX-pointerStart.x,e.clientY-pointerStart.y);pointerStart=null;if(dist>5)return;
    const rect=canvas.getBoundingClientRect();raycaster.setFromCamera(new THREE.Vector2((e.clientX-rect.left)/rect.width*2-1,-(e.clientY-rect.top)/rect.height*2+1),camera);
    const hit=raycaster.intersectObjects(pickables,false)[0];if(hit)onLamp(hit.object.userData.deviceId);
  }
  function onPointerCancel(){pointerStart=null;}
  function onKey(e){
    if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','=','-','0'].includes(e.key))return;e.preventDefault();transition=null;
    if(e.key==='0'){setView('overview');return;}
    const offset=camera.position.clone().sub(controls.target);const s=new THREE.Spherical().setFromVector3(offset);
    if(e.key==='ArrowLeft')s.theta-=.10;if(e.key==='ArrowRight')s.theta+=.10;if(e.key==='ArrowUp')s.phi=Math.max(.08,s.phi-.08);if(e.key==='ArrowDown')s.phi=Math.min(Math.PI*.49,s.phi+.08);
    if(e.key==='+'||e.key==='=')s.radius=Math.max(controls.minDistance,s.radius*.9);if(e.key==='-')s.radius=Math.min(controls.maxDistance,s.radius*1.1);
    camera.position.copy(controls.target).add(new THREE.Vector3().setFromSpherical(s));controls.update();
  }
  canvas.addEventListener('pointerdown',onPointerDown);canvas.addEventListener('pointerup',onPointerUp);canvas.addEventListener('pointercancel',onPointerCancel);canvas.addEventListener('keydown',onKey);
  controls.addEventListener('start',()=>transition=null);

  function fitPosition(direction,target,bounds) {
    const unit=direction.clone().normalize(),testCamera=camera.clone(),corners=[];
    for(const x of [bounds[0],bounds[3]])for(const y of [bounds[1],bounds[4]])for(const z of [bounds[2],bounds[5]])corners.push(new THREE.Vector3(x,y,z));
    let near=2,far=70;
    for(let i=0;i<22;i++){
      const distance=(near+far)/2;testCamera.position.copy(target).addScaledVector(unit,distance);testCamera.lookAt(target);testCamera.updateMatrixWorld();
      const inside=corners.every(v=>{const p=v.clone().project(testCamera);return Math.abs(p.x)<.86&&Math.abs(p.y)<.86&&p.z<1&&p.z>-1});
      if(inside)far=distance;else near=distance;
    }
    return target.clone().addScaledVector(unit,far);
  }
  function preset(view) {
    const bounds=[-cx,-.18,-cz,Math.max(...xs)-cx,2.8,Math.max(...zs)-cz];
    if(view==='top'){const target=new THREE.Vector3(0,0,0);return {target,position:fitPosition(new THREE.Vector3(0,1,.0001),target,bounds)}}
    if(view==='living'){const target=new THREE.Vector3(5.2-cx,.3,5.45-cz);return {target,position:fitPosition(new THREE.Vector3(7,11,10),target,[.3-cx,0,3.5-cz,10-cx,2.7,7.1-cz])};}
    if(view==='studio'){const r=house.rooms.find(r=>r.id==='studio'),target=new THREE.Vector3(r.center[0]-cx,.55,r.center[1]-cz);return {target,position:fitPosition(new THREE.Vector3(3.2,10,-8),target,[1.6-cx,0,7-cz,5.15-cx,2.7,10-cz])};}
    if(view==='bedroom'){const target=new THREE.Vector3(9.7-cx,.3,1.8-cz);return {target,position:fitPosition(new THREE.Vector3(3,6.5,7),target,[7.8-cx,0,.25-cz,11.8-cx,2.7,3.5-cz])};}
    const target=new THREE.Vector3(0,.45,0);return {target,position:fitPosition(new THREE.Vector3(13.8,18.5,20.2),target,bounds)};
  }
  function setView(view,animate=true){
    currentView=view;const p=preset(view);
    if(animate&&!reduced)transition={start:performance.now(),duration:650,from:camera.position.clone(),to:p.position,fromTarget:controls.target.clone(),toTarget:p.target};
    else{camera.position.copy(p.position);controls.target.copy(p.target);camera.lookAt(controls.target);controls.update();transition=null;}
  }
  function setCutaway(value) {
    cutaway=Boolean(value);
    for(const item of wallMeshes){const height=cutaway?Math.min(item.height,.68):item.height;item.mesh.scale.y=height/item.height;item.mesh.position.y=item.base+height/2;}
    for(const piece of upperPieces)if(piece)piece.visible=!cutaway;
    for(const g of windowPieces)g.visible=!cutaway;
    for(const g of partitionPieces)g.visible=!cutaway;
    for(const f of tallFurniture)f.group.scale.y=cutaway?Math.min(1,1.1/f.height):1;
    designerDecor?.setCutaway(cutaway);
  }
  function applyState(state){
    lastState=state;
    designerDecor?.applyState(state);
    for(const device of devices){
      const value=state.devices[device.id],v=lampViews.get(device.id),intensity=value.on?value.brightness/100:0;
      v.light.intensity=intensity*(night?45:22);v.lightMaterial.emissiveIntensity=intensity*(night?3:1.5);v.glow.material.opacity=intensity*(night?.85:.45);
      v.el.classList.toggle('off',!value.on);v.el.classList.toggle('selected',state.selectedId===device.id);v.el.setAttribute('aria-label',`${device.name}，${value.on?'已开启':'已关闭'}，点击${value.on?'关闭':'开启'}`);v.el.setAttribute('aria-pressed',String(value.on));
    }
    for(const room of house.rooms){const related=devices.filter(d=>d.roomId===room.id),average=related.length?related.reduce((sum,d)=>sum+(state.devices[d.id].on?state.devices[d.id].brightness:0),0)/related.length/100:0;const material=roomMaterials.get(room.id);material.emissive=new THREE.Color('#c78c38');material.emissiveIntensity=average*(night?.17:.035);}
  }
  function setNight(value){
    night=Boolean(value);scene.background.set(night?'#262f2e':'#eae7df');ground.material.color.set(night?'#262f2e':'#eae7df');ambient.intensity=night?.45:1.7;sun.intensity=night?.18:2.6;fill.intensity=night?.12:.7;renderer.toneMappingExposure=night?1.15:.92;
    if(lastState)applyState(lastState);
  }
  function resize(){const {width,height}=container.getBoundingClientRect();if(width<1||height<1)return;camera.aspect=width/height;camera.updateProjectionMatrix();renderer.setSize(width,height,false);setView(currentView,false);}
  const observer=new ResizeObserver(resize);observer.observe(container);resize();setCutaway(true);
  function project(el,position,visible=true){
    const p=position.clone().project(camera);const w=container.clientWidth,h=container.clientHeight;
    el.hidden=!visible||p.z>1||p.z< -1||Math.abs(p.x)>1.03||Math.abs(p.y)>1.03;
    el.style.left=`${(p.x*.5+.5)*w}px`;el.style.top=`${(-p.y*.5+.5)*h}px`;
  }
  function render(now){
    if(disposed)return;
    if(transition){const t=Math.min(1,(now-transition.start)/transition.duration),ease=1-Math.pow(1-t,3);camera.position.lerpVectors(transition.from,transition.to,ease);controls.target.lerpVectors(transition.fromTarget,transition.toTarget,ease);if(t===1)transition=null;}
    controls.update();renderer.render(scene,camera);
    for(const label of labels)project(label.el,label.position,showLabels);
    for(const v of lampViews.values())project(v.el,v.position);
    frame=requestAnimationFrame(render);
  }
  frame=requestAnimationFrame(render);
  return {applyState,setView,setCutaway,setNight,setCad:value=>{cad.visible=Boolean(value)},setLabels:value=>{showLabels=Boolean(value)},dispose(){disposed=true;cancelAnimationFrame(frame);observer.disconnect();controls.dispose();canvas.removeEventListener('pointerdown',onPointerDown);canvas.removeEventListener('pointerup',onPointerUp);canvas.removeEventListener('pointercancel',onPointerCancel);canvas.removeEventListener('keydown',onKey);const materials=new Set(),textures=new Set();scene.traverse(o=>{o.geometry?.dispose();for(const material of Array.isArray(o.material)?o.material:o.material?[o.material]:[]){materials.add(material);if(material.map)textures.add(material.map)}});textures.forEach(t=>t.dispose());materials.forEach(m=>m.dispose());woodTexture.dispose();wovenTexture?.dispose();renderer.dispose();roomLayer.replaceChildren();lampLayer.replaceChildren();}};
}
