// Enable bootstrap tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

const index = "/dashboard"

function gotoUser(id) {
    window.location = `${index}/user/${id}`;
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
    let sure = confirm(`Confirm deletion of detail ${id}/(${name})`);
    if (sure) {
        const detail_url = `${index}/detail/${id}`;
        const url = `${detail_url}/delete`;
        window.location = url;
    }
}

function createCrew(linked_users = null) {
    let name = prompt("Type a name of the crew to create");
    if (name) {
        let url = `${index}/create_crew/${name}`;
        if (linked_users != null) {
            url += `?linked_users=${linked_users}`
        }
        window.location = url;
    }
}

function linkUserWithCrew(user_id) {
    let crew_id = prompt("Enter id of the crew to link with")
    if (crew_id) {
        const url = `${index}/crew/${crew_id}/link?users=${user_id}`;
        window.location = url;
    }
}

function changeCurrency(crew_id, crew_name) {
    let currency = prompt(`Enter a new currency value for crew ${crew_id}/${crew_name}`);
    if (currency != null && parseInt(currency) != NaN) {
        const crew_url = `${index}/crew/${crew_id}`;
        let url = `${crew_url}/set_currency/${currency}`;
        window.location = url;
    }
}

function deleteCrew(id, name) {
    let sure = prompt(`Confirm deletion of crew ${id}/${name} by typing CONFIRM word`);
    if (sure == "CONFIRM") {
        const crew_url = `${index}/crew/${id}`;
        const url = `${crew_url}/delete`;
        window.location = url;
    }
}

function deleteDetailCopy(id, name) {
    let sure = prompt(`Confirm deletion of detail copy ${id}/${name} by typing CONFIRM word`);
    if (sure == "CONFIRM") {
        const dc_url = `${index}/detail_copy/${id}`;
        const url = `${crew_url}/delete`;
        window.location = url;
    }
}
