
let allEmployees = [];
let visibleCount = 20;
let filteredEmployees = [];

function loadEmployees() {
    fetch('/rgz/rest-api/employees/')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            allEmployees = data;
            filteredEmployees = data.slice();
            renderEmployees();
        })
        .catch(function(error) {
            console.log("Произошла ошибка:", error);
        });
}

function renderEmployees() {
    let tbody = document.getElementById('employee-list');
    tbody.innerHTML = '';
    
    if (filteredEmployees.length == 0) {
        tbody.innerHTML = '<tr><td colspan="3">Нет данных</td></tr>';
        return;
    }

    let toShow = filteredEmployees.slice(0, visibleCount);
    
    let showMoreBtn = document.querySelector('button[onclick="showMore()"]');
    if (showMoreBtn) {
        showMoreBtn.style.display = (visibleCount >= filteredEmployees.length) ? 'none' : 'block';
    }
    
    
    for (let emp of toShow) {
        let tr = document.createElement('tr');
        
        let tdName = document.createElement('td');
        tdName.textContent = emp.full_name || '';
        
        let tdPosition = document.createElement('td');
        tdPosition.textContent = emp.position || '';

        let tdEmail = document.createElement('td');
        tdEmail.textContent = emp.email || '';
    
        tr.append(tdName);
        tr.append(tdPosition);
        tr.append(tdEmail);
        tbody.append(tr);
        
        if (emp.can_edit) {
            let tdActions = document.createElement('td');
            tr.append(tdActions);
            let editBtn = document.createElement('button');
            editBtn.textContent = 'редактировать';
            editBtn.onclick = function() { editEmployee(emp.id); };
            
            let delBtn = document.createElement('button');
            delBtn.textContent = 'удалить';
            delBtn.onclick = function() { deleteEmployee(emp.id); };
            
            tdActions.append(editBtn);
            tdActions.append(delBtn);
        }
        
    }
}

function showMore() {
    visibleCount += 20;
    renderEmployees();
}

function searchEmployees() {
    let text = document.getElementById("search-input").value.toLowerCase();

    if (text == "") {
        filteredEmployees = allEmployees.slice();
    } else {
        filteredEmployees = allEmployees.filter(function(emp) {
            let name = (emp.full_name || "").toLowerCase();
            let pos = (emp.position || "").toLowerCase();
            let email = (emp.email || "").toLowerCase();

            return name.includes(text) ||
                   pos.includes(text) ||
                   email.includes(text);
        });
    }
    visibleCount = 20;

    renderEmployees();
}

function sortBy(field) {
    filteredEmployees.sort(function(a, b) {
        let x = (a[field] || "").toLowerCase();
        let y = (b[field] || "").toLowerCase();

        if (x < y) return -1;
        if (x > y) return 1;
        return 0;
    });

    visibleCount = 20;

    renderEmployees();
}


document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('employee-list')) {
        loadEmployees();
    }
});


function deleteEmployee(id) {
    if (!confirm(`Вы точно хотите удалить сотрудника?`)) return;

    fetch(`/rgz/rest-api/employees/${id}`, { method: 'DELETE' })
    .then(resp => {
        if (resp.ok) {
            alert('Сотрудник удалён!');
            loadEmployees();
        } else {
            alert('Ошибка удаления сотрудника');
        }
    });

}

function showModal() {
    document.getElementById('fullname-error').innerText = '';
    document.getElementById('position-error').innerText = '';
    document.getElementById('gender-error').innerText = '';
    document.getElementById('phone-error').innerText = '';
    document.getElementById('email-error').innerText = '';
    document.getElementById('trial-error').innerText = '';
    document.getElementById('hire-date-error').innerText = '';
    document.querySelector('div.modal').style.display = 'block';
}
function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}
function cancel() {
    hideModal();
}

function editEmployee(id) {
    fetch(`/rgz/rest-api/employees/${id}`)
    .then(function (data) {
        return data.json();
    })
    .then(function (employee) {
        document.getElementById('id').value = id;
        document.getElementById('full_name').value = employee.full_name;
        document.getElementById('position').value = employee.position;
        document.getElementById('gender').value = employee.gender;
        document.getElementById('phone').value = employee.phone;
        document.getElementById('email').value = employee.email;
        document.getElementById('trial').value = employee.trial ? '1' : '0';
        document.getElementById('hire_date').value = employee.hire_date;
        showModal();
    })
}

function sendEmployee() {
    const id = document.getElementById('id').value;
    const employee = {
        full_name: document.getElementById('full_name').value,
        position: document.getElementById('position').value,
        gender: document.getElementById('gender').value,
        phone: document.getElementById('phone').value,
        email: document.getElementById('email').value,
        trial: document.getElementById('trial').value,
        hire_date: document.getElementById('hire_date').value
    };

    const url = `/rgz/rest-api/employees/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    document.getElementById('fullname-error').innerText = '';
    document.getElementById('position-error').innerText = '';
    document.getElementById('gender-error').innerText = '';
    document.getElementById('phone-error').innerText = '';
    document.getElementById('email-error').innerText = '';
    document.getElementById('trial-error').innerText = '';
    document.getElementById('hire-date-error').innerText = '';

    fetch(url, {
        method: method,
        headers: {"Content-type": "application/json"},
        body: JSON.stringify(employee)
    })
    .then(resp => {
        if(resp.ok) {
            loadEmployees();
            hideModal();
            return {};
        }
        return resp.json();
    })
    .then(errors => {
        if(errors.full_name)
            document.getElementById('fullname-error').innerText = errors.full_name;
        if(errors.position)
            document.getElementById('position-error').innerText = errors.position;
        if(errors.gender)
            document.getElementById('gender-error').innerText = errors.gender;
        if(errors.phone)
            document.getElementById('phone-error').innerText = errors.phone;
        if(errors.email)
            document.getElementById('email-error').innerText = errors.email;
        if(errors.trial)
            document.getElementById('trial-error').innerText = errors.trial;
        if(errors.hire_date)
            document.getElementById('hire-date-error').innerText = errors.hire_date;
    });
}


