document.addEventListener('DOMContentLoaded', () => {
    loadUsers();

    document.getElementById('addUserForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('newUserName').value;
        const email = document.getElementById('newUserEmail').value;

        const response = await fetch('/users', {
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
    });
});

async function loadUsers() {
    const response = await fetch('/users');
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
}

function showUserDetails(user) {
    document.getElementById('userId').textContent = user.id;
    document.getElementById('userName').textContent = user.name;
    document.getElementById('userEmail').textContent = user.email;
    const modal = new bootstrap.Modal(document.getElementById('userModal'));
    modal.show();
}