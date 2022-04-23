function apiCheckReservation(date, service) {
    return fetch(`/reservation/${date}/${service}`,
    ).then(res => res.json())

            .then(data => {
                 if (data.is_available) {
                     commentBox.removeAttribute("disabled");
                     submitButton.removeAttribute("disabled");
                     message.innerText = "";
                 } else {
                     commentBox.setAttribute("disabled", "");
                     submitButton.setAttribute("disabled", "");
                     message.innerText = "Wybrany termin jest zajęty";
                 }
            }).catch(error => {
                console.log(error);
            });
    }

const submitButton = document.querySelector("input[type='submit']");
submitButton.setAttribute("disabled", "");
const commentBox = document.getElementById("id_comments");
commentBox.setAttribute("disabled", "");
const dateTable = document.getElementById("id_target_date");
dateTable.setAttribute("disabled", "");
const message = document.getElementById("message");
const serviceButton = document.getElementById("id_service_type")

if (serviceButton.selectedIndex !== 0) {
    dateTable.removeAttribute("disabled");
    }

serviceButton.addEventListener('change', (event) => {
    dateTable.value = null;
    message.innerText = "";
    commentBox.setAttribute("disabled", "");
    submitButton.setAttribute("disabled", "");
    if (serviceButton.selectedIndex !== 0) {
        dateTable.removeAttribute("disabled");
    }else {
        dateTable.setAttribute("disabled", "");
    }
});

dateTable.addEventListener('change', (event) => {
    let dateId = dateTable.value;
    let serviceId = serviceButton.value;
    apiCheckReservation(dateId, serviceId)
});
