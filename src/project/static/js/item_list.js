var passwords = document.getElementsByClassName('password');

for (var i = 0; i < passwords.length; i++) {
    passwords[i].addEventListener('click', revealPassword);
}

let base_url = window.location.origin;




function revealPassword() {
    var id = this.getAttribute('data-id');

    fetch(base_url+"/display_password/"+id, {
        method: 'GET',
        headers: {
            "Accept": "application/json",
            'X-Requested-With': 'XMLHttpRequest'
        },
    })
    .then(response => {
        return response.json()
    })
    .then(data => {
        this.innerText = data.password;
    })

    this.removeEventListener('click', revealPassword);
    this.addEventListener('click', hidePassword);
}

function hidePassword() {
    this.innerText = '••••••';
    this.removeEventListener('click', hidePassword);
    this.addEventListener('click', revealPassword);
}

function confirmDelete(itemId) {
    if (confirm("Are you sure you want to delete this element ?")) {
        window.location.href = "/delete_item/" + itemId;
    }
}