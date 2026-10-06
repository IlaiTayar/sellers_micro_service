const API = '';
let session = null;
let sellerScope = 'me';
let itemScope = 'me';

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const isAdmin = () => session && session.role === 'admin';
const PLACEHOLDER = 'data:image/svg+xml;utf8,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="180"><rect width="100%" height="100%" fill="#eef1f6"/><text x="50%" y="50%" fill="#9aa6b8" font-family="sans-serif" font-size="15" text-anchor="middle" dominant-baseline="middle">No image</text></svg>');


function toast(msg, kind) {
  const t = $('toast');
  t.textContent = msg;
  t.className = 'toast show ' + (kind || 'info');
  setTimeout(() => { t.className = 'toast ' + (kind || 'info'); }, 3200);
}

async function api(path, method, body) {
  const headers = { 'Content-Type': 'application/json' };
  if (session && session.token) headers['Authorization'] = 'Bearer ' + session.token;
  let res;
  try {
    res = await fetch(API + path, { method: method || 'GET', headers, body: body ? JSON.stringify(body) : undefined });
  } catch (e) {
    throw new Error('Could not reach the server. Please try again.');
  }
  const text = await res.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch (e) { data = text; }
  if (!res.ok) {
    const detail = data && data.detail
      ? (typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail))
      : ('Request failed (HTTP ' + res.status + ')');
    throw new Error(detail);
  }
  return data;
}

function applySession(r) {
  session = { token: r.access_token, seller_id: r.seller_id, seller_name: r.seller_name, role: r.role };
  $('loginCard').classList.add('hidden');
  $('app').classList.remove('hidden');
  $('logoutBtn').classList.remove('hidden');
  $('whoami').textContent = 'Signed in as ' + r.seller_name + ' (id ' + r.seller_id + ')';
  $('adminBadge').style.display = isAdmin() ? 'inline-block' : 'none';
  $('adminSellerField').style.display = isAdmin() ? 'block' : 'none';
  $('sellerActionsHead').style.display = isAdmin() ? 'table-cell' : 'none';
  sellerScope = isAdmin() ? 'all' : 'me';
  itemScope = isAdmin() ? 'all' : 'me';
  syncSeg('sellerScope', sellerScope);
  syncSeg('itemScope', itemScope);
  loadProfile(); loadSellers(); loadItems();
}

function logout() {
  session = null;
  $('app').classList.add('hidden');
  $('logoutBtn').classList.add('hidden');
  $('loginCard').classList.remove('hidden');
  $('adminBadge').style.display = 'none';
  $('whoami').textContent = 'Not signed in';
}

async function doLogin() {
  const seller_id = parseInt($('loginId').value, 10);
  const email = $('loginEmail').value.trim();
  if (!seller_id || !email) { toast('Enter your id and email', 'err'); return; }
  try {
    const r = await api('/auth/login', 'POST', { seller_id, email });
    applySession(r);
    toast('Welcome, ' + r.seller_name, 'ok');
  } catch (e) { toast(e.message, 'err'); }
}

async function doRegister() {
  const seller_name = $('regName').value.trim();
  const email = $('regEmail').value.trim();
  const status = $('regStatus').value;
  if (!seller_name || !email) { toast('Fill in name and email', 'err'); return; }
  try {
    const r = await api('/auth/register', 'POST', { seller_name, email, status });
    applySession(r);
    toast('Account created. Your seller id is ' + r.seller_id, 'ok');
  } catch (e) { toast(e.message, 'err'); }
}

async function loadProfile() {
  try {
    const s = await api('/seller/' + session.seller_id);
    $('pName').value = s.seller_name; $('pEmail').value = s.email; $('pStatus').value = s.status;
  } catch (e) { toast(e.message, 'err'); }
}

async function saveProfile() {
  const body = { seller_id: session.seller_id, seller_name: $('pName').value, email: $('pEmail').value, status: $('pStatus').value };
  try { await api('/seller/' + session.seller_id, 'PUT', body); toast('Profile saved', 'ok'); session.seller_name = body.seller_name; $('whoami').textContent = 'Signed in as ' + body.seller_name + ' (id ' + session.seller_id + ')'; loadSellers(); }
  catch (e) { toast(e.message, 'err'); }
}

async function deleteProfile() {
  if (!confirm('Delete your seller account? This cannot be undone.')) return;
  try { await api('/seller/' + session.seller_id, 'DELETE'); toast('Account deleted', 'ok'); logout(); }
  catch (e) { toast(e.message, 'err'); }
}

