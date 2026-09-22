import io
from PIL import Image
from conftest import client


def make_test_image():
    img = Image.new("RGB", (500, 500), color="blue")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf


def test_create_thumbnail_with_preset():
    buf = make_test_image()
    response = client.post(
        "/thumbnails",
        files=[("files", ("test.jpg", buf, "image/jpeg"))],
        data={"preset": "small"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data[0]["width"] <= 150
    assert data[0]["height"] <= 150


def test_create_thumbnail_with_custom_dimensions():
    buf = make_test_image()
    response = client.post(
        "/thumbnails",
        files=[("files", ("test.jpg", buf, "image/jpeg"))],
        data={"width": 100, "height": 100},
    )
    assert response.status_code == 200
    assert response.json()[0]["width"] <= 100


def test_create_multiple_thumbnails_at_once():
    buf1 = make_test_image()
    buf2 = make_test_image()
    response = client.post(
        "/thumbnails",
        files=[
            ("files", ("test1.jpg", buf1, "image/jpeg")),
            ("files", ("test2.jpg", buf2, "image/jpeg")),
        ],
        data={"preset": "small"},
    )
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_create_thumbnail_invalid_preset():
    buf = make_test_image()
    response = client.post(
        "/thumbnails",
        files=[("files", ("test.jpg", buf, "image/jpeg"))],
        data={"preset": "not_a_real_preset"},
    )
    assert response.status_code == 400


def test_create_thumbnail_missing_preset_and_dimensions():
    buf = make_test_image()
    response = client.post(
        "/thumbnails",
        files=[("files", ("test.jpg", buf, "image/jpeg"))],
    )
    assert response.status_code == 422


def test_get_thumbnail_not_found():
    response = client.get("/thumbnails/fake-nonexistent-id")
    assert response.status_code == 404


def test_create_and_retrieve_thumbnail():
    buf = make_test_image()
    create_response = client.post(
        "/thumbnails",
        files=[("files", ("test.jpg", buf, "image/jpeg"))],
        data={"preset": "medium"},
    )
    thumbnail_id = create_response.json()[0]["id"]

    get_response = client.get(f"/thumbnails/{thumbnail_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == thumbnail_id

    download_response = client.get(f"/thumbnails/{thumbnail_id}/download")
    assert download_response.status_code == 200
    assert download_response.headers["content-type"] == "image/jpeg"


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}