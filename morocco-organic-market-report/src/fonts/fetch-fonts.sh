#!/usr/bin/env bash
# Fetch the two OFL typefaces the report is set in.
#
#   Spectral                 — body serif        (SIL Open Font License 1.1)
#   IBM Plex Sans Condensed  — headings & tables (SIL Open Font License 1.1)
#   IBM Plex Mono            — code & URLs       (SIL Open Font License 1.1)
#
# The font binaries are not committed to this repository; this script pulls them
# from the upstream Google Fonts repository, which also carries each family's
# OFL.txt. Run it once before the first build.
set -euo pipefail
cd "$(dirname "$0")"
B=https://raw.githubusercontent.com/google/fonts/main

get () { curl -fsSL -o "$2" "$B/$1" && echo "  $2"; }

echo "fetching fonts into $(pwd)"
get ofl/spectral/Spectral-Regular.ttf                                 Spectral-Regular.ttf
get ofl/spectral/Spectral-Italic.ttf                                  Spectral-Italic.ttf
get ofl/spectral/Spectral-Medium.ttf                                  Spectral-Medium.ttf
get ofl/spectral/Spectral-SemiBold.ttf                                Spectral-SemiBold.ttf
get ofl/spectral/Spectral-Bold.ttf                                    Spectral-Bold.ttf
get ofl/ibmplexsanscondensed/IBMPlexSansCondensed-Regular.ttf         PlexCn-Regular.ttf
get ofl/ibmplexsanscondensed/IBMPlexSansCondensed-Italic.ttf          PlexCn-Italic.ttf
get ofl/ibmplexsanscondensed/IBMPlexSansCondensed-Medium.ttf          PlexCn-Medium.ttf
get ofl/ibmplexsanscondensed/IBMPlexSansCondensed-SemiBold.ttf        PlexCn-SemiBold.ttf
get ofl/ibmplexsanscondensed/IBMPlexSansCondensed-Bold.ttf            PlexCn-Bold.ttf
get ofl/ibmplexmono/IBMPlexMono-Regular.ttf                           PlexMono-Regular.ttf
get ofl/ibmplexmono/IBMPlexMono-SemiBold.ttf                          PlexMono-SemiBold.ttf
echo "done."
