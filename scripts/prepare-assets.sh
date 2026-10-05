#!/usr/bin/env bash
set -euo pipefail

# Pin the Anix source revision so future updates there cannot silently change this site.
source_revision="fabf15399e200bfea8773b970f39e8d8f217e69e"
base="https://raw.githubusercontent.com/tsarev2709/anix_landing/${source_revision}/src/images"
assets="$(cd "$(dirname "$0")/../site/assets" && pwd)"

fetch_image() {
  local source_path="$1" destination="$2"
  curl --fail --location --silent --show-error --retry 3 --connect-timeout 15 --max-time 120 \
    "${base}/${source_path}" --output "${assets}/${destination}"
  test -s "${assets}/${destination}"
  printf 'Fetched %s\n' "$destination"
}

fetch_image 'andrey/profile/andrey-profile-portrait.webp' 'portrait.webp'
fetch_image 'andrey/profile/andrey-profile-tochka-theatre.webp' 'theatre.webp'
fetch_image 'andrey/profile/andrey-profile-business-school-speaking.webp' 'speaking.webp'
fetch_image 'experts/andrey-tsarev-scientist.webp' 'scientist.webp'
fetch_image 'cases/hemotech-ai.webp' 'hemotech.webp'
fetch_image 'cases/mosfarma.webp' 'mosfarma.webp'
