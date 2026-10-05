# Андрей Царёв — персональный сайт

Статический сайт: главная страница, фармацевтическое направление и MedTech. Исходники лежат в `site/` и не требуют npm или сервера. Контент адаптирован из `tsarev2709/anix_landing` (страницы Андрея Царёва и Anix Medicine, состояние `fabf15399e200bfea8773b970f39e8d8f217e69e`).

## Локальная проверка

```bash
python3 scripts/check_site.py
bash scripts/prepare-assets.sh
python3 scripts/check_site.py --assets
python3 -m http.server 8000 -d site
```

При открытии локальной копии: `http://localhost:8000/`. Скрипт изображений скачивает шесть фотографий и иллюстраций из закреплённой версии Anix; в опубликованной сборке они лежат внутри сайта. Локальные копии `.webp` не коммитятся.

## Деплой

Каждый push в `main` запускает `.github/workflows/deploy.yml`: копирует изображения, проверяет страницы и публикует `site/` в ветку `gh-pages`. В GitHub для **этого репозитория** нужно один раз выбрать `Settings → Pages → Build and deployment → Deploy from a branch → gh-pages / (root) → Save`. После этого адрес: `https://tsarev2709.github.io/iptsarev/`. Если Pages уже настроен на эту ветку, дополнительных действий не нужно. Отдельный домен пока не задан.

При будущем подключении домена нужно обновить canonical/OG URL в HTML, `robots.txt`, `sitemap.xml`, добавить `CNAME` в `site/` и настроить DNS/Pages. В источнике Anix эти условия и цены могут со временем меняться, поэтому перед коммерческим использованием проверяйте блок Pharma Launch System.

Контактные CTA ведут в личный Telegram `https://t.me/tsarev2709`; внешние кейсы остаются на сайте Anix. На сайте нет форм, трекеров, API-ключей и обработки пользовательского ввода.
