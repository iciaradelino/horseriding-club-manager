// ── Data ────────────────────────────────────────────────────────────────────

const tables = [
  {
    id: 'accounts_user',
    label: 'accounts_user',
    theme: 'auth',
    description: 'Custom user account extending Django\'s AbstractUser. Holds login credentials and a role field (admin / trainer / member) shared across all user types.',
    x: 1000, y: 200,
    fields: [
      { name: 'id',           type: 'INTEGER',      kind: 'pk' },
      { name: 'username',     type: 'VARCHAR(150)',  kind: 'field' },
      { name: 'password',     type: 'VARCHAR(128)',  kind: 'field' },
      { name: 'email',        type: 'VARCHAR(254)',  kind: 'field' },
      { name: 'first_name',   type: 'VARCHAR(150)',  kind: 'field' },
      { name: 'last_name',    type: 'VARCHAR(150)',  kind: 'field' },
      { name: 'role',         type: 'VARCHAR(20)',   kind: 'field' },
      { name: 'phone',        type: 'VARCHAR(20)',   kind: 'field' },
      { name: 'is_staff',     type: 'BOOL',          kind: 'field' },
      { name: 'is_superuser', type: 'BOOL',          kind: 'field' },
      { name: 'is_active',    type: 'BOOL',          kind: 'field' },
      { name: 'date_joined',  type: 'DATETIME',      kind: 'field' },
    ],
  },
  {
    id: 'members_member',
    label: 'members_member',
    theme: 'people',
    description: 'Profile for club members. One-to-one with accounts_user. Stores skill level, join date, and emergency contact details.',
    x: 550, y: 200,
    fields: [
      { name: 'id',                      type: 'INTEGER',      kind: 'pk' },
      { name: 'user_id',                 type: 'FK → accounts_user', kind: 'fk' },
      { name: 'date_of_birth',           type: 'DATE',         kind: 'field' },
      { name: 'skill_level',             type: 'VARCHAR(20)',  kind: 'field' },
      { name: 'joined_date',             type: 'DATE',         kind: 'field' },
      { name: 'emergency_contact_name',  type: 'VARCHAR(100)', kind: 'field' },
      { name: 'emergency_contact_phone', type: 'VARCHAR(20)',  kind: 'field' },
      { name: 'notes',                   type: 'TEXT',         kind: 'field' },
    ],
  },
  {
    id: 'staff_trainer',
    label: 'staff_trainer',
    theme: 'people',
    description: 'Profile for trainers. One-to-one with accounts_user. Tracks specialisation, bio, and whether the trainer is currently active.',
    x: 1450, y: 260,
    fields: [
      { name: 'id',             type: 'INTEGER',      kind: 'pk' },
      { name: 'user_id',        type: 'FK → accounts_user', kind: 'fk' },
      { name: 'specialisation', type: 'VARCHAR(100)', kind: 'field' },
      { name: 'bio',            type: 'TEXT',         kind: 'field' },
      { name: 'is_active',      type: 'BOOL',         kind: 'field' },
    ],
  },
  {
    id: 'horses_horse',
    label: 'horses_horse',
    theme: 'horses',
    description: 'Registry of horses in the club. Stores breed, colour, date of birth, current status (available / retired / injured), and an optional photo.',
    x: 1450, y: 800,
    fields: [
      { name: 'id',            type: 'INTEGER',     kind: 'pk' },
      { name: 'name',          type: 'VARCHAR(100)', kind: 'field' },
      { name: 'breed',         type: 'VARCHAR(100)', kind: 'field' },
      { name: 'color',         type: 'VARCHAR(50)',  kind: 'field' },
      { name: 'date_of_birth', type: 'DATE',         kind: 'field' },
      { name: 'status',        type: 'VARCHAR(20)',  kind: 'field' },
      { name: 'notes',         type: 'TEXT',         kind: 'field' },
      { name: 'photo',         type: 'VARCHAR(100)', kind: 'field' },
    ],
  },
  {
    id: 'horses_healthrecord',
    label: 'horses_healthrecord',
    theme: 'horses',
    description: 'Veterinary and care records for each horse. Tracks check-ups, vaccinations and treatments with a next_due_date for scheduling.',
    x: 1450, y: 500,
    fields: [
      { name: 'id',           type: 'INTEGER',     kind: 'pk' },
      { name: 'horse_id',     type: 'FK → horses_horse', kind: 'fk' },
      { name: 'record_type',  type: 'VARCHAR(20)', kind: 'field' },
      { name: 'date',         type: 'DATE',        kind: 'field' },
      { name: 'description',  type: 'TEXT',        kind: 'field' },
      { name: 'performed_by', type: 'VARCHAR(100)', kind: 'field' },
      { name: 'next_due_date', type: 'DATE',       kind: 'field' },
    ],
  },
  {
    id: 'lessons_lesson',
    label: 'lessons_lesson',
    theme: 'lessons',
    description: 'A scheduled riding lesson. Links a trainer and a horse to a time slot, with status tracking (scheduled / completed / cancelled).',
    x: 1000, y: 600,
    fields: [
      { name: 'id',         type: 'INTEGER',     kind: 'pk' },
      { name: 'title',      type: 'VARCHAR(100)', kind: 'field' },
      { name: 'trainer_id', type: 'FK → staff_trainer', kind: 'fk' },
      { name: 'horse_id',   type: 'FK → horses_horse',  kind: 'fk' },
      { name: 'start_time', type: 'DATETIME',    kind: 'field' },
      { name: 'end_time',   type: 'DATETIME',    kind: 'field' },
      { name: 'status',     type: 'VARCHAR(20)', kind: 'field' },
      { name: 'notes',      type: 'TEXT',        kind: 'field' },
    ],
  },
  {
    id: 'lessons_lesson_members',
    label: 'lessons_lesson_members',
    theme: 'lessons',
    description: 'Django-generated M2M join table that enrolls members in lessons. Each row represents one member\'s participation in one lesson.',
    x: 550, y: 600,
    fields: [
      { name: 'id',        type: 'INTEGER', kind: 'pk' },
      { name: 'lesson_id', type: 'FK → lessons_lesson',  kind: 'fk' },
      { name: 'member_id', type: 'FK → members_member',  kind: 'fk' },
    ],
  },
  {
    id: 'billing_membershipplan',
    label: 'billing_membershipplan',
    theme: 'billing',
    description: 'Catalogue of available membership tiers. Defines pricing, billing cycle (monthly / annual), and how many lessons are included per cycle.',
    x: 100, y: 750,
    fields: [
      { name: 'id',                type: 'INTEGER',     kind: 'pk' },
      { name: 'name',              type: 'VARCHAR(100)', kind: 'field' },
      { name: 'description',       type: 'TEXT',        kind: 'field' },
      { name: 'price',             type: 'DECIMAL(8,2)', kind: 'field' },
      { name: 'billing_cycle',     type: 'VARCHAR(20)', kind: 'field' },
      { name: 'lessons_per_cycle', type: 'INTEGER',     kind: 'field' },
      { name: 'is_active',         type: 'BOOL',        kind: 'field' },
    ],
  },
  {
    id: 'billing_membership',
    label: 'billing_membership',
    theme: 'billing',
    description: 'An active subscription linking a member to a plan. Records the start/end dates and the current status (active / expired / cancelled).',
    x: 100, y: 200,
    fields: [
      { name: 'id',         type: 'INTEGER', kind: 'pk' },
      { name: 'member_id',  type: 'FK → members_member',        kind: 'fk' },
      { name: 'plan_id',    type: 'FK → billing_membershipplan', kind: 'fk' },
      { name: 'start_date', type: 'DATE',        kind: 'field' },
      { name: 'end_date',   type: 'DATE',        kind: 'field' },
      { name: 'status',     type: 'VARCHAR(20)', kind: 'field' },
    ],
  },
  {
    id: 'billing_invoice',
    label: 'billing_invoice',
    theme: 'billing',
    description: 'Individual invoice issued for a membership. Tracks the amount, issue and due dates, and payment status (pending / paid / overdue).',
    x: 100, y: 500,
    fields: [
      { name: 'id',             type: 'INTEGER',      kind: 'pk' },
      { name: 'membership_id',  type: 'FK → billing_membership', kind: 'fk' },
      { name: 'amount',         type: 'DECIMAL(8,2)', kind: 'field' },
      { name: 'issued_date',    type: 'DATE',         kind: 'field' },
      { name: 'due_date',       type: 'DATE',         kind: 'field' },
      { name: 'paid_date',      type: 'DATE',         kind: 'field' },
      { name: 'status',         type: 'VARCHAR(20)',  kind: 'field' },
    ],
  },
];

