// Local demonstration only. This module has no network or Home Assistant client.
const STORAGE_KEY = 'wuhan-twin-demo-v1';
const VERSION = 1;
const SCENES = Object.freeze({
  home: Object.freeze({'living-main':100,'dining-pendant':75,'studio-main':65,'studio-desk':45}),
  movie: Object.freeze({'living-main':15,'dining-pendant':0,'studio-main':0,'studio-desk':10}),
  away: Object.freeze({'living-main':0,'dining-pendant':0,'studio-main':0,'studio-desk':0}),
});
const PROVENANCE = '模拟点位，待电气图确认';
const record = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const validLevel = value => typeof value === 'number' && Number.isInteger(value) && value >= 0 && value <= 100;
const safeId = value => typeof value === 'string' && /^[a-zA-Z0-9_-]+$/.test(value)
  && !['__proto__','constructor','prototype'].includes(value);

function deviceList(input) {
  const source = Array.isArray(input) ? input : (Array.isArray(input?.devices) ? input.devices : []);
  const seen = new Set();
  return source.filter(device => {
    if (!record(device) || !safeId(device.id) || seen.has(device.id)) return false;
    seen.add(device.id);
    return true;
  });
}

export function createStore(devices, options = {}) {
  const ids = deviceList(devices).map(device => device.id);
  const known = new Set(ids);
  const storage = options?.storage ?? null;
  const listeners = new Set();
  let selectedId = null, scene = 'home', disposed = false;
  let levels = Object.create(null), lastBrightness = Object.create(null);

  function defaults() {
    selectedId = null;
    scene = 'home';
    levels = Object.fromEntries(ids.map(id => [id, SCENES.home[id] ?? 100]));
    lastBrightness = {...levels};
  }
  function getState() {
    return {
      mode:'simulation', selectedId,
      devices:Object.fromEntries(ids.map(id => [id,{on:levels[id] > 0,brightness:levels[id]}])),
      scene,
    };
  }
  function matchesScene(name) {
    return Object.hasOwn(SCENES,name) && ids.every(id => levels[id] === (SCENES[name][id] ?? (name === 'home' ? 100 : 0)));
  }
  function restore() {
    try {
      const raw = storage?.getItem(STORAGE_KEY);
      if (typeof raw !== 'string' || raw.length > 100_000) return;
      const saved = JSON.parse(raw);
      if (!record(saved) || saved.version !== VERSION || saved.mode !== 'simulation' || !record(saved.devices)) return;
      for (const id of ids) {
        if (!Object.hasOwn(saved.devices,id)) continue;
        const item = saved.devices[id];
        if (!record(item) || typeof item.on !== 'boolean' || !validLevel(item.brightness) || item.on !== (item.brightness > 0)) continue;
        levels[id] = item.brightness;
        const remembered = record(saved.lastBrightness) && Object.hasOwn(saved.lastBrightness,id) ? saved.lastBrightness[id] : null;
        if (levels[id] > 0) lastBrightness[id] = levels[id];
        else if (validLevel(remembered) && remembered > 0) lastBrightness[id] = remembered;
      }
      selectedId = known.has(saved.selectedId) ? saved.selectedId : null;
      scene = typeof saved.scene === 'string' && matchesScene(saved.scene) ? saved.scene : 'custom';
    } catch {
      // Blocked storage, corrupt JSON, and untrusted values leave the demo usable.
    }
  }
  function persisted() {
    return JSON.stringify({version:VERSION,...getState(),lastBrightness:{...lastBrightness}});
  }
  function change(operation) {
    if (disposed) return;
    const before = persisted();
    const beforePublic = JSON.stringify(getState());
    operation();
    const after = persisted();
    if (before === after) return;
    try { storage?.setItem(STORAGE_KEY,after); } catch { /* Persistence is optional. */ }
    if (beforePublic !== JSON.stringify(getState())) {
      for (const listener of [...listeners]) listener(getState());
    }
  }
  function setLevel(id,value) {
    levels[id] = value;
    if (value > 0) lastBrightness[id] = value;
  }

  defaults();
  restore();
  return {
    getState,
    subscribe(listener) {
      if (disposed || typeof listener !== 'function') return () => {};
      listeners.add(listener);
      return () => listeners.delete(listener);
    },
    select(id) {
      if (id !== null && !known.has(id)) return;
      change(() => { selectedId = id; });
    },
    toggle(id) {
      if (!known.has(id)) return;
      change(() => {
        setLevel(id,levels[id] > 0 ? 0 : (lastBrightness[id] || 100));
        scene = 'custom';
      });
    },
    setBrightness(id,value) {
      if (!known.has(id) || typeof value !== 'number' || !Number.isFinite(value)) return;
      const level = Math.round(Math.max(0,Math.min(100,value)));
      if (level === levels[id]) return;
      change(() => { setLevel(id,level);scene = 'custom'; });
    },
    applyScene(name) {
      if (typeof name !== 'string' || !Object.hasOwn(SCENES,name)) return;
      change(() => {
        for (const id of ids) setLevel(id,SCENES[name][id] ?? (name === 'home' ? 100 : 0));
        scene = name;
      });
    },
    reset() { change(defaults); },
    dispose() { disposed = true;listeners.clear(); },
  };
}

export function exportEntityMapping(devices) {
  return {
    schemaVersion:VERSION,
    mode:'simulation',
    connected:false,
    description:'灯具交互演示的待绑定清单；未接入 Home Assistant，entityId 须在实际设备接入后填写并验证。',
    coordinateSystem:{unit:'m',axes:'x 向图右，y 向上，z 向图下'},
    devices:deviceList(devices).map(device => ({
      id:device.id,
      name:typeof device.name === 'string' ? device.name : device.id,
      roomId:typeof device.roomId === 'string' ? device.roomId : null,
      position:Array.isArray(device.position) && device.position.length === 3 && device.position.every(Number.isFinite) ? [...device.position] : null,
      entityId:null,
      provenance:PROVENANCE,
    })),
  };
}
