"""Make a local-only variant of the official preview; upstream stays untouched."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "vendor/neonplan/preview/index.html"
target = source.with_name("wuhan.html")
html = source.read_text(encoding="utf-8")
old = 'let building = params.has("empty") ? { version: 1, floors: [], settings: { wall_exterior: 0.24, wall_interior: 0.12, grid: 0.05 } } : DEMO_BUILDING;'
new = '''// Local adaptation: load the CAD-derived, schema-validated native backup.
      const localResponse = await fetch("../../../exports/wuhan-neonplan-backup.json");
      if (!localResponse.ok) throw new Error("Local Wuhan backup is unavailable");
      let building = (await localResponse.json()).building;
      const demoDevices = (await (await fetch("../../../data/devices.json")).json()).devices;
      const wuhanStates = {};
      const wuhanEntities = {};
      const wuhanAreas = {};
      for (const room of building.floors[0].rooms) {
        room.area_id = "demo_" + room.id;
        wuhanAreas[room.area_id] = {area_id: room.area_id, name: room.name, floor_id: "floor_wuhan"};
      }
      for (const device of demoDevices) {
        const entity = "light.demo_wuhan_" + device.id.replaceAll("-", "_");
        const lamp = building.floors[0].furniture.find(f => f.id === "lamp_" + device.id);
        if (!lamp) throw new Error("Unbound lamp model missing: " + device.id);
        lamp.entity = entity;
        lamp.name = device.name + "（模拟）";
        wuhanEntities[entity] = {entity_id: entity, area_id: "demo_room_" + device.roomId};
        wuhanStates[entity] = {entity_id: entity, state: "off", attributes: {friendly_name: device.name + "（模拟）", supported_color_modes: ["rgb"], color_mode: "rgb", rgb_color: device.id.includes("desk") ? [154,100,255] : [255,202,140]}};
      }
      building.floors[0].ha_floor = "floor_wuhan";
      window.wuhanImportProof = {rooms: building.floors[0].rooms.length, openings: building.floors[0].openings.length, source: "local native backup", actualHomeAssistant: false, simulatedLights: demoDevices.length};'''
if html.count(old) != 1:
    raise RuntimeError("Pinned upstream preview changed; review adapter before replacing")
html = html.replace(old, new)
html = html.replace('const params = new URLSearchParams(location.search);', 'const params = new URLSearchParams(location.search);\n      try { localStorage.setItem("neonplan3d.news.fun_gifts_winter_2026", "never"); } catch {}')
html = html.replace('areas: DEMO_AREAS,', 'areas: wuhanAreas,')
html = html.replace('floors: DEMO_FLOORS,', 'floors: {floor_wuhan: {floor_id: "floor_wuhan", name: "武汉印", level: 0}},')
html = html.replace('entities: DEMO_ENTITIES,', 'entities: wuhanEntities,')
html = html.replace('states: structuredClone(DEMO_STATES),', 'states: structuredClone(wuhanStates),')
html = html.replace('current = { ...current, states };', 'current = { ...current, states };\n          window.wuhanDemoStates = states;\n          document.querySelectorAll("[data-wuhan-light]").forEach(btn => {const on = states[btn.dataset.wuhanLight]?.state === "on";btn.textContent = btn.dataset.label + (on ? " · 开" : " · 关");btn.style.background = on ? "#8edfba" : "#1b3246";btn.style.color = on ? "#102720" : "#e5edf6";});')
html = html.replace('window.fp3dPanel = panel;', '''window.fp3dPanel = panel;
        window.wuhanDemoStates = current.states;
        window.wuhanDemoToggle = async id => hass.callService("light", "toggle", {entity_id: "light.demo_wuhan_" + id.replaceAll("-", "_")});
        const controls = document.getElementById("wuhan-light-controls");
        for (const device of demoDevices) {
          const btn = document.createElement("button");
          btn.dataset.wuhanLight = "light.demo_wuhan_" + device.id.replaceAll("-", "_");
          btn.dataset.label = device.name;
          btn.textContent = device.name + " · 关";
          btn.setAttribute("aria-label", "模拟切换：" + device.name);
          btn.style.cssText = "padding:6px 9px;border:1px solid #577287;border-radius:5px;background:#1b3246;color:#e5edf6;cursor:pointer";
          btn.onclick = () => window.wuhanDemoToggle(device.id);
          controls.append(btn);
        }''')
html = html.replace('<title>NeonPlan 3D – Vorschau</title>', '<title>武汉印 · NeonPlan 4.0 本地导入验证</title>')
html = html.replace('<html lang="de">', '<html lang="zh">')
html = html.replace('<body>', '''<body>
    <div style="position:fixed;bottom:8px;right:10px;z-index:100000;background:#101b28ed;color:#e5edf6;border:1px solid #466078;border-radius:8px;padding:8px 12px;font:12px/1.5 sans-serif;max-width:340px">武汉印 · 官方 NeonPlan 4.0 本地预览<br>模型来自本地 DWG；本页使用模拟 HA，未连接真实设备。<div id="wuhan-light-controls" style="display:grid;grid-template-columns:1fr 1fr;gap:5px;margin:7px 0"></div><a href="../../../exports/wuhan-neonplan-backup.json" download style="color:#97e9d3">下载已校验的完整导入备份</a></div>''')
target.write_text(html, encoding="utf-8")
print(target)
