// All parsing, construction, native-file reading, and wall geometry below use
// unmodified official NeonPlan v4.0.0 code. The semantic-zone adaptation is ours.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readSimple } from '../vendor/neonplan/frontend/src/import/simple.ts';
import { buildPlan } from '../vendor/neonplan/frontend/src/import/builder.ts';
import { exportFile, parseExport } from '../vendor/neonplan/frontend/src/transfer.ts';
import { generateWalls, openingHost, locateOpening } from '../vendor/neonplan/frontend/src/geometry/walls.ts';
import { applyReferenceStyle } from './neonplan_style.mjs';

const [simplePath, housePath, outDir] = process.argv.slice(2);
const read = p => JSON.parse(fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, ''));
const simple = read(simplePath);
const house = read(housePath);
const imported = buildPlan(readSimple(simple), { join: false, square: false, roomsFromWalls: false, lang: 'en' });
assert.equal(imported.building.floors[0].rooms.length, house.rooms.length, 'Official importer lost a room');
const building = imported.building;
const floor = building.floors[0];
const points = [...house.rooms.flatMap(r => r.polygon), ...house.walls.flatMap(w => [w.a, w.b])];
const origin = [Math.min(...points.map(p => p[0])), Math.min(...points.map(p => p[1]))];
const round = n => Math.round(n * 1e6) / 1e6;
const shift = p => [round(p[0] - origin[0]), round(p[1] - origin[1])];
const safeId = id => String(id).replace(/[^a-zA-Z0-9_.-]/g, '_').slice(0, 50);
floor.id = 'floor_wuhan';
floor.name = '武汉印 · 住宅层';
floor.rooms.forEach((r, i) => {
  r.id = `room_${safeId(house.rooms[i].id)}`;
  r.wall_heights = r.points.map(() => 0); // Official documented value: no wall.
  r.floor_material = /卫|厨/.test(r.name) ? 'tiles' : 'wood';
});
assert.equal(floor.furniture.length, house.furniture.length, 'Official importer lost source furniture');
floor.furniture.forEach((item, i) => { item.id = `furn_${safeId(house.furniture[i].id)}`; });
floor.walls = house.walls.map((w, i) => ({id: `cad_wall_${i}`, a: shift(w.a), b: shift(w.b), thickness: w.thickness ?? .2, height: w.height ?? floor.height}));
floor.openings = [];
const devicePath = path.join(path.dirname(housePath), 'devices.json');
const devices = fs.existsSync(devicePath) ? read(devicePath).devices : [];
for (const device of devices) {
  const [x, z] = shift([device.position[0], device.position[2]]);
  const table = device.id.includes('desk');
  const pendant = device.id.includes('pendant');
  floor.furniture.push({id: `lamp_${safeId(device.id)}`, name: `${device.name}（示意点位，待绑定）`, type: table ? 'lamp_table' : pendant ? 'lamp_pendant' : 'lamp_ceiling', x, z, w: table ? .22 : .4, d: table ? .22 : .4, h: table ? .35 : pendant ? .45 : .08, rotation: 0, variant: null, entity: null, power: null, ...(table ? {mount_y: Math.max(0, device.position[1]-.35)} : {})});
}
const openingMap = [];
for (const [index, o] of (house.openings ?? []).entries()) {
  if (!['door', 'window'].includes(o.kind)) continue;
  const a = shift(o.a), b = shift(o.b);
  const width = Math.hypot(b[0] - a[0], b[1] - a[1]);
  assert.ok(width > .1, `Degenerate opening ${o.id}`);
  // CAD walls already stop at the aperture. Add a host spanning that aperture,
  // then cut it using the native opening; 20 mm overlap joins the neighbouring wall.
  const e = [(b[0]-a[0]) / width * .02, (b[1]-a[1]) / width * .02];
  const wall = {id: `opening_host_${index}`, a: [round(a[0]-e[0]), round(a[1]-e[1])], b: [round(b[0]+e[0]), round(b[1]+e[1])], thickness: .2, height: floor.height};
  floor.walls.push(wall);
  const at = [(a[0]+b[0])/2, (a[1]+b[1])/2];
  const nearest = house.rooms.map((r, i) => ({i, distance: Math.hypot(shift(r.center)[0]-at[0], shift(r.center)[1]-at[1])})).sort((a,b) => a.distance-b.distance)[0];
  const opening = {id: `opening_${safeId(o.id)}`, room_id: floor.rooms[nearest.i].id, edge: 0, wall: wall.id, offset: round(width/2+.02), width: round(width), type: o.kind, sill: o.sill ?? 0, height: o.height ?? 2.1, hinge: 'left', leaves: o.kind === 'window' && width > 1.4 ? 2 : 1, swing: 'in', cover: null, contact: null, contact2: null, tilt: null};
  floor.openings.push(opening);
  openingMap.push({sourceId: o.id, nativeId: opening.id, host: wall.id, width: opening.width, center: at});
}
const stylePath = path.join(path.dirname(housePath), 'design-style.json');
const materialMapping = applyReferenceStyle(building, house, fs.existsSync(stylePath) ? read(stylePath) : null, origin);
const backup = exportFile(building, true);
const verified = parseExport(JSON.stringify(backup));
const checkedFloor = verified.floors[0];
const geometry = generateWalls(checkedFloor.rooms, {exterior: building.settings.wall_exterior, interior: building.settings.wall_interior}, checkedFloor.walls);
const unhosted = checkedFloor.openings.filter(o => {
  const host = openingHost(o, checkedFloor.rooms, checkedFloor.walls);
  return !host || !locateOpening(geometry.walls, o, host);
});
assert.equal(geometry.walls.filter(w => !w.free).length, 0, 'Phantom room boundary wall');
assert.equal(unhosted.length, 0, 'Native opening does not attach to rendered wall');
assert.equal(checkedFloor.openings.length, simple.floors[0].doors.length + simple.floors[0].windows.length);
const report = {
  upstream: {tag: 'v4.0.0', commit: '8a0fecd90c4eb565c8af8e2fcac01346125f069f'},
  sourceHouseSha256: createHash('sha256').update(fs.readFileSync(housePath)).digest('hex'),
  sourceDevicesSha256: fs.existsSync(devicePath) ? createHash('sha256').update(fs.readFileSync(devicePath)).digest('hex') : null,
  sourceDesignStyleSha256: fs.existsSync(stylePath) ? createHash('sha256').update(fs.readFileSync(stylePath)).digest('hex') : null,
  referenceStyleApplied: materialMapping.applied,
  officialImporter: 'readSimple -> buildPlan',
  importerStatsBeforeSemanticAdaptation: imported.stats,
  importerWarningsBeforeSemanticAdaptation: imported.warnings,
  adaptation: 'Room polygons are semantic floor zones: all room boundary walls disabled; surveyed walls and aperture host walls retained explicitly. No HA entity IDs assigned.',
  officialParseExportPassed: true,
  sourceUnits: 'm', originShiftMetres: origin,
  roomCount: checkedFloor.rooms.length,
  sourcePhysicalWallSegments: house.walls.length,
  openingHostWalls: checkedFloor.openings.length,
  generatedRoomBoundaryWalls: geometry.walls.filter(w => !w.free).length,
  renderedFreeWallSegments: geometry.walls.length,
  adjacentRoomPairs: geometry.open.length,
  geometryWarnings: geometry.warnings,
  unhostedOpenings: unhosted.map(o => o.id),
  openings: openingMap,
  furnitureCount: checkedFloor.furniture.length,
  lampPlaceholderCount: devices.length,
  realEntityBindings: checkedFloor.furniture.filter(f => f.entity).length,
};
fs.mkdirSync(outDir, {recursive: true});
fs.writeFileSync(path.join(outDir, 'wuhan-neonplan-backup.json'), JSON.stringify(backup, null, 2));
fs.writeFileSync(path.join(outDir, 'neonplan-validation.json'), JSON.stringify(report, null, 2));
fs.writeFileSync(path.join(outDir, 'neonplan-material-mapping.json'), JSON.stringify(materialMapping, null, 2));
