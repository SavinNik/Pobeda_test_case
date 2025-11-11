const API_BASE = '/api';

document.addEventListener('DOMContentLoaded', () => {
    loadUsers();

    document.getElementById('addUserForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('newUserName').value;
        const email = document.getElementById('newUserEmail').value;

        try {
            const response = await fetch(`${API_BASE}/users`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email })
            });

            const result = await response.json();

            if (response.ok) {
                document.getElementById('message').innerHTML = '<div class="alert alert-success">User added!</div>';
                loadUsers();
                document.getElementById('addUserForm').reset();
            } else {
                document.getElementById('message').innerHTML = `<div class="alert alert-danger">${result.error}</div>`;
            }
        } catch (error) {
            document.getElementById('message').innerHTML = '<div class="alert alert-danger">Network error</div>';
        }
    });
});

async function loadUsers() {
    try {
        const response = await fetch(`${API_BASE}/users`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const users = await response.json();

        const tbody = document.getElementById('usersTableBody');
        tbody.innerHTML = '';

        users.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.email}</td>
            `;
            row.addEventListener('click', () => showUserDetails(user));
            tbody.appendChild(row);
        });
    } catch (error) {
        document.getElementById('usersTableBody').innerHTML = '<tr><td colspan="3">Failed to load users</td></tr>';
    }
}

function showUserDetails(user) {
    document.getElementById('userId').textContent = user.id;
    document.getElementById('userName').textContent = user.name;
    document.getElementById('userEmail').textContent = user.email;
    const modal = new bootstrap.Modal(document.getElementById('userModal'));
    modal.show();
}