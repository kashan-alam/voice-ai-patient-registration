from uuid import UUID


PATIENT_DATA = {
    "first_name": "John",
    "last_name": "Smith",
    "date_of_birth": "1995-05-10",
    "sex": "Male",
    "phone_number": "415-555-1234",
    "address_line_1": "123 Main Street",
    "address_line_2": None,
    "city": "San Francisco",
    "state": "CA",
    "zip_code": "94105",
    "email": "john.smith@example.com",
    "insurance_provider": "Example Health",
    "insurance_member_id": "ABC12345",
    "preferred_language": "English",
    "emergency_contact_name": "Jane Smith",
    "emergency_contact_phone": "415-555-5678",
}


def test_create_patient(client):
    response = client.post(
        "/patients",
        json=PATIENT_DATA,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["error"] is None
    assert body["data"]["first_name"] == "John"
    assert body["data"]["last_name"] == "Smith"

    patient_id = body["data"]["patient_id"]

    UUID(patient_id)


def test_get_patients(client):
    response = client.get("/patients")

    assert response.status_code == 200

    body = response.json()

    assert body["error"] is None
    assert isinstance(body["data"], list)


def test_get_patient_by_id(client):
    create_response = client.post(
        "/patients",
        json=PATIENT_DATA,
    )

    assert create_response.status_code == 201

    patient_id = create_response.json()["data"]["patient_id"]

    response = client.get(
        f"/patients/{patient_id}"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["error"] is None
    assert body["data"]["patient_id"] == patient_id


def test_update_patient(client):
    create_response = client.post(
        "/patients",
        json=PATIENT_DATA,
    )

    patient_id = create_response.json()["data"]["patient_id"]

    response = client.put(
        f"/patients/{patient_id}",
        json={
            "phone_number": "415-555-9999",
            "city": "Oakland",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["error"] is None
    assert body["data"]["phone_number"] == "4155559999"
    assert body["data"]["city"] == "Oakland"
    assert body["data"]["first_name"] == "John"


def test_delete_patient(client):
    create_response = client.post(
        "/patients",
        json=PATIENT_DATA,
    )

    patient_id = create_response.json()["data"]["patient_id"]

    response = client.delete(
        f"/patients/{patient_id}"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["error"] is None
    assert body["data"]["deleted_at"] is not None


def test_deleted_patient_is_not_found(client):
    create_response = client.post(
        "/patients",
        json=PATIENT_DATA,
    )

    patient_id = create_response.json()["data"]["patient_id"]

    delete_response = client.delete(
        f"/patients/{patient_id}"
    )

    assert delete_response.status_code == 200

    response = client.get(
        f"/patients/{patient_id}"
    )

    assert response.status_code == 404

    body = response.json()

    assert body["data"] is None
    assert body["error"]["message"] == "Patient not found"


def test_invalid_patient_data(client):
    invalid_data = {
        **PATIENT_DATA,
        "phone_number": "123",
        "state": "XX",
        "zip_code": "123",
        "date_of_birth": "2035-01-01",
    }

    response = client.post(
        "/patients",
        json=invalid_data,
    )

    assert response.status_code == 422

    body = response.json()

    assert body["data"] is None
    assert body["error"] is not None


def test_nonexistent_patient(client):
    patient_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(
        f"/patients/{patient_id}"
    )

    assert response.status_code == 404

    body = response.json()

    assert body["data"] is None
    assert body["error"]["message"] == "Patient not found"