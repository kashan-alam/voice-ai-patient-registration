const API_BASE_URL = "/patients";


document.addEventListener(
    "DOMContentLoaded",
    () => {
        loadPatients();
    }
);


async function loadPatients() {

    const lastName =
        document.getElementById("lastName").value.trim();

    const dateOfBirth =
        document.getElementById("dateOfBirth").value;

    const phoneNumber =
        document.getElementById("phoneNumber").value.trim();


    const params = new URLSearchParams();


    if (lastName) {
        params.append(
            "last_name",
            lastName
        );
    }


    if (dateOfBirth) {
        params.append(
            "date_of_birth",
            dateOfBirth
        );
    }


    if (phoneNumber) {
        params.append(
            "phone_number",
            phoneNumber
        );
    }


    const queryString =
        params.toString();


    const url =
        queryString
            ? `${API_BASE_URL}?${queryString}`
            : API_BASE_URL;


    try {

        const response =
            await fetch(url);


        const result =
            await response.json();


        if (!response.ok) {

            showMessage(
                result.error?.message ||
                "Failed to load patients.",
                "error"
            );

            return;
        }


        renderPatients(
            result.data
        );


    } catch (error) {

        console.error(error);

        showMessage(
            "Unable to connect to the API.",
            "error"
        );
    }
}


function renderPatients(patients) {

    const container =
        document.getElementById(
            "patientTableContainer"
        );


    if (!patients.length) {

        container.innerHTML = `
            <div class="empty">
                No patients found.
            </div>
        `;

        return;
    }


    const rows =
        patients.map(
            patient => `
                <tr>

                    <td>
                        ${escapeHtml(patient.first_name)}
                        ${escapeHtml(patient.last_name)}
                    </td>

                    <td>
                        ${escapeHtml(patient.date_of_birth)}
                    </td>

                    <td>
                        ${escapeHtml(patient.sex)}
                    </td>

                    <td>
                        ${formatPhone(patient.phone_number)}
                    </td>

                    <td>
                        ${escapeHtml(patient.city)},
                        ${escapeHtml(patient.state)}
                    </td>

                    <td>
                        <div class="actions">

                            <button
                                class="primary"
                                onclick="viewPatient('${patient.patient_id}')"
                            >
                                View
                            </button>

                            <button
                                class="danger"
                                onclick="deletePatient('${patient.patient_id}')"
                            >
                                Delete
                            </button>

                        </div>
                    </td>

                </tr>
            `
        ).join("");


    container.innerHTML = `
        <table>

            <thead>
                <tr>
                    <th>Name</th>
                    <th>Date of Birth</th>
                    <th>Sex</th>
                    <th>Phone</th>
                    <th>Location</th>
                    <th>Actions</th>
                </tr>
            </thead>

            <tbody>
                ${rows}
            </tbody>

        </table>
    `;
}


async function viewPatient(patientId) {

    try {

        const response =
            await fetch(
                `${API_BASE_URL}/${patientId}`
            );


        const result =
            await response.json();


        if (!response.ok) {

            showMessage(
                result.error?.message ||
                "Unable to retrieve patient.",
                "error"
            );

            return;
        }


        const patient =
            result.data;


        alert(
            `Patient Details\n\n` +

            `Name: ${patient.first_name} ${patient.last_name}\n` +

            `DOB: ${patient.date_of_birth}\n` +

            `Sex: ${patient.sex}\n` +

            `Phone: ${formatPhone(patient.phone_number)}\n` +

            `Address: ${patient.address_line_1}` +

            `${patient.address_line_2
                ? ", " + patient.address_line_2
                : ""}\n` +

            `City: ${patient.city}\n` +

            `State: ${patient.state}\n` +

            `ZIP: ${patient.zip_code}\n` +

            `Email: ${patient.email || "Not provided"}\n` +

            `Insurance: ${patient.insurance_provider || "Not provided"}\n` +

            `Preferred Language: ${patient.preferred_language}`
        );


    } catch (error) {

        console.error(error);

        showMessage(
            "Unable to connect to the API.",
            "error"
        );
    }
}


async function deletePatient(patientId) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this patient?"
        );


    if (!confirmed) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/${patientId}`,
                {
                    method: "DELETE"
                }
            );


        const result =
            await response.json();


        if (!response.ok) {

            showMessage(
                result.error?.message ||
                "Unable to delete patient.",
                "error"
            );

            return;
        }


        showMessage(
            "Patient deleted successfully.",
            "success"
        );


        await loadPatients();


    } catch (error) {

        console.error(error);

        showMessage(
            "Unable to connect to the API.",
            "error"
        );
    }
}


function clearFilters() {

    document.getElementById(
        "lastName"
    ).value = "";


    document.getElementById(
        "dateOfBirth"
    ).value = "";


    document.getElementById(
        "phoneNumber"
    ).value = "";


    loadPatients();
}


function showMessage(
    message,
    type
) {

    const element =
        document.getElementById(
            "message"
        );


    element.textContent =
        message;


    element.className =
        `message ${type}`;


    setTimeout(
        () => {
            element.className =
                "message";
        },
        4000
    );
}


function formatPhone(phone) {

    if (!phone) {
        return "";
    }


    if (phone.length !== 10) {
        return phone;
    }


    return `(${phone.slice(0, 3)}) ` +
           `${phone.slice(3, 6)}-` +
           `${phone.slice(6)}`;
}


function escapeHtml(value) {

    if (value === null || value === undefined) {
        return "";
    }


    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}