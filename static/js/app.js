const State = {
  currentSection: 'discover',
  activeTripId: null,
  dashboard: null,
  destinations: [],
  trips: [],
  currentTrip: null,
  activities: [],
  places: [],
  packing: [],
  journal: [],
  selectedPlaceCategory: 'all'
};

const DEFAULT_FALLBACK_IMAGE = "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=800&q=80";

async function fetchAPI(url, options = {}) {
  try {
    const config = {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      ...options
    };
    if (config.body && typeof config.body === 'object') {
      config.body = JSON.stringify(config.body);
    }
    const resp = await fetch(url, config);
    const result = await resp.json();
    if (!resp.ok || !result.success) {
      throw new Error(result.error || 'Network request failed');
    }
    return result.data;
  } catch (err) {
    showToast(err.message, 'error');
    throw err;
  }
}

function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <span>${type === 'success' ? '✓' : '✕'}</span>
    <div>${message}</div>
  `;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initGlobalSearch();
  initSlidePanels();
  loadInitialData();
});

function initNavigation() {
  const navLinks = document.querySelectorAll('.nav-link[data-section]');
  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const sec = link.getAttribute('data-section');
      switchSection(sec);
    });
  });

  const path = window.location.pathname.replace('/', '');
  if (path && ['discover', 'trips', 'itinerary', 'places'].includes(path)) {
    switchSection(path);
  } else {
    switchSection('discover');
  }
}

function switchSection(secId) {
  State.currentSection = secId;

  document.querySelectorAll('.nav-link[data-section]').forEach(el => {
    if (el.getAttribute('data-section') === secId) {
      el.classList.add('active');
    } else {
      el.classList.remove('active');
    }
  });

  document.querySelectorAll('.section-pane').forEach(pane => {
    if (pane.id === `${secId}-section`) {
      pane.classList.add('active');
    } else {
      pane.classList.remove('active');
    }
  });

  window.history.pushState({}, '', secId === 'discover' ? '/' : `/${secId}`);

  if (secId === 'discover') renderDiscoverSection();
  if (secId === 'trips') renderTripsSection();
  if (secId === 'itinerary') renderItinerarySection();
  if (secId === 'places') renderPlacesSection();
}

async function loadInitialData() {
  try {
    const dbData = await fetchAPI('/api/dashboard');
    State.dashboard = dbData;
    State.trips = dbData.recent_journeys || [];
    State.destinations = dbData.featured_destinations || [];

    if (!State.destinations || State.destinations.length === 0) {
      State.destinations = await fetchAPI('/api/destinations');
    }

    if (!State.trips || State.trips.length === 0) {
      State.trips = await fetchAPI('/api/trips');
    }

    if (State.trips.length > 0 && !State.activeTripId) {
      State.activeTripId = State.trips[0].id;
    }

    renderDashboardStats();
    if (State.currentSection === 'discover') renderDiscoverSection();
  } catch (err) {
    console.error('Initial data load failed', err);
  }
}

function renderDashboardStats() {
  const stats = State.dashboard;
  if (!stats) return;

  const totalTripsEl = document.getElementById('stat-total-trips');
  const activeTripsEl = document.getElementById('stat-active-trips');
  const totalBudgetEl = document.getElementById('stat-total-budget');
  const packingProgressEl = document.getElementById('stat-packing-progress');

  if (totalTripsEl) totalTripsEl.textContent = stats.total_trips !== undefined ? stats.total_trips : 0;
  if (activeTripsEl) activeTripsEl.textContent = stats.upcoming_count !== undefined ? stats.upcoming_count : 0;
  if (totalBudgetEl) totalBudgetEl.textContent = `₹${(stats.total_estimated_budget || 0).toLocaleString('en-IN')}`;
  if (packingProgressEl) packingProgressEl.textContent = `${stats.overall_packing_progress !== undefined ? stats.overall_packing_progress : 0}%`;
}

async function renderDiscoverSection() {
  const grid = document.getElementById('destinations-grid');
  if (!grid) return;

  if (!State.destinations || State.destinations.length === 0) {
    try {
      State.destinations = await fetchAPI('/api/destinations');
    } catch (err) {
      grid.innerHTML = '<div class="empty-state">Unable to load destinations right now.</div>';
      return;
    }
  }

  grid.innerHTML = State.destinations.map(dest => `
    <div class="dest-card">
      <div class="dest-img-container">
        <img src="${dest.image}" alt="${dest.name}" class="dest-img" loading="lazy" onerror="this.onerror=null;this.src='${DEFAULT_FALLBACK_IMAGE}';">
        <span class="dest-badge">${dest.region}</span>
      </div>
      <div class="dest-body">
        <h3 class="dest-name font-heading">${dest.name}</h3>
        <div class="dest-country">📍 ${dest.country} • Recommended ${dest.recommended_days} Days</div>
        <p class="dest-desc">${dest.description}</p>
        <div class="dest-meta-tags">
          ${dest.travel_styles.map(s => `<span class="tag-pill">${s}</span>`).join('')}
        </div>
        <div class="dest-footer">
          <div class="dest-price">Est. Daily: <strong>₹${dest.estimated_daily_budget.toLocaleString('en-IN')}</strong></div>
          <button class="btn btn-sm btn-primary" onclick="openCreateTripModal('${dest.id}', '${dest.name}')">+ Start Trip</button>
        </div>
      </div>
    </div>
  `).join('');
}

async function renderTripsSection() {
  const container = document.getElementById('trips-list-container');
  if (!container) return;

  try {
    State.trips = await fetchAPI('/api/trips');
    if (!State.destinations || State.destinations.length === 0) {
      State.destinations = await fetchAPI('/api/destinations');
    }
    const destMap = {};
    State.destinations.forEach(d => destMap[d.id] = d);

    if (State.trips.length === 0) {
      container.innerHTML = `
        <div class="card-panel text-center" style="padding: 3.5rem 2rem;">
          <div style="font-size: 3rem; margin-bottom: 1rem;">✈️</div>
          <h3 class="font-heading" style="font-size: 1.5rem;">No Journeys Planned Yet</h3>
          <p class="color-muted" style="margin: 0.5rem 0 1.5rem;">Explore curated destinations and build your custom itinerary.</p>
          <button class="btn btn-primary" onclick="switchSection('discover')">Explore Destinations</button>
        </div>
      `;
      return;
    }

    container.innerHTML = State.trips.map(t => {
      const dest = destMap[t.destination_id] || {};
      const imgUrl = dest.image || DEFAULT_FALLBACK_IMAGE;
      const statusClass = t.status ? t.status.toLowerCase().replace(' ', '-') : 'upcoming';

      return `
        <div class="journey-card-modern">
          <div class="journey-cover" style="background-image: url('${imgUrl}');">
            <span class="journey-status-badge status-${statusClass}">${t.status || 'Upcoming'}</span>
          </div>
          <div class="journey-content">
            <div class="journey-main-info">
              <h3 class="journey-title font-heading">${t.name}</h3>
              <div class="journey-destination">📍 ${t.destination_name}, ${t.country}</div>
              <div class="journey-meta-pills">
                <span class="tag-pill">📅 ${t.start_date} to ${t.end_date}</span>
                <span class="tag-pill">👥 ${t.travelers} Traveler(s)</span>
                <span class="tag-pill style-pill">✨ ${t.travel_style || 'Culture'}</span>
              </div>
            </div>
            <div class="journey-actions">
              <button class="btn btn-primary" onclick="viewTripDetails('${t.id}')">View Itinerary & Timeline</button>
              <button class="btn btn-outline btn-icon-only" onclick="deleteTrip('${t.id}')" title="Delete Journey">🗑️</button>
            </div>
          </div>
        </div>
      `;
    }).join('');
  } catch (err) {
    console.error('Failed to load trips', err);
  }
}

async function viewTripDetails(tripId) {
  State.activeTripId = tripId;
  switchSection('itinerary');
}

async function renderItinerarySection() {
  try {
    if (!State.trips || State.trips.length === 0) {
      State.trips = await fetchAPI('/api/trips');
    }
  } catch (err) {
    console.error('Error fetching trips for itinerary', err);
  }

  if (State.trips.length > 0 && !State.activeTripId) {
    State.activeTripId = State.trips[0].id;
  }

  const selector = document.getElementById('trip-selector');
  if (selector && State.trips.length > 0) {
    selector.innerHTML = State.trips.map(t => `
      <option value="${t.id}" ${t.id === State.activeTripId ? 'selected' : ''}>${t.name} (${t.destination_name})</option>
    `).join('');

    selector.onchange = (e) => {
      State.activeTripId = e.target.value;
      renderItinerarySection();
    };
  }

  if (!State.activeTripId) {
    const container = document.getElementById('itinerary-content');
    if (container) container.innerHTML = '<div class="empty-state">Please select or create a journey first.</div>';
    return;
  }

  try {
    const data = await fetchAPI(`/api/trips/${State.activeTripId}`);
    State.currentTrip = data.trip;
    State.activities = data.activities || [];
    State.places = data.places || [];
    State.packing = data.packing || [];
    State.journal = data.journal || data.journal_entries || [];

    renderItineraryTimeline(data);
    renderPackingPanel(State.packing);
    renderJournalPanel(State.journal);
    renderBudgetSummary(data.budget);
  } catch (err) {
    console.error('Failed to load itinerary details', err);
  }
}

function renderItineraryTimeline(data) {
  const container = document.getElementById('itinerary-content');
  if (!container) return;

  const activitiesList = data.activities || [];
  const actsByDay = {};
  activitiesList.forEach(a => {
    if (!actsByDay[a.day]) actsByDay[a.day] = [];
    actsByDay[a.day].push(a);
  });

  const days = Object.keys(actsByDay).sort((a, b) => parseInt(a) - parseInt(b));

  if (days.length === 0) {
    container.innerHTML = `
      <div class="card-panel text-center" style="padding: 3rem 2rem;">
        <h4 class="font-heading" style="font-size: 1.3rem; margin-bottom: 0.5rem;">No Activities Scheduled Yet</h4>
        <p class="color-muted" style="margin-bottom: 1.25rem;">Start building your day-by-day travel timeline.</p>
        <button class="btn btn-primary btn-sm" onclick="openAddActivityModal()">+ Add First Activity</button>
      </div>
    `;
    return;
  }

  let html = `<div class="timeline-container">`;
  days.forEach(d => {
    html += `
      <div class="timeline-day-block">
        <div class="day-badge">Day ${d}</div>
        <div class="day-header">
          <h3 class="day-title font-heading">Day ${d} Schedule</h3>
          <button class="btn btn-sm btn-outline" onclick="openAddActivityModal(${d})">+ Add Activity</button>
        </div>
        ${actsByDay[d].map(act => `
          <div class="activity-card">
            <div class="act-time">⏱️ ${act.time}</div>
            <div class="act-details">
              <div class="act-name">${act.title}</div>
              <div class="act-meta">
                <span>📍 ${act.location}</span>
                <span>⏳ ${act.duration}</span>
                <span class="tag-pill">${act.category}</span>
              </div>
              ${act.notes ? `<div class="act-notes">💡 ${act.notes}</div>` : ''}
            </div>
            <div style="text-align: right;">
              <div class="act-price">₹${act.estimated_cost.toLocaleString('en-IN')}</div>
              <button class="btn btn-sm btn-outline btn-icon-only" style="margin-top: 0.5rem;" onclick="deleteActivity('${act.id}')" title="Delete">🗑️</button>
            </div>
          </div>
        `).join('')}
      </div>
    `;
  });
  html += `</div>`;
  container.innerHTML = html;
}

function renderPackingPanel(items) {
  const container = document.getElementById('packing-list-container');
  const progressFill = document.getElementById('packing-progress-fill');
  const countLabel = document.getElementById('packing-count-label');

  if (!container) return;

  if (!Array.isArray(items)) {
    items = [];
  }

  const total = items.length;
  const done = items.filter(i => i && i.completed).length;
  const pct = total === 0 ? 0 : Math.round((done / total) * 100);

  if (progressFill) progressFill.style.width = `${pct}%`;
  if (countLabel) countLabel.textContent = `${done}/${total} packed (${pct}%)`;

  if (items.length === 0) {
    container.innerHTML = '<div class="color-muted" style="font-size: 0.88rem; padding: 0.5rem 0;">No items on checklist yet.</div>';
    return;
  }

  container.innerHTML = items.map(item => `
    <li class="check-item ${item.completed ? 'completed' : ''}">
      <label class="check-label">
        <input type="checkbox" ${item.completed ? 'checked' : ''} onchange="togglePackingItem('${item.id}', this.checked)">
        <span class="item-name">${item.name}</span>
        <small class="tag-pill">${item.category}</small>
      </label>
      <button class="btn btn-sm btn-outline btn-icon-only" onclick="deletePackingItem('${item.id}')">🗑️</button>
    </li>
  `).join('');
}

function renderJournalPanel(entries) {
  const container = document.getElementById('journal-list-container');
  if (!container) return;

  if (!Array.isArray(entries) || entries.length === 0) {
    container.innerHTML = '<div class="color-muted" style="font-size: 0.88rem; padding: 0.5rem 0;">No journal memories logged yet.</div>';
    return;
  }

  container.innerHTML = entries.map(j => `
    <div class="journal-card">
      <div class="journal-date">Day ${j.day} • ${j.date}</div>
      <h4 class="journal-title font-heading">${j.title}</h4>
      <div class="journal-text">${j.content}</div>
      <button class="btn btn-sm btn-outline btn-icon-only" style="position: absolute; bottom: 1rem; right: 1rem;" onclick="deleteJournalEntry('${j.id}')">🗑️</button>
    </div>
  `).join('');
}

function renderBudgetSummary(budget) {
  if (!budget) return;

  const totalEl = document.getElementById('summary-total-cost');
  const dailyEl = document.getElementById('summary-daily-avg');

  const totalCost = budget.total_estimated !== undefined ? budget.total_estimated : (budget.total_cost || 0);
  const dailyAvg = budget.daily_average !== undefined ? budget.daily_average : 0;

  if (totalEl) totalEl.textContent = `₹${totalCost.toLocaleString('en-IN')}`;
  if (dailyEl) dailyEl.textContent = `₹${dailyAvg.toLocaleString('en-IN')}/day`;
}

async function renderPlacesSection() {
  const container = document.getElementById('places-grid');
  const countBadge = document.getElementById('places-count-badge');
  if (!container) return;

  try {
    const allPlaces = await fetchAPI('/api/places');

    let filtered = allPlaces;
    if (State.selectedPlaceCategory !== 'all') {
      filtered = allPlaces.filter(p => p.category.toLowerCase() === State.selectedPlaceCategory.toLowerCase());
    }

    if (countBadge) {
      countBadge.textContent = `Showing ${filtered.length} Saved Attractions`;
    }

    if (filtered.length === 0) {
      container.innerHTML = '<div class="empty-state">No saved places in this category yet.</div>';
      return;
    }

    container.innerHTML = filtered.map(p => `
      <div class="place-photo-card">
        <div class="place-img-wrapper">
          <img src="${p.image}" alt="${p.name}" class="place-img" loading="lazy" onerror="this.onerror=null;this.src='${DEFAULT_FALLBACK_IMAGE}';">
          <span class="place-category-badge">${p.category}</span>
        </div>
        <div class="place-card-body">
          <h3 class="place-card-title font-heading">${p.name}</h3>
          <p class="place-card-desc">${p.description}</p>
          <div class="place-card-footer">
            <div class="place-ticket-price">
              ${p.estimated_cost > 0 ? `Est. Ticket: <strong>₹${p.estimated_cost.toLocaleString('en-IN')}</strong>` : '<span style="color: var(--color-success); font-weight: 700;">Free Entry</span>'}
            </div>
            <button class="btn btn-sm btn-outline btn-icon-only" onclick="deletePlace('${p.id}')" title="Remove Place">🗑️</button>
          </div>
        </div>
      </div>
    `).join('');
  } catch (err) {
    console.error('Failed to load places', err);
  }
}

function filterPlacesByCategory(cat) {
  State.selectedPlaceCategory = cat;
  document.querySelectorAll('.cat-pill-btn').forEach(btn => {
    if (btn.getAttribute('data-cat') === cat) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });
  renderPlacesSection();
}

function initSlidePanels() {
  const overlay = document.getElementById('slide-overlay');
  const closeBtns = document.querySelectorAll('[data-close-slide]');

  closeBtns.forEach(btn => {
    btn.addEventListener('click', closeSlidePanel);
  });

  if (overlay) {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeSlidePanel();
    });
  }
}

function openSlidePanel(panelId) {
  const overlay = document.getElementById('slide-overlay');
  const panels = document.querySelectorAll('.slide-panel');

  panels.forEach(p => p.classList.remove('active'));

  const target = document.getElementById(panelId);
  if (target && overlay) {
    overlay.classList.add('active');
    target.classList.add('active');
  }
}

function closeSlidePanel() {
  const overlay = document.getElementById('slide-overlay');
  const panels = document.querySelectorAll('.slide-panel');

  panels.forEach(p => p.classList.remove('active'));
  if (overlay) overlay.classList.remove('active');
}

function openCreateTripModal(destId = '', destName = '') {
  const destSelect = document.getElementById('trip-dest-select');
  if (destSelect && State.destinations.length > 0) {
    destSelect.innerHTML = State.destinations.map(d => `
      <option value="${d.id}" ${d.id === destId ? 'selected' : ''}>${d.name} (${d.country})</option>
    `).join('');
  }

  const titleInput = document.getElementById('trip-name-input');
  if (titleInput && destName) {
    titleInput.value = `Journey to ${destName}`;
  }

  openSlidePanel('panel-create-trip');
}

async function submitCreateTrip(e) {
  e.preventDefault();
  const form = e.target;
  const payload = {
    name: form.name.value,
    destination_id: form.destination_id.value,
    start_date: form.start_date.value,
    end_date: form.end_date.value,
    travelers: parseInt(form.travelers.value || 1),
    travel_style: form.travel_style.value
  };

  try {
    const newTripData = await fetchAPI('/api/trips', {
      method: 'POST',
      body: payload
    });
    showToast(`Journey '${payload.name}' created!`);
    closeSlidePanel();
    State.activeTripId = newTripData.trip.id;
    await loadInitialData();
    switchSection('itinerary');
  } catch (err) {
    console.error('Failed to create trip', err);
  }
}

function openAddActivityModal(day = 1) {
  const dayInput = document.getElementById('act-day-input');
  if (dayInput) dayInput.value = day;
  openSlidePanel('panel-add-activity');
}

async function submitCreateActivity(e) {
  e.preventDefault();
  if (!State.activeTripId) {
    showToast('Please select a trip first', 'error');
    return;
  }

  const form = e.target;
  const payload = {
    day: parseInt(form.day.value || 1),
    title: form.title.value,
    time: form.time.value,
    location: form.location.value,
    category: form.category.value,
    duration: form.duration.value,
    estimated_cost: parseFloat(form.estimated_cost.value || 0),
    notes: form.notes.value
  };

  try {
    await fetchAPI(`/api/trips/${State.activeTripId}/activities`, {
      method: 'POST',
      body: payload
    });
    showToast('Activity added to timeline!');
    closeSlidePanel();
    form.reset();
    renderItinerarySection();
  } catch (err) {
    console.error('Failed to add activity', err);
  }
}

async function togglePackingItem(itemId, completed) {
  try {
    await fetchAPI(`/api/packing/${itemId}`, {
      method: 'PATCH',
      body: { completed }
    });
    renderItinerarySection();
  } catch (err) {
    console.error('Failed to update packing status', err);
  }
}

async function submitCreatePacking(e) {
  e.preventDefault();
  if (!State.activeTripId) return;

  const form = e.target;
  const payload = {
    name: form.name.value,
    category: form.category.value
  };

  try {
    await fetchAPI(`/api/trips/${State.activeTripId}/packing`, {
      method: 'POST',
      body: payload
    });
    showToast('Item added to packing list');
    form.reset();
    renderItinerarySection();
  } catch (err) {
    console.error('Failed to create packing item', err);
  }
}

async function submitCreateJournal(e) {
  e.preventDefault();
  if (!State.activeTripId) return;

  const form = e.target;
  const payload = {
    day: parseInt(form.day.value || 1),
    title: form.title.value,
    content: form.content.value
  };

  try {
    await fetchAPI(`/api/trips/${State.activeTripId}/journal`, {
      method: 'POST',
      body: payload
    });
    showToast('Journal memory saved!');
    closeSlidePanel();
    form.reset();
    renderItinerarySection();
  } catch (err) {
    console.error('Failed to create journal entry', err);
  }
}

async function deleteTrip(tripId) {
  if (!confirm('Are you sure you want to delete this journey?')) return;
  try {
    await fetchAPI(`/api/trips/${tripId}`, { method: 'DELETE' });
    showToast('Journey deleted');
    if (State.activeTripId === tripId) State.activeTripId = null;
    await loadInitialData();
    renderTripsSection();
  } catch (err) {
    console.error('Failed to delete trip', err);
  }
}

async function deleteActivity(actId) {
  try {
    await fetchAPI(`/api/activities/${actId}`, { method: 'DELETE' });
    showToast('Activity removed');
    renderItinerarySection();
  } catch (err) {
    console.error('Failed to delete activity', err);
  }
}

async function deletePackingItem(itemId) {
  try {
    await fetchAPI(`/api/packing/${itemId}`, { method: 'DELETE' });
    showToast('Packing item removed');
    renderItinerarySection();
  } catch (err) {
    console.error('Failed to delete packing item', err);
  }
}

async function deleteJournalEntry(entryId) {
  try {
    await fetchAPI(`/api/journal/${entryId}`, { method: 'DELETE' });
    showToast('Journal entry deleted');
    renderItinerarySection();
  } catch (err) {
    console.error('Failed to delete journal entry', err);
  }
}

async function deletePlace(placeId) {
  try {
    await fetchAPI(`/api/places/${placeId}`, { method: 'DELETE' });
    showToast('Saved place removed');
    renderPlacesSection();
  } catch (err) {
    console.error('Failed to delete place', err);
  }
}

function initGlobalSearch() {
  const searchInput = document.getElementById('global-search-input');
  const dropdown = document.getElementById('search-results-dropdown');
  if (!searchInput || !dropdown) return;

  let debounceTimer;

  searchInput.addEventListener('input', (e) => {
    clearTimeout(debounceTimer);
    const query = e.target.value.trim();
    if (query.length < 2) {
      dropdown.classList.remove('show');
      return;
    }

    debounceTimer = setTimeout(async () => {
      try {
        const results = await fetchAPI(`/api/search?q=${encodeURIComponent(query)}`);
        renderSearchResults(results);
      } catch (err) {
        console.error('Search error', err);
      }
    }, 250);
  });

  document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.classList.remove('show');
    }
  });
}

function renderSearchResults(results) {
  const dropdown = document.getElementById('search-results-dropdown');
  if (!dropdown) return;

  let html = '';
  const { destinations, trips, places, activities } = results;

  if (destinations && destinations.length > 0) {
    html += `<div class="search-group-title">Destinations</div>`;
    destinations.forEach(d => {
      html += `
        <div class="search-result-item" onclick="selectSearchResult('dest', '${d.id}')">
          <div>
            <div class="search-result-title">${d.name}</div>
            <div class="search-result-sub">${d.country} • ${d.region}</div>
          </div>
          <span>📍</span>
        </div>
      `;
    });
  }

  if (trips && trips.length > 0) {
    html += `<div class="search-group-title">Journeys</div>`;
    trips.forEach(t => {
      html += `
        <div class="search-result-item" onclick="selectSearchResult('trip', '${t.id}')">
          <div>
            <div class="search-result-title">${t.name}</div>
            <div class="search-result-sub">${t.destination_name} • ${t.status}</div>
          </div>
          <span>✈️</span>
        </div>
      `;
    });
  }

  if (places && places.length > 0) {
    html += `<div class="search-group-title">Attractions</div>`;
    places.forEach(p => {
      html += `
        <div class="search-result-item" onclick="selectSearchResult('place', '${p.id}')">
          <div>
            <div class="search-result-title">${p.name}</div>
            <div class="search-result-sub">${p.category}</div>
          </div>
          <span>🏛️</span>
        </div>
      `;
    });
  }

  if (!html) {
    html = '<div class="color-muted" style="padding: 0.75rem; font-size: 0.88rem;">No matching travel items found.</div>';
  }

  dropdown.innerHTML = html;
  dropdown.classList.add('show');
}

function selectSearchResult(type, id) {
  const dropdown = document.getElementById('search-results-dropdown');
  if (dropdown) dropdown.classList.remove('show');

  if (type === 'dest') {
    switchSection('discover');
  } else if (type === 'trip') {
    State.activeTripId = id;
    switchSection('itinerary');
  } else if (type === 'place') {
    switchSection('places');
  }
}
