// Enable bootstrap tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

const index = "/dashboard"

function gotoUser(id) {
    window.location = `${index}/user/${id}`;
}

function changeCurrency(user_id, user_login, old_currency) {
    let currency = prompt(`Enter a new currency value for ${user_login}`, old_currency);
    if (currency != null && parseInt(currency) != NaN) {
        const user_url = `${index}/user/${user_id}`;
        let url = `${user_url}/set_currency/${currency}`;
        window.location = url;
    }
}

function changeLogin(user_id, user_login, old_login) {
    let login = prompt(`Type a new login for user ${user_login}`, old_login);
    if (login != null) {
        const user_url = `${index}/user/${user_id}`;
        const url = `${user_url}/set_login/${login}`;
        window.location = url;
    }
}

function resetPassword(user_id, user_login) {
    let password = prompt(`Type a new password for user ${user_login}`);
    if (password != null) {
        const user_url = `${index}/user/${user_id}`;
        const url = `${user_url}/set_password/${password}`;
        window.location = url;
    }
}

function deleteUser(user_id, user_login) {
    let sure = confirm(`Confirm deletion of user ${user_id}/${user_login}`);
    if (sure) {
        const user_url = `${index}/user/${user_id}`;
        const url = `${user_url}/delete`;
        window.location = url;
    }
}

function gotoDetailType(id, lang) {
    window.location = `${index}/detail_type/${id}?lang=${lang}`;
}

function deleteDetailType(id, name) {
    let sure = confirm(`Confirm deletion of detail type "${name}" with id ${id}`);
    if (sure) {
        const dt_url = `${index}/detail_type/${id}`;
        const url = `${dt_url}/delete`;
        window.location = url;
    }
}

function deleteDetail(id, name) {
    let sure = confirm(`Confirm deletion of detail "${name}" with id ${id}`);
    if (sure) {
        const dt_url = `${index}/detail/${id}`;
        const url = `${dt_url}/delete`;
        window.location = url;
    }
}

function createCrew() {
    let name = prompt("Type a name of the crew to create");
    if (name) {
        const url = `${index}/create_crew/${name}`;
        window.location = url;
    }
}