const relationships = [
  { from: 'members_member',         fromField: 'user_id',       to: 'accounts_user',          toField: 'id', color: 'rel-auth' },
  { from: 'staff_trainer',          fromField: 'user_id',       to: 'accounts_user',          toField: 'id', color: 'rel-auth' },
  { from: 'horses_healthrecord',    fromField: 'horse_id',      to: 'horses_horse',           toField: 'id', color: 'rel-horses' },
  { from: 'lessons_lesson',         fromField: 'trainer_id',    to: 'staff_trainer',          toField: 'id', color: 'rel-people' },
  { from: 'lessons_lesson',         fromField: 'horse_id',      to: 'horses_horse',           toField: 'id', color: 'rel-horses' },
  { from: 'lessons_lesson_members', fromField: 'lesson_id',     to: 'lessons_lesson',         toField: 'id', color: 'rel-lessons' },
  { from: 'lessons_lesson_members', fromField: 'member_id',     to: 'members_member',         toField: 'id', color: 'rel-people' },
  { from: 'billing_membership',     fromField: 'member_id',     to: 'members_member',         toField: 'id', color: 'rel-people' },
  { from: 'billing_membership',     fromField: 'plan_id',       to: 'billing_membershipplan', toField: 'id', color: 'rel-billing' },
  { from: 'billing_invoice',        fromField: 'membership_id', to: 'billing_membership',     toField: 'id', color: 'rel-billing' },
];

