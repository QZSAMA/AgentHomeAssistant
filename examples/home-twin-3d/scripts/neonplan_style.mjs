// Maps only documented, renderer-effective v4.0.0 material fields. No wall or
// source-furniture coordinates are changed; unsupported appearance is reported.
import assert from 'node:assert/strict';
import { finishRolesOf } from '../vendor/neonplan/frontend/src/finishes.ts';

const FLOORS = new Set(['wood', 'oak', 'tiles', 'carpet', 'stone', 'concrete']);
const hex = value => {
  if (value === undefined || value === null) return undefined;
  assert.match(value, /^#[0-9a-f]{6}$/i, 'Design colours must be #rrggbb');
  return value;
};
const nativeId = value => String(value).replace(/[^a-zA-Z0-9_.-]/g, '_').slice(0, 50);
const r6 = value => Math.round(value * 1e6) / 1e6;

export function applyReferenceStyle(building, house, profile, origin) {
  const floor = building.floors[0];
  const report = {applied: !!profile, rooms: [], walls: [], furniture: [], decorAdded: [], decorSkipped: [], approximations: []};
  if (!profile) return report;
  const warn = message => { if (!report.approximations.includes(message)) report.approximations.push(message); };
  const palette = profile.palette ?? {};
  const defaultWall = hex(palette.wall);
  const originalGeometry = JSON.stringify({walls: floor.walls.map(({a,b,height,thickness})=>({a,b,height,thickness})), openings: floor.openings});
  const originalFurniture = new Map(floor.furniture.map(f => [f.id, [f.x,f.z,f.w,f.d,f.h,f.rotation]]));
  for (const [i, room] of floor.rooms.entries()) {
    const source = house.rooms[i];
    const settings = profile.roomStyles?.[source.id] ?? {};
    if (settings.neonplanFloorMaterial) {
      assert.ok(FLOORS.has(settings.neonplanFloorMaterial), `Unrecognized NeonPlan floor: ${settings.neonplanFloorMaterial}`);
      room.floor_material = settings.neonplanFloorMaterial;
    }
    const wallColor = hex(settings.wallColor) ?? defaultWall;
    if (wallColor) room.wall_color = wallColor;
    report.rooms.push({sourceId: source.id, nativeId: room.id, floor: room.floor_material, wallColor: room.wall_color ?? null});
    if (settings.floor === 'herringbone') warn(`${source.id}: herringbone -> native ${room.floor_material}; 原生使用固定木地板纹理，不能显示人字拼。`);
  }
  if (defaultWall) building.settings.facade_color = defaultWall;
  building.settings.style_day = 'cozy';
  building.settings.style_evening = 'evening';
  building.settings.style_night = 'evening';
  for (const [i, wall] of floor.walls.entries()) {
    const source = house.walls[i]; // The remaining walls are aperture hosts.
    const settings = source ? profile.wallStyles?.[source.id] ?? {} : {};
    const owner = source && [...house.rooms].sort((a,b)=>b.id.length-a.id.length).find(room => source.id.startsWith(`${room.id}-`));
    const color = hex(settings.color) ?? hex(owner && profile.roomStyles?.[owner.id]?.wallColor) ?? defaultWall;
    if (color) wall.color = color;
    report.walls.push({sourceId: source?.id ?? wall.id, nativeId: wall.id, color: wall.color ?? null});
    if (settings.kind === 'wood-framed-glass') warn(`${source.id}: wood-framed-glass -> 保留原CAD墙及高度；原生未近似添加整玻璃或新开口，半墙木框玻璃仅在独立预览表达。`);
  }
  function finish(item, requested, sourceId) {
    const supported = finishRolesOf(item.type, null);
    const effective = {};
    for (const [role, color] of Object.entries(requested ?? {})) {
      const value = hex(color);
      if (!value) continue;
      if (supported.includes(role)) effective[role] = value;
      else warn(`${sourceId}: ${item.type}.finish.${role} 无有效内置颜色角色，未伪写为已生效。`);
    }
    if (Object.keys(effective).length) item.finish = effective;
    return effective;
  }
  for (const source of house.furniture) {
    const item = floor.furniture.find(f => f.id === `furn_${nativeId(source.id)}`);
    assert.ok(item, `Missing source furniture ${source.id}`);
    const settings = profile.furnitureStyles?.[source.id];
    if (!settings) continue;
    if (settings.shape === 'round-glass') {
      item.type = 'table_round';
      warn(`${source.id}: round-glass -> 原生table_round不透明圆桌；保留中心及包围尺寸，无法携带透明玻璃材质。`);
    }
    const requested = {...settings.finish};
    // In the native bed, "fabric" colours the duvet, not the headboard. In
    // kitchen/island models "wood" colours the slab, not the base cabinets.
    if (item.type === 'bed' && settings.linenColor) requested.fabric = hex(settings.linenColor);
    if (['kitchen', 'island', 'worktop'].includes(item.type) && settings.counterColor) {
      requested.wood = hex(settings.counterColor);
      warn(`${source.id}: counterColor 映射到原生wood台面角色；下柜暖木色无独立有效角色，保留原生默认柜体。`);
    }
    if (settings.headboardFabric) warn(`${source.id}: headboardFabric 无独立软包角色；床头保留木色，fabric按linenColor表达床品。`);
    if (settings.upperCabinets) warn(`${source.id}: upperCabinets 尚无明确尺寸/高度，原生未新增猜测吊柜。`);
    if (source.id.startsWith('bedroom-')) warn(`${source.id}: 次卧全景未完整加载；床品暂示意，非完整设计师复原。`);
    const effective = finish(item, requested, source.id);
    if (settings.pillowColor) warn(`${source.id}: pillowColor 独立靠垫色不能映射；原生靠垫随fabric色变亮。`);
    report.furniture.push({sourceId: source.id, nativeId: item.id, type: item.type, finish: effective});
  }
  const decorTypes = {'rug':'rug', 'floor-lamp':'lamp_floor', 'accent-chair':'armchair'};
  const ids = new Set(floor.furniture.map(f => f.id));
  for (const source of profile.decor ?? []) {
    const type = decorTypes[source.type];
    if (!type) {
      report.decorSkipped.push({id: source.id, type: source.type});
      warn(`${source.id}: ${source.type} 无准确原生模型，本次不添加猜测位置或替代结构。`);
      continue;
    }
    const id = `decor_${nativeId(source.id)}`;
    assert.ok(!ids.has(id), `Duplicate decoration id ${id}`);
    ids.add(id);
    const values = [source.x, source.z, source.width, source.depth, source.height, source.rotation ?? 0];
    assert.ok(values.every(Number.isFinite), `Decoration ${source.id} lacks explicit dimensions`);
    const item = {id, name: source.id, type, x:r6(source.x-origin[0]), z:r6(source.z-origin[1]), w:source.width, d:source.depth, h:source.height, rotation:r6(((source.rotation ?? 0)*180/Math.PI%360+360)%360), variant:null, entity:null, power:null};
    const requested = source.finish ?? (type === 'rug' ? {fabric:palette.white} : type === 'armchair' ? {fabric:source.color, wood:palette.oak} : {});
    finish(item, requested, source.id);
    floor.furniture.push(item);
    report.decorAdded.push({id:source.id,nativeId:id,type,entity:null});
    if (type === 'rug') warn(`${source.id}: 彩块地毯近似为单色fabric地毯，原生未携带彩块图案。`);
    if (type === 'lamp_floor' && source.color) warn(`${source.id}: 原生落地灯保留类型/位置，不支持红色壳体；未把壳体色误作灯光颜色。`);
  }
  assert.equal(JSON.stringify({walls: floor.walls.map(({a,b,height,thickness})=>({a,b,height,thickness})), openings: floor.openings}), originalGeometry, 'Reference styling changed structural geometry');
  for (const [id, coords] of originalFurniture) {
    const f = floor.furniture.find(item=>item.id===id);
    assert.deepEqual([f.x,f.z,f.w,f.d,f.h,f.rotation], coords, `Reference styling moved or rotated ${id}`);
  }
  return report;
}
