"""
ServerHub — Scraper Görevleri
Kullanım: python manage.py shell -c "from apps.scraper.tasks import run_scraper; run_scraper()"
Veya cron/Celery ile periyodik çalıştırılabilir.
"""
import logging
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.utils.text import slugify

logger = logging.getLogger(__name__)

TIMEOUT = getattr(settings, 'SCRAPE_REQUEST_TIMEOUT', 10)
MAX_RETRIES = getattr(settings, 'SCRAPE_MAX_RETRIES', 2)


def fetch_page(url: str) -> str | None:
    """Belirtilen URL'den HTML içeriğini getirir."""
    headers = {'User-Agent': 'Mozilla/5.0 (ServerHub-Bot/1.0)'}
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(url, headers=headers, timeout=TIMEOUT)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as exc:
            logger.warning(f'Fetch hatası [{attempt + 1}/{MAX_RETRIES}]: {exc}')
    return None


def parse_metin2_servers(html: str) -> list[dict]:
    """
    Örnek parser — Metin2 server listesi sitesinden veri çeker.
    Gerçek siteye göre CSS seçicileri düzenlenmeli.
    """
    soup = BeautifulSoup(html, 'lxml')
    servers = []

    for row in soup.select('.server-row, .server-card, tr.server'):
        try:
            name_el = row.select_one('.server-name, .name, td.name')
            exp_el  = row.select_one('.exp, .exp-rate, td.exp')
            web_el  = row.select_one('a.website, a[href*="http"]')

            if not name_el:
                continue

            servers.append({
                'name':     name_el.get_text(strip=True),
                'exp_rate': int(exp_el.get_text(strip=True).replace('x', '').strip()) if exp_el else 1,
                'website':  web_el['href'] if web_el and web_el.get('href') else '',
            })
        except (ValueError, TypeError, KeyError) as exc:
            logger.debug(f'Satır parse hatası: {exc}')
            continue

    return servers


def save_servers(parsed: list[dict], game_slug: str = 'metin2') -> tuple[int, int]:
    """
    Parse edilen sunucuları veritabanına kaydeder.
    Zaten varsa atlar.
    Returns: (toplam, yeni eklenen)
    """
    from apps.servers.models import Game, Server

    try:
        game = Game.objects.get(slug=game_slug)
    except Game.DoesNotExist:
        logger.error(f'Oyun bulunamadı: {game_slug}')
        return 0, 0

    # Scraper için sistem kullanıcısı — isteğe bağlı
    from django.contrib.auth import get_user_model
    User = get_user_model()
    bot_user, _ = User.objects.get_or_create(
        username='scraper-bot',
        defaults={'email': 'bot@serverhub.internal', 'is_active': False}
    )

    new_count = 0
    for item in parsed:
        slug = slugify(item['name'])
        if Server.objects.filter(slug=slug).exists():
            continue
        Server.objects.create(
            owner=bot_user,
            game=game,
            name=item['name'],
            exp_rate=item.get('exp_rate', 1),
            website=item.get('website', ''),
            status=Server.STATUS_PENDING,  # Admin onayı gerekli
        )
        new_count += 1

    return len(parsed), new_count


def run_scraper(url: str = 'https://example.com/metin2-servers') -> None:
    """Ana scraper fonksiyonu — cron ile çağrılabilir."""
    from .models import ScrapeLog

    logger.info(f'Scraper başladı: {url}')
    html = fetch_page(url)

    if not html:
        ScrapeLog.objects.create(source_url=url, status='error', error_msg='Sayfa getirilemedi.')
        return

    parsed = parse_metin2_servers(html)
    total, new_count = save_servers(parsed)

    ScrapeLog.objects.create(
        source_url=url,
        servers_found=total,
        servers_new=new_count,
        status='ok',
    )
    logger.info(f'Scraper tamamlandı: {total} bulundu, {new_count} yeni eklendi.')
