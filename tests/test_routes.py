import io

from app import store


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


class TestGenerate:
    def test_valid_text_and_size(self, client):
        response = client.post('/generate', data={'text': 'hello', 'size': '10'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert isinstance(data['id'], str)

    def test_invalid_size_non_integer(self, client):
        response = client.post('/generate', data={'text': 'hello', 'size': 'abc'})
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert len(data['errors']) > 0

    def test_missing_size_field(self, client):
        response = client.post('/generate', data={'text': 'hello'})
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False

    def test_text_too_long_returns_validation_error(self, client):
        response = client.post('/generate', data={'text': 'x' * 56, 'size': '10'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is False
        assert len(data['errors']) > 0

    def test_size_out_of_range(self, client):
        response = client.post('/generate', data={'text': 'hi', 'size': '31'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is False


class TestResult:
    def test_valid_token(self, client, qr_token):
        response = client.get(f'/result?id={qr_token}')
        assert response.status_code == 200

    def test_invalid_token_returns_404(self, client):
        response = client.get('/result?id=doesnotexist')
        assert response.status_code == 404

    def test_missing_id_returns_404(self, client):
        response = client.get('/result')
        assert response.status_code == 404


class TestDownload:
    def test_valid_token_returns_png(self, client, qr_token):
        response = client.get(f'/download?id={qr_token}')
        assert response.status_code == 200
        assert response.content_type == 'image/png'

    def test_invalid_token_returns_404(self, client):
        response = client.get('/download?id=bad')
        assert response.status_code == 404

    def test_missing_id_returns_404(self, client):
        response = client.get('/download')
        assert response.status_code == 404


class TestDownloadWithImage:
    def test_token_without_artistic_returns_404(self, client, qr_token):
        response = client.get(f'/download_with_image?id={qr_token}')
        assert response.status_code == 404

    def test_token_with_artistic_returns_200(self, client, qr_with_artistic_token):
        response = client.get(f'/download_with_image?id={qr_with_artistic_token}')
        assert response.status_code == 200
        assert 'image/' in response.content_type

    def test_invalid_token_returns_404(self, client):
        response = client.get('/download_with_image?id=bad')
        assert response.status_code == 404
