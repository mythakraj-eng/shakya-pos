import os
import shutil

FILE = "index.html"
BACKUP = "index_backup.html"

if not os.path.exists(FILE):
    print("❌ index.html nahi mila! Kripya script ko index.html wale folder mein save karein.")
    exit()

# 1. Automatic Safety Backup
shutil.copy(FILE, BACKUP)
print(f"✅ Backup ban gaya: {BACKUP}")

with open(FILE, "r", encoding="utf-8") as f:
    code = f.read()

# 2. Remove accidental ```html or ``` fences at top/bottom
code = code.lstrip()
if code.startswith("```html"):
    code = code[7:].lstrip()
elif code.startswith("```"):
    code = code[3:].lstrip()
if code.rstrip().endswith("```"):
    code = code.rstrip()[:-3].rstrip()

def replace_block(src, old_block, new_block, label):
    if old_block in src:
        print(f"✅ Updated: {label}")
        return src.replace(old_block, new_block, 1)
    else:
        print(f"⚠️ Skipped (Already updated or not found): {label}")
        return src

# 3. Upgrade Colour Chip CSS + Add Anchor
old_css = """    .chip-wrap { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
    .color-chip { background: var(--chip-bg); color: var(--maroon-dark); border: 1px solid var(--chip-border); padding: 4.5px 10px; border-radius: 16px; font-size: 11px; font-weight: 700; cursor: pointer; user-select: none; transition: all 0.12s; }
    .color-chip:active { background: var(--maroon); color: #fff; transform: scale(0.95); }"""

new_css = """    /* [ANCHOR:COLOR_CSS_START] */
    .palette-header { display: flex; justify-content: space-between; align-items: center; margin-top: 8px; margin-bottom: 5px; font-size: 11px; color: #475569; font-weight: 700; }
    .palette-actions { display: flex; gap: 6px; }
    .preset-link { background: var(--maroon-light); color: var(--maroon); border: 1px solid var(--chip-border); padding: 2px 7px; border-radius: 6px; font-size: 10px; font-weight: 800; cursor: pointer; }
    .clear-link { color: var(--red); font-size: 10.5px; font-weight: 800; cursor: pointer; padding: 2px 4px; }
    .chip-wrap { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; background: #f8fafc; padding: 7px; border-radius: 10px; border: 1px solid #e2e8f0; }
    .color-chip { display: flex; align-items: center; gap: 6px; background: #ffffff; color: #1e293b; border: 1.5px solid #cbd5e1; padding: 6px 8px; border-radius: 8px; font-size: 11px; font-weight: 700; cursor: pointer; user-select: none; transition: all 0.14s ease; }
    .color-chip .swatch-dot { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; border: 1px solid rgba(0,0,0,0.2); }
    .color-chip.selected { background: var(--maroon); color: #ffffff; border-color: var(--maroon-dark); box-shadow: 0 2px 6px rgba(0,0,0,0.15); }
    .color-chip.selected .swatch-dot { border-color: #ffffff; box-shadow: 0 0 0 1.5px var(--gold); }
    /* [ANCHOR:COLOR_CSS_END] */"""

code = replace_block(code, old_css, new_css, "Colour Palette CSS")

# 4. Upgrade Colour Palette HTML + Add Anchor
old_html = """      <div style="flex:2">
        <label>Colours (Ek ya Poore Set ke Colours)</label>
        <input type="text" id="sColor" placeholder="Ex: Red, Yellow, Green">
      </div>
      <div style="flex:1">
        <label>Qty (Each)</label>
        <input type="number" id="sQty" value="1">
      </div>
    </div>

    <div style="margin-top:6px;">
      <small style="color:#475569; font-size:11px;">👇 Tap karke Colours jodein (Clear: <b style="color:var(--red);cursor:pointer;" onclick="document.getElementById('sColor').value=''">✕ Saaf karein</b>):</small>
      <div class="chip-wrap">
        <span class="color-chip" onclick="addColorChip('Red')">🔴 Red</span>
        <span class="color-chip" onclick="addColorChip('Rani Pink')">🩷 Rani Pink</span>
        <span class="color-chip" onclick="addColorChip('Yellow')">🟡 Yellow</span>
        <span class="color-chip" onclick="addColorChip('Green')">🟢 Green</span>
        <span class="color-chip" onclick="addColorChip('Maroon')">🍷 Maroon</span>
        <span class="color-chip" onclick="addColorChip('Royal Blue')">🔵 Royal Blue</span>
        <span class="color-chip" onclick="addColorChip('Rama')">🩵 Rama</span>
        <span class="color-chip" onclick="addColorChip('Orange')">🟠 Orange</span>
        <span class="color-chip" onclick="addColorChip('Purple')">🟣 Purple</span>
        <span class="color-chip" onclick="addColorChip('Black')">⚫ Black</span>
        <span class="color-chip" onclick="addColorChip('White')">⚪ White</span>
        <span class="color-chip" onclick="addColorChip('Golden')">✨ Golden</span>
        <span class="color-chip" onclick="addColorChip('Multi')">🌈 Multi</span>
      </div>
    </div>"""