// ── DOM references ───────────────────────────────────────────────────────────

const canvas   = document.getElementById('canvas');
const svgEl    = document.getElementById('lines');
const tableEls = {};
const fieldEls = {};

// ── Tooltip ──────────────────────────────────────────────────────────────────

const tooltip = document.createElement('div');
tooltip.id = 'table-tooltip';
document.body.appendChild(tooltip);

function showTooltip(text, headerEl) {
  tooltip.textContent = text;
  tooltip.classList.add('visible');
  positionTooltip(headerEl);
}

function positionTooltip(headerEl) {
  const rect  = headerEl.getBoundingClientRect();
  const gap   = 8;
  tooltip.style.left = `${rect.left}px`;
  tooltip.style.top  = `${rect.bottom + gap}px`;

  // keep within viewport horizontally
  const tRect = tooltip.getBoundingClientRect();
  if (tRect.right > window.innerWidth - 8) {
    tooltip.style.left = `${window.innerWidth - 8 - tRect.width}px`;
  }
}

function hideTooltip() {
  tooltip.classList.remove('visible');
}

// ── Highlight / Focus ────────────────────────────────────────────────────────

let hoveredTable = null;
let focusedTable = null;

function getRelatedIds(tableId) {
  const ids = new Set([tableId]);
  relationships.forEach(rel => {
    if (rel.from === tableId) ids.add(rel.to);
    if (rel.to   === tableId) ids.add(rel.from);
  });
  return ids;
}

