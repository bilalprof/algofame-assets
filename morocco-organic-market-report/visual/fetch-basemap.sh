#!/usr/bin/env bash
# Fetch the basemap geometry used by makemap.py.
#
#   Natural Earth 1:50m admin-0 countries — public domain.
#   ~3 MB, so it is not committed to this repository.
set -euo pipefail
cd "$(dirname "$0")"
curl -fsSL -o ne50.geojson \
  https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson
echo "ne50.geojson: $(du -h ne50.geojson | cut -f1)"
