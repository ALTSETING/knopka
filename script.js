const API_URL = (window.localStorage.getItem('api_url') || 'https://knopka-xc6q.onrender.com').replace(/\/$/, '');

const statsLabels = {
  done: 'Done',
  in_progress: 'In progress',
  ongoing: 'Ongoing',
  waiting_review: 'Waiting review'
};

const usernameEl = document.getElementById('username');
const pendingEl = document.getElementById('pending');
const avatarEl = document.getElementById('avatar');
const featuredTitleEl = document.getElementById('featuredTitle');
const featuredAssigneesEl = document.getElementById('featuredAssignees');
const statsGridEl = document.getElementById('statsGrid');
const timelineEl = document.getElementById('timeline');
const taskFormEl = document.getElementById('taskForm');

async function fetchJSON(path, options) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  return response.json();
}

function renderStats(stats) {
  statsGridEl.innerHTML = Object.entries(stats)
    .map(([key, value]) => `
      <article class="stat-card">
        <strong>${value}</strong>
        <span>${statsLabels[key] || key}</span>
      </article>
    `)
    .join('');
}

function renderTasks(tasks) {
  timelineEl.innerHTML = tasks
    .map(
      (task) => `
      <article class="task-row">
        <h3>${task.title}</h3>
        <small>${task.assignees.join(', ')}</small><br />
        <small>${task.time}</small>
      </article>
    `
    )
    .join('');
}

async function loadDashboard() {
  try {
    const dashboard = await fetchJSON('/api/dashboard');
    const tasks = await fetchJSON('/api/tasks');

    usernameEl.textContent = dashboard.user.name;
    pendingEl.textContent = dashboard.user.pending;
    avatarEl.src = dashboard.user.avatar;
    featuredTitleEl.textContent = dashboard.featured_task?.title || 'No tasks yet';
    featuredAssigneesEl.textContent = (dashboard.featured_task?.assignees || []).join(' and ');

    renderStats(dashboard.stats);
    renderTasks(tasks);
  } catch (error) {
    timelineEl.innerHTML = `<p>Backend недоступний. Встав API URL через localStorage key <b>api_url</b>.</p>`;
    console.error(error);
  }
}

taskFormEl.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(taskFormEl);

  try {
    await fetchJSON('/api/tasks', {
      method: 'POST',
      body: JSON.stringify({
        title: formData.get('title'),
        time: formData.get('time'),
        assignees: ['Mike', 'Anita'],
        status: 'ongoing',
        date: '2026-04-12'
      })
    });
    taskFormEl.reset();
    await loadDashboard();
  } catch (error) {
    alert('Не вдалося додати задачу. Перевір API URL.');
  }
});

loadDashboard();