function applyHighlight() {
  const activeId = focusedTable || hoveredTable;
  Object.entries(tableEls).forEach(([id, el]) => {
    el.classList.toggle('dimmed', !!activeId && !getRelatedIds(activeId).has(id));
    el.classList.toggle('focused', id === focusedTable);
  });
  drawLines();
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function getFieldY(tableId, fieldName) {
  const el = fieldEls[`${tableId}.${fieldName}`];
  if (!el) return null;
  const rect = el.getBoundingClientRect();
  return rect.top + rect.height / 2;
}

function getTableRect(tableId) {
  const el = tableEls[tableId];
  return el ? el.getBoundingClientRect() : null;
}

// ── SVG lines ────────────────────────────────────────────────────────────────

const LINE_COLORS = {
  'rel-auth':    '#1f3a2a',
  'rel-people':  '#2f6d47',
  'rel-horses':  '#1e4747',
  'rel-lessons': '#274a36',
  'rel-billing': '#b8893a',
};

function drawLines() {
  svgEl.innerHTML = '';

  relationships.forEach(rel => {
    const fromRect = getTableRect(rel.from);
    const toRect   = getTableRect(rel.to);
    const fy = getFieldY(rel.from, rel.fromField);
    const ty = getFieldY(rel.to,   rel.toField);

    if (!fromRect || !toRect || fy == null || ty == null) return;

    const fromCx = fromRect.left + fromRect.width  / 2;
    const toCx   = toRect.left   + toRect.width    / 2;

    // tables overlap horizontally if their x ranges intersect
    const hOverlap = fromRect.right > toRect.left && fromRect.left < toRect.right;

    let x1, y1, x2, y2, cpx1, cpx2;

    if (hOverlap) {
      // same column — loop out to whichever side has more space
      const spaceLeft  = Math.min(fromRect.left, toRect.left) - 0;
      const spaceRight = window.innerWidth - Math.max(fromRect.right, toRect.right);
      const goRight    = spaceRight >= spaceLeft;
      const outer      = goRight
        ? Math.max(fromRect.right, toRect.right) + 55
        : Math.min(fromRect.left, toRect.left)   - 55;

      x1   = goRight ? fromRect.right : fromRect.left;
      x2   = goRight ? toRect.right   : toRect.left;
      y1   = fy;
      y2   = ty;
      cpx1 = outer;
      cpx2 = outer;
    } else {
      // normal horizontal connection — exit from nearest side
      const goRight = fromCx < toCx;
      x1 = goRight ? fromRect.right : fromRect.left;
      x2 = goRight ? toRect.left    : toRect.right;
      y1 = fy;
      y2 = ty;
      const bend = Math.max(Math.abs(x2 - x1) * 0.42, 55);
      cpx1 = goRight ? x1 + bend : x1 - bend;
      cpx2 = goRight ? x2 - bend : x2 + bend;
    }

    const activeId   = focusedTable || hoveredTable;
    const isActive   = activeId && (rel.from === activeId || rel.to === activeId);
    const lineState  = !activeId ? '' : isActive ? ' line-active' : ' line-dimmed';

    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('class', `rel-line ${rel.color}${lineState}`);
    path.setAttribute('d', `M ${x1} ${y1} C ${cpx1} ${y1}, ${cpx2} ${y2}, ${x2} ${y2}`);
    svgEl.appendChild(path);

    [{ x: x1, y: y1 }, { x: x2, y: y2 }].forEach(({ x, y }) => {
      const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      dot.setAttribute('cx', x);
      dot.setAttribute('cy', y);
      dot.setAttribute('r', isActive ? 4 : 3);
      dot.style.fill    = LINE_COLORS[rel.color];
      dot.style.opacity = !activeId ? '0.75' : isActive ? '1' : '0.08';
      svgEl.appendChild(dot);
    });
  });
}

// ── Build table DOM ──────────────────────────────────────────────────────────

function buildFieldRow(tableId, field) {
  const row = document.createElement('div');
  row.className = `field ${field.kind === 'pk' ? 'pk-row' : field.kind === 'fk' ? 'fk-row' : ''}`;
  row.id = `field-${tableId}-${field.name}`;

  const icon = field.kind === 'pk' ? '<span class="field-icon pk">🔑</span>'
             : field.kind === 'fk' ? '<span class="field-icon fk">◆</span>'
             :                       '<span class="field-icon regular">◇</span>';

  row.innerHTML = `${icon}<span class="field-name">${field.name}</span><span class="field-type">${field.type}</span>`;
  fieldEls[`${tableId}.${field.name}`] = row;
  return row;
}

function buildTable(t) {
  const div = document.createElement('div');
  div.className = `table theme-${t.theme}`;
  div.id = `tbl-${t.id}`;
  div.style.left = `${t.x}px`;
  div.style.top  = `${t.y}px`;

  const header = document.createElement('div');
  header.className = 'table-header';
  header.innerHTML = `<span class="icon">▦</span>${t.label}`;
  if (t.description) {
    header.addEventListener('mouseenter', () => showTooltip(t.description, header));
    header.addEventListener('mousemove',  () => positionTooltip(header));
    header.addEventListener('mouseleave', hideTooltip);
  }

  // click header to focus/unfocus
  header.addEventListener('click', e => {
    e.stopPropagation();
    focusedTable = focusedTable === t.id ? null : t.id;
    hoveredTable = null;
    applyHighlight();
  });

  // hover whole table to highlight relationships
  div.addEventListener('mouseenter', () => {
    if (focusedTable) return;
    hoveredTable = t.id;
    applyHighlight();
  });
  div.addEventListener('mouseleave', () => {
    if (focusedTable) return;
    hoveredTable = null;
    applyHighlight();
  });

  div.appendChild(header);

  const body = document.createElement('div');
  body.className = 'table-body';
  t.fields.forEach(f => body.appendChild(buildFieldRow(t.id, f)));
  div.appendChild(body);

  canvas.appendChild(div);
  tableEls[t.id] = div;
}

tables.forEach(buildTable);

// ── Drag ─────────────────────────────────────────────────────────────────────

let dragging = null, dragOffX = 0, dragOffY = 0;

Object.values(tableEls).forEach(el => {
  el.addEventListener('mousedown', e => {
    dragging = el;
    dragOffX = e.clientX / scale - parseInt(el.style.left);
    dragOffY = e.clientY / scale - parseInt(el.style.top);
    el.style.zIndex = 100;
    e.preventDefault();
  });
});

document.addEventListener('mousemove', e => {
  if (!dragging) return;
  dragging.style.left = `${e.clientX / scale - dragOffX}px`;
  dragging.style.top  = `${e.clientY / scale - dragOffY}px`;
  drawLines();
});

document.addEventListener('mouseup', () => {
  if (dragging) { dragging.style.zIndex = 10; dragging = null; }
});

// ── Pan & zoom ───────────────────────────────────────────────────────────────

let panning = false, panStartX = 0, panStartY = 0;
let offsetX = 0, offsetY = 0, scale = 1;

function applyTransform() {
  canvas.style.transformOrigin = '0 0';
  canvas.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(${scale})`;
  drawLines();
}

canvas.addEventListener('click', e => {
  if (e.target === canvas) {
    focusedTable = null;
    hoveredTable = null;
    applyHighlight();
  }
});

canvas.addEventListener('mousedown', e => {
  if (e.target === canvas || e.target === svgEl) {
    panning   = true;
    panStartX = e.clientX - offsetX;
    panStartY = e.clientY - offsetY;
  }
});

document.addEventListener('mousemove', e => {
  if (!panning) return;
  offsetX = e.clientX - panStartX;
  offsetY = e.clientY - panStartY;
  applyTransform();
});

document.addEventListener('mouseup', () => { panning = false; });

canvas.addEventListener('wheel', e => {
  e.preventDefault();
  const delta = e.deltaY > 0 ? -0.08 : 0.08;
  scale = Math.min(2, Math.max(0.3, scale + delta));
  applyTransform();
}, { passive: false });

// ── Fit to screen ────────────────────────────────────────────────────────────

function fitToScreen() {
  const ids  = Object.keys(tableEls);
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;

  ids.forEach(id => {
    const el = tableEls[id];
    const x  = parseInt(el.style.left);
    const y  = parseInt(el.style.top);
    minX = Math.min(minX, x);
    minY = Math.min(minY, y);
    maxX = Math.max(maxX, x + el.offsetWidth);
    maxY = Math.max(maxY, y + el.offsetHeight);
  });

  const padding = 40;
  const contentW = maxX - minX + padding * 2;
  const contentH = maxY - minY + padding * 2;
  const scaleX = window.innerWidth  / contentW;
  const scaleY = window.innerHeight / contentH;
  scale   = Math.min(scaleX, scaleY, 1);
  offsetX = (padding - minX) * scale;
  offsetY = (padding - minY) * scale;
  applyTransform();
}

// fit button
const fitBtn = document.createElement('button');
fitBtn.textContent = 'Fit to screen';
fitBtn.style.cssText = `
  position: fixed; bottom: 16px; right: 16px;
  background: #ffffff;
  color: #3a3f3a; border: 1px solid #e6dfce;
  border-radius: 6px; padding: 6px 14px;
  font-family: 'Geist Mono', 'JetBrains Mono', monospace; font-size: 11px;
  cursor: pointer; z-index: 200;
  box-shadow: 0 1px 3px rgba(24,28,24,.06);
  letter-spacing: 0.04em;
`;
fitBtn.addEventListener('click', fitToScreen);
document.body.appendChild(fitBtn);

// ── Init ─────────────────────────────────────────────────────────────────────

window.addEventListener('load', () => {
  fitToScreen();
  drawLines();
});
window.addEventListener('resize', () => {
  fitToScreen();
  drawLines();
});
