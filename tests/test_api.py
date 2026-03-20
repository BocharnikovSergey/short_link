import pytest


MAX_LEN_SHORT_LINK = 20
CLICK_LINK = 5


@pytest.mark.asyncio
async def test_create_short_id(client, url):
    """Проверяет создание короткой ссылки."""
    response = await client.post('/shorten', json={'url': url})
    assert response.status_code == 201
    data = response.json()
    assert 'short_id' in data
    assert data['short_id']
    assert isinstance(data['short_id'], str)
    assert len(data['short_id']) <= MAX_LEN_SHORT_LINK


@pytest.mark.asyncio
async def test_short_id_unique(client, url):
    """Проверяем, что при одинаковом запросе возвращает одинаковый ответ."""

    response1 = await client.post('/shorten', json={'url': url})
    response2 = await client.post('/shorten', json={'url': url})

    assert response1.json()['short_id'] == response2.json()['short_id']


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'url, expected_status',
    [
        ('htp://example.com', 422),
        ('example.com', 422),
        ('/path/to/page.html', 422),
        ('http:///', 422),
        ('', 422),
        ('https://example.com/', 201),
        ('https://google.com/', 201),
        ('https://ya.ru/', 201),
    ],
)
async def test_valid_and_invalid_urls(client, url, expected_status):
    """Проверяем создание разных URL."""

    response = await client.post('/shorten', json={'url': url})
    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_redirect(client, url):
    """Проверяет, что переход по короткой ссылке введет на тот же URL"""
    response = await client.post(
        '/shorten', json={'url': url}
    )
    short_id = response.json().get('short_id')
    redirect_response = await client.get(
        f'/{short_id}', follow_redirects=False
    )
    assert redirect_response.status_code in (302, 307)
    assert redirect_response.headers['location'] == url


@pytest.mark.asyncio
async def test_redirect_not_found(client):
    """Проверяе, что при получении количества переходов по несуществующей
    ссылки не существует."""
    response = await client.get('/djfkd')
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_click_link(client, short_id):
    """Проверяет, что счетчик увеличивается при переходе по короткой ссылке."""
    for _ in range(CLICK_LINK):
        await client.get(f'/{short_id}')
    stats_response = await client.get(f'/stats/{short_id}')
    data = stats_response.json()
    assert stats_response.status_code == 200
    assert 'click_link' in data
    assert data.get('click_link') == CLICK_LINK


@pytest.mark.asyncio
async def test_stats_not_found(client):
    """Проверяе, что при получении количества переходов по несуществующей
    ссылки не существует."""
    response = await client.get('/stats/djfkd')
    assert response.status_code == 404