async function loadSellers() {
  try {
    let list = await api('/seller');
    if (sellerScope === 'me') list = list.filter(s => s.seller_id === session.seller_id);
    $('sellersBody').innerHTML = list.map(s => {
      const mine = s.seller_id === session.seller_id;
      const reveal = mine || isAdmin();
      const st = (s.status || '').toLowerCase();
      const idCell = reveal ? (s.seller_id + (mine ? ' <span class="badge me">me</span>' : '')) : '<span class="muted">hidden</span>';
      const emailCell = reveal ? esc(s.email) : '<span class="muted">hidden</span>';
      const actions = isAdmin() ? '<td><button class="btn secondary sm" onclick="editSeller(' + s.seller_id + ')">Edit</button> <button class="btn danger sm" onclick="deleteSeller(' + s.seller_id + ')">Delete</button></td>' : '';
      return '<tr><td>' + idCell + '</td><td>' + esc(s.seller_name) + '</td><td>' + emailCell + '</td><td><span class="badge ' + st + '">' + esc(s.status) + '</span></td>' + actions + '</tr>';
    }).join('') || '<tr><td colspan=4 class="empty">No sellers</td></tr>';
  } catch (e) { toast(e.message, 'err'); }
}

async function loadItems() {
  try {
    let list = await api('/item');
    let nameById = {};
    try {
      const sls = await api('/seller');
      sls.forEach(s => { nameById[s.seller_id] = (s.seller_name || '').trim(); });
    } catch (e) { toast('Could not load seller names: ' + e.message, 'err'); }
    if (itemScope === 'me') list = list.filter(it => it.seller_id === session.seller_id);
    $('itemsWrap').innerHTML = list.map(it => {
      const mine = it.seller_id === session.seller_id;
      const canEdit = mine || isAdmin();
      const img = it.image_url || PLACEHOLDER;
      const ownerName = nameById[it.seller_id] || ('Seller #' + it.seller_id);
      const foot = canEdit
        ? '<div class="foot"><button class="btn secondary sm" onclick="editItem(' + it.item_id + ')">Edit</button><button class="btn danger sm" onclick="delItem(' + it.item_id + ')">Delete</button></div>'
        : '<div class="foot"><span class="muted" style="font-size:12px">Owned by ' + esc(ownerName) + '</span></div>';
      return '<div class="item-card" data-id="' + it.item_id + '" data-name="' + esc(it.item_name) + '" data-price="' + esc(it.price) + '" data-img="' + esc(it.image_url || '') + '" data-owner="' + it.seller_id + '"><img src="' + esc(img) + '" onerror="this.src=\'' + PLACEHOLDER + '\'"/><div class="body"><div class="name">' + esc(it.item_name) + (mine ? ' <span class="badge me">me</span>' : '') + '</div><div class="price">$' + esc(it.price) + '</div><div class="meta">Item #' + it.item_id + ' \u00b7 ' + esc(ownerName) + '</div></div>' + foot + '</div>';
    }).join('') || '<div class="empty">No items in the catalog</div>';
  } catch (e) { toast(e.message, 'err'); }
}

async function searchItemByName() {
  const name = $('itemSearchName').value.trim();
  const seller = $('itemSearchSeller').value.trim();
  if (!name) { toast('Enter an item name', 'err'); return; }
  try {
    const query = '?item_name=' + encodeURIComponent(name) + (seller ? '&seller_name=' + encodeURIComponent(seller) : '');
    const item = await api('/item/by-name' + query);
    renderSearchItems([item]);
  } catch (e) { toast('Item search failed: ' + e.message, 'err'); }
}

async function searchItemsBySellerName() {
  const seller = $('sellerSearchName').value.trim();
  if (!seller) { toast('Enter a seller name', 'err'); return; }
  try {
    renderSearchItems(await api('/item/by-seller-name?seller_name=' + encodeURIComponent(seller)));
  } catch (e) { toast('Seller item search failed: ' + e.message, 'err'); }
}

async function searchItemsBySellerId() {
  const id = parseInt($('sellerSearchId').value, 10);
  if (!id) { toast('Enter a seller id', 'err'); return; }
  try {
    renderSearchItems(await api('/item/by-seller-id?seller_id=' + id));
  } catch (e) { toast('Seller ID search failed: ' + e.message, 'err'); }
}

function renderSearchItems(items) {
  $('itemSearchResults').innerHTML = (items || []).map(it => {
    const img = it.image_url || PLACEHOLDER;
    return '<div class="item-card"><img src="' + esc(img) + '" /><div class="body"><div class="name">' + esc(it.item_name) + '</div><div class="price">$' + esc(it.price) + '</div><div class="meta">Item #' + esc(it.item_id) + ' · Seller #' + esc(it.seller_id) + '</div></div></div>';
  }).join('') || '<div class="empty">No matching items found.</div>';
}

async function createItem() {
  const item_name = $('iName').value.trim();
  const price = parseFloat($('iPrice').value);
  if (!item_name || isNaN(price)) { toast('Enter an item name and price', 'err'); return; }
  const image_url = $('iImage').value.trim() || null;
  try { await api('/item', 'POST', { seller_id: session.seller_id, item_name, price, image_url }); toast('Item added', 'ok'); $('iName').value = ''; $('iPrice').value = ''; $('iImage').value = ''; if ($('iSellerId')) $('iSellerId').value = ''; loadItems(); }
  catch (e) { toast(e.message, 'err'); }
}

