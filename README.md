
# Free Fire Prime Level Checker — Vercel

## What it does
- Player UID input
- Server selection
- Multi-region support
- Returns nickname, UID, actual region and Prime Level
- API key stays server-side in Vercel Environment Variables

## Regions
BD, IND, PK, SG, ID, TH, VN, TW, BR, SAC, US, NA, ME, RU, CIS, EUROPE

## API
GET /api/prime?uid=PLAYER_UID&region=BD

## Vercel setup
1. Upload/import this project into Vercel.
2. Open Project Settings → Environment Variables.
3. Add:
   FREEFIRE_API_KEY = YOUR_UPSTREAM_API_KEY
4. Optional:
   FREEFIRE_API_URL = http://siambhau69.eu.cc/freefireinfo/bhau
5. Redeploy.

The upstream API documentation currently describes `basicInfo.primeInfo.primeLevel`
and lists multiple Free Fire server regions. The upstream may require its own API key
and may have rate limits/terms. Do not put the upstream API key in frontend code.

## Important
This project does not bypass Cloudflare or scrape-protected pages. It uses a
documented/authorized upstream API endpoint. If that upstream changes or does not
return `primeInfo`, the tool will report that Prime Level was not returned.