new_html = """      <!-- [ANCHOR:COLOR_HTML_START] -->
      <div style="flex:2">
        <label>Colours (Ek ya Poore Set ke Colours)</label>
        <input type="text" id="sColor" placeholder="Ex: Red, Yellow, Green" oninput="syncColorChipsUI()">
      </div>
      <div style="flex:1">
        <label>Qty (Each)</label>
        <input type="number" id="sQty" value="1">
      </div>
    </div>

    <div>
      <div class="palette-header">
        <span>🎨 Colours Chunein (Tap = Add/Remove):</span>
        <div class="palette-actions">
          <span class="preset-link" onclick="applyPresetSet()">+ 6-Set</span>
          <span class="clear-link" onclick="clearColorChips()">✕ Clear</span>
        </div>
      </div>
      <div class="chip-wrap" id="colorPaletteGrid">
        <span class="color-chip" data-col="Red" onclick="toggleColorChip('Red')"><i class="swatch-dot" style="background:#dc2626;"></i>Red</span>
        <span class="color-chip" data-col="Rani Pink" onclick="toggleColorChip('Rani Pink')"><i class="swatch-dot" style="background:#ec4899;"></i>Rani Pink</span>
        <span class="color-chip" data-col="Yellow" onclick="toggleColorChip('Yellow')"><i class="swatch-dot" style="background:#eab308;"></i>Yellow</span>
        <span class="color-chip" data-col="Green" onclick="toggleColorChip('Green')"><i class="swatch-dot" style="background:#16a34a;"></i>Green</span>
        <span class="color-chip" data-col="Maroon" onclick="toggleColorChip('Maroon')"><i class="swatch-dot" style="background:#7f1d1d;"></i>Maroon</span>
        <span class="color-chip" data-col="Royal Blue" onclick="toggleColorChip('Royal Blue')"><i class="swatch-dot" style="background:#1d4ed8;"></i>Royal Blue</span>
        <span class="color-chip" data-col="Rama" onclick="toggleColorChip('Rama')"><i class="swatch-dot" style="background:#06b6d4;"></i>Rama</span>
        <span class="color-chip" data-col="Orange" onclick="toggleColorChip('Orange')"><i class="swatch-dot" style="background:#f97316;"></i>Orange</span>
        <span class="color-chip" data-col="Purple" onclick="toggleColorChip('Purple')"><i class="swatch-dot" style="background:#7e22ce;"></i>Purple</span>
        <span class="color-chip" data-col="Black" onclick="toggleColorChip('Black')"><i class="swatch-dot" style="background:#0f172a;"></i>Black</span>
        <span class="color-chip" data-col="White" onclick="toggleColorChip('White')"><i class="swatch-dot" style="background:#ffffff;"></i>White</span>
        <span class="color-chip" data-col="Golden" onclick="toggleColorChip('Golden')"><i class="swatch-dot" style="background:linear-gradient(135deg,#fde047,#ca8a04);"></i>Golden</span>
        <span class="color-chip" data-col="Multi" onclick="toggleColorChip('Multi')"><i class="swatch-dot" style="background:conic-gradient(#ef4444,#eab308,#22c55e,#3b82f6,#a855f7,#ef4444);"></i>Multi</span>
      </div>
    </div>
    <!-- [ANCHOR:COLOR_HTML_END] -->"""

code = replace_block(code, old_html, new_html, "Colour Palette HTML")

# 5. Upgrade JS Functions + Add Anchor
old_js = """  function addColorChip(colName) {
    const inp = document.getElementById('sColor');
    let current = inp.value.split(',').map(s => s.trim()).filter(Boolean);
    if (!current.includes(colName)) { current.push(colName); }
    inp.value = current.join(', ');
  }"""

new_js = """  // [ANCHOR:COLOR_JS_START]
  function toggleColorChip(colName) {
    const inp = document.getElementById('sColor');
    let current = inp.value.split(',').map(s => s.trim()).filter(Boolean);
    const idx = current.findIndex(c => c.toLowerCase() === colName.toLowerCase());
    if (idx > -1) { current.splice(idx, 1); } else { current.push(colName); }
    inp.value = current.join(', ');
    syncColorChipsUI();
    playPosBeep(900, 0.04);
  }
  function applyPresetSet() {
    document.getElementById('sColor').value = 'Red, Rani Pink, Yellow, Green, Maroon, Royal Blue';
    syncColorChipsUI();
    playPosBeep(960, 0.06);
  }
  function clearColorChips() {
    document.getElementById('sColor').value = '';
    syncColorChipsUI();
  }
  function syncColorChipsUI() {
    const val = document.getElementById('sColor')?.value || '';
    const activeList = val.split(',').map(s => s.trim().toLowerCase()).filter(Boolean);
    document.querySelectorAll('#colorPaletteGrid .color-chip').forEach(chip => {
      const col = (chip.getAttribute('data-col') || '').toLowerCase();
      chip.classList.toggle('selected', activeList.includes(col));
    });
  }
  // [ANCHOR:COLOR_JS_END]"""

code = replace_block(code, old_js, new_js, "Colour Palette JS")

# 6. Reset highlight on Stock Save
old_save_reset = """    document.getElementById('sCode').value = '';
    document.getElementById('sColor').value = '';"""
new_save_reset = """    document.getElementById('sCode').value = '';
    document.getElementById('sColor').value = '';
    if (typeof syncColorChipsUI === 'function') syncColorChipsUI();"""

code = replace_block(code, old_save_reset, new_save_reset, "Stock Save Reset Hook")

with open(FILE, "w", encoding="utf-8") as f:
    f.write(code)

print("\n🎉 Done! index.html update ho gaya aur ab har section mein [ANCHOR] tags lag gaye hain.")
