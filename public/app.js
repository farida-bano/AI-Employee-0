// API endpoint - change this to your API URL when deployed
const API_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : '/api';

// Load dashboard data
async function loadDashboard() {
    try {
        await Promise.all([
            loadStats(),
            loadTasks(),
            loadReports(),
            loadLogs()
        ]);

        document.getElementById('last-update').textContent =
            `Last updated: ${new Date().toLocaleTimeString()}`;
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch(`${API_URL}/api/stats`);
        const stats = await response.json();

        document.getElementById('inbox-count').textContent = stats.inbox_count;
        document.getElementById('needs-action-count').textContent = stats.needs_action_count;
        document.getElementById('done-count').textContent = stats.done_count;
        document.getElementById('error-count').textContent = stats.error_count;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Load tasks
async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/api/tasks`);
        const tasks = await response.json();

        // Render inbox tasks
        const inboxHtml = tasks.inbox.length > 0
            ? tasks.inbox.map(task => `
                <div class="task-item">
                    <h4>${task.name}</h4>
                    <small>Modified: ${new Date(task.modified).toLocaleString()}</small>
                </div>
            `).join('')
            : '<p>No tasks in inbox</p>';
        document.getElementById('inbox-tasks').innerHTML = inboxHtml;

        // Render needs action tasks
        const needsActionHtml = tasks.needs_action.length > 0
            ? tasks.needs_action.map(task => `
                <div class="task-item">
                    <h4>${task.name}</h4>
                    <p>${task.content}</p>
                    <small>Modified: ${new Date(task.modified).toLocaleString()}</small>
                </div>
            `).join('')
            : '<p>No tasks need action</p>';
        document.getElementById('needs-action-tasks').innerHTML = needsActionHtml;

        // Render done tasks
        const doneHtml = tasks.done.length > 0
            ? tasks.done.map(task => `
                <div class="task-item">
                    <h4>${task.name}</h4>
                    <small>Completed: ${new Date(task.modified).toLocaleString()}</small>
                </div>
            `).join('')
            : '<p>No completed tasks</p>';
        document.getElementById('done-tasks').innerHTML = doneHtml;
    } catch (error) {
        console.error('Error loading tasks:', error);
    }
}

// Load reports
async function loadReports() {
    try {
        const response = await fetch(`${API_URL}/api/reports`);
        const reports = await response.json();

        const reportsHtml = reports.length > 0
            ? reports.map(report => `
                <div class="report-item" onclick="showReport('${report.name}', \`${report.content.replace(/`/g, '\\`')}\`)">
                    <h4>${report.name}</h4>
                    <small>Updated: ${new Date(report.modified).toLocaleString()}</small>
                </div>
            `).join('')
            : '<p>No reports available</p>';
        document.getElementById('reports-list').innerHTML = reportsHtml;
    } catch (error) {
        console.error('Error loading reports:', error);
    }
}

// Load logs
async function loadLogs() {
    try {
        const response = await fetch(`${API_URL}/api/logs`);
        const logs = await response.json();

        document.getElementById('system-log-content').textContent =
            logs.system.length > 0 ? logs.system.join('\n') : 'No system logs';

        document.getElementById('errors-log-content').textContent =
            logs.errors.length > 0 ? logs.errors.join('\n') : 'No errors';

        document.getElementById('business-log-content').textContent =
            logs.business.length > 0 ? logs.business.join('\n') : 'No business logs';
    } catch (error) {
        console.error('Error loading logs:', error);
    }
}

// Show report in alert (you can make this a modal later)
function showReport(name, content) {
    alert(`Report: ${name}\n\n${content}`);
}

// Tab switching for tasks
function showTab(tabName) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName).classList.add('active');

    // Add active class to clicked button
    event.target.classList.add('active');
}

// Tab switching for logs
function showLogTab(tabName) {
    // Hide all log tab contents
    const logTabs = ['system-log', 'errors-log', 'business-log'];
    logTabs.forEach(tab => {
        document.getElementById(tab).classList.remove('active');
    });

    // Remove active class from all log buttons
    event.target.parentElement.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected log tab
    document.getElementById(`${tabName}-log`).classList.add('active');

    // Add active class to clicked button
    event.target.classList.add('active');
}

// Auto-refresh every 30 seconds
setInterval(loadDashboard, 30000);

// Load dashboard on page load
window.addEventListener('DOMContentLoaded', loadDashboard);