window.editSeller = async function (id) {
  if (!isAdmin()) return;
  const row = Array.from(document.querySelectorAll('#sellersBody tr')).find(r => r.textContent.includes(String(id)));
  const cells = row ? row.querySelectorAll('td') : [];
  const seller_name = prompt('Seller name:', cells[1] ? cells[1].textContent.trim() : '');
  if (seller_name == null || !seller_name.trim()) return;
  const email = prompt('Email:', cells[2] ? cells[2].textContent.trim() : '');
  if (email == null || !email.trim()) return;
  const status = prompt('Status (active/inactive):', cells[3] ? cells[3].textContent.trim() : 'active');
  if (status == null) return;
  try {
    await api('/seller/' + id, 'PUT', { seller_id: id, seller_name: seller_name.trim(), email: email.trim(), status: status.trim().toLowerCase() });
    toast('Seller updated', 'ok');
    loadSellers();
  } catch (e) { toast('Seller update failed: ' + e.message, 'err'); }
};

window.deleteSeller = async function (id) {
  if (!isAdmin()) return;
  if (id === session.seller_id) { toast('Use your profile to delete your own account', 'err'); return; }
  if (!confirm('Delete seller ' + id + '?')) return;
  try {
    await api('/seller/' + id, 'DELETE');
    toast('Seller deleted', 'ok');
    loadSellers();
    loadItems();
  } catch (e) { toast('Seller deletion failed: ' + e.message, 'err'); }
};

window.editItem = async function (id) {
  const card = document.querySelector('.item-card[data-id="' + id + '"]');
  const curName = card ? card.dataset.name : '';
  const curPrice = card ? card.dataset.price : '';
  const curImg = card ? card.dataset.img : '';
  const owner = card ? parseInt(card.dataset.owner, 10) : session.seller_id;
  const item_name = prompt('Item name:', curName);
  if (item_name == null || !item_name.trim()) return;
  const priceStr = prompt('Price:', curPrice);
  if (priceStr == null) return;
  const price = parseFloat(priceStr);
  if (isNaN(price)) { toast('Invalid price', 'err'); return; }
  const image_url = prompt('Image URL (blank = no image):', curImg) || null;
  let seller_id = session.seller_id;
  if (isAdmin()) {
    const sellerIdStr = prompt('Seller id:', String(owner));
    if (sellerIdStr == null) return;
    seller_id = parseInt(sellerIdStr, 10);
    if (!seller_id) { toast('Invalid seller id', 'err'); return; }
  }
  try { await api('/item/' + id, 'PUT', { item_id: id, seller_id, item_name: item_name.trim(), price, image_url }); toast('Item updated', 'ok'); loadItems(); }
  catch (e) { toast(e.message, 'err'); }
};

window.delItem = async function (id) {
  if (!confirm('Delete item ' + id + '?')) return;
  try { await api('/item/' + id, 'DELETE'); toast('Item deleted', 'ok'); loadItems(); }
  catch (e) { toast(e.message, 'err'); }
};

function switchTab(name) {
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.tab === name));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.add('hidden'));
  $('tab-' + name).classList.remove('hidden');
}

function syncSeg(groupId, val) {
  document.querySelectorAll('#' + groupId + ' .seg').forEach(b => b.classList.toggle('active', b.dataset.scope === val));
}

function switchAuth(name) {
  document.querySelectorAll('.authtab').forEach(t => t.classList.toggle('active', t.dataset.auth === name));
  $('authLogin').classList.toggle('hidden', name !== 'login');
  $('authRegister').classList.toggle('hidden', name !== 'register');
}

document.addEventListener('DOMContentLoaded', () => {
  $('loginBtn').onclick = doLogin;
  $('registerBtn').onclick = doRegister;
  $('logoutBtn').onclick = logout;
  $('pSave').onclick = saveProfile;
  $('pDelete').onclick = deleteProfile;
  $('iCreate').onclick = createItem;
  $('itemSearchBtn').onclick = searchItemByName;
  $('sellerSearchBtn').onclick = searchItemsBySeller;

  document.querySelectorAll('input').forEach(input => input.addEventListener('keydown', e => {
    if (e.key !== 'Enter') return;
    const button = input.closest('.inline, .form-row')?.querySelector('button');
    if (button) button.click();
  }));
  document.querySelectorAll('.tab').forEach(t => t.onclick = () => switchTab(t.dataset.tab));
  document.querySelectorAll('.authtab').forEach(t => t.onclick = () => switchAuth(t.dataset.auth));
  document.querySelectorAll('#sellerScope .seg').forEach(b => b.onclick = () => { sellerScope = b.dataset.scope; syncSeg('sellerScope', sellerScope); loadSellers(); });
  document.querySelectorAll('#itemScope .seg').forEach(b => b.onclick = () => { itemScope = b.dataset.scope; syncSeg('itemScope', itemScope); loadItems(); });
});
