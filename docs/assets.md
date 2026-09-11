# KohliIQ — Asset Register (relevance-first, honesty-preserving)

Opposition cards follow: exact knock → same-opposition photo →
relevant action photo (honestly captioned) → ball-graphic fallback.
Sourcing is broad (Commons, boards, media, search), but every record
carries `licenseStatus`/`rightsVerified` — unverified rights are labelled,
never invented. No generic portrait is ever shown as an opposition image.

| Opposition | Image | Match association | Exact match | Same opposition | Source | Rights status |
| ---------- | ----- | ----------------- | ----------- | --------------- | ------ | ------------- |
| South Africa | virat-kohli-batting-2013.jpg | India vs South Africa, Champions Trophy 2013 | No | Yes | Wikimedia Commons (Dee03) | verified (CC BY-SA 4.0) |
| West Indies | virat-kohli-greenfield-2018.jpg | India vs West Indies, Thiruvananthapuram 2018 | No | Yes | Wikimedia Commons (Jishith) | verified (CC BY-SA 4.0) |
| New Zealand | virat-kohli-batting-2010.jpg | India v New Zealand, Dec 2010 | No | Yes | Wikimedia Commons (lensbug.chandru) | verified (CC BY 2.0) |
| Australia | virat-kohli-aus-2023.jpg | India vs Australia, Ahmedabad 2023 (ceremony) | No | Yes | Wikimedia Commons, PMO India | verified (GODL-India) |
| England | virat-kohli-england-2018.jpg | India vs England, Trent Bridge 2018 | No | Yes | Wikimedia Commons (It's No Game) | verified (CC BY 2.0) |
| Pakistan | none (fallback) | researched: only Getty/AFP/AP commercial photos with clear captions (e.g. MCG 2022) — technically hotlink-protected, legally commercial; not vendored | n/a | n/a | n/a | n/a |
| Sri Lanka | none (fallback) | researched: only Getty/Reuters-via-Rediff commercial photos (e.g. Hobart 2012, Colombo 2017) — not vendored | n/a | n/a | n/a | n/a |
| Bangladesh | none (fallback) | researched: no clearly-captioned reusable action photo found | n/a | n/a | n/a | n/a |
| Afghanistan / Zimbabwe / Ireland / associates / IPL | none (fallback) | no reusable captioned source found | n/a | n/a | n/a | n/a |

No Level-1 exact-knock photo is verified for any displayed knock, so no
exact-match claims are made. No Level-3 generic action image is currently
populated — no suitable opposition-neutral licensed action shot was found,
and commercial-agency photos were deliberately not vendored. The registry
schema (`licenseStatus`, `sameOpposition`, `rightsVerified`) already
supports unverified/action-tier images when a suitable one appears.

| Asset | Source | Author | License | URL | Attribution Required |
| ----- | ------ | ------ | ------- | --- | -------------------- |

| Asset | Source | Author | License | URL | Attribution Required |
| ----- | ------ | ------ | ------- | --- | -------------------- |
| ~~`frontend/public/images/virat-kohli-portrait.jpg`~~ (removed: hero replaced by action shot) | Wikimedia Commons | Anand Anil | CC BY-SA 4.0 | https://commons.wikimedia.org/wiki/File:Virat_Kohli_portrait.jpg | Was credited in hero/footer through Phase 8 |
| `frontend/public/images/kohli-hero-waca-2015.jpg` (hero, 1600px) | Wikimedia Commons | Bahnfrend | CC BY-SA 4.0 | https://commons.wikimedia.org/wiki/File:2015_CWC_I_v_UAE_02-28_Kohli_(01).JPG | Yes — Kohli batting at the WACA, World Cup 2015; credited in hero caption and footer |
| `frontend/public/images/kohli-113-pbks-2016.jpg` (knock, Tier 1) | Rediff, BCCI photo | BCCI | copyrighted | https://www.rediff.com/cricket/report/ipl-photos-chinnaswamy-match-report-virat-kohlis-fourth-ton-helps-royal-challengers-bangalore-move-up-to-second-punjab/20160519.htm | Yes — 113 vs Punjab Kings, Bengaluru, 18 May 2016 |
| `frontend/public/images/kohli-113-rr-2024.jpg` (knock, Tier 1) | Rediff, BCCI photo | BCCI | copyrighted | https://www.rediff.com/cricket/report/ipl-pix-rr-vs-rcb-virat-kohlis-masterclass-takes-bengaluru-to-1833-faf-samson-buttler-chahal/20240406.htm | Yes — 113* vs Rajasthan Royals, Jaipur, 6 Apr 2024 |
| `frontend/public/images/kohli-109-gl-2016.jpg` (knock, Tier 1) | ESPNcricinfo gallery, AFP photo | AFP | copyrighted | https://www.espncricinfo.com/series/ipl-2016-968923/royal-challengers-bangalore-vs-gujarat-lions-44th-match-980987/match-photo | Yes — 109 vs Gujarat Lions, Bengaluru, 14 May 2016 |
| `frontend/public/images/kohli-108-rps-2016.jpg` (knock, Tier 1) | Rediff, PTI photo | PTI | copyrighted | https://www.rediff.com/cricket/report/ipl-photos-chinnaswamy-match-report-virat-kohlis-ton-helps-royal-challengers-bangalore-ease-past-pune/20160507.htm | Yes — 108* vs Rising Pune Supergiant, Bengaluru, 7 May 2016 |
| `frontend/public/images/kohli-157-wi-2018.jpg` (knock, Tier 1) | ESPNcricinfo gallery, AP photo | Associated Press | copyrighted | https://www.espncricinfo.com/series/west-indies-in-india-2018-19-1157747/india-vs-west-indies-2nd-odi-1157755/match-photo | Yes — 157* vs West Indies, Visakhapatnam, 24 Oct 2018 ("whips one through mid-wicket") |
| `frontend/public/images/kohli-94-wi-2019.jpg` (knock, Tier 1) | ESPNcricinfo gallery, BCCI photo | BCCI | copyrighted | https://www.espncricinfo.com/series/west-indies-in-india-2019-20-1186986/india-vs-west-indies-1st-t20i-1187018/match-photo | Yes — 94* vs West Indies, Hyderabad, 6 Dec 2019 ("lofts the ball over cover") |
| `frontend/public/images/virat-kohli-batting-2013.jpg` (analysis banner, 1280px) | Wikimedia Commons | Dee03 | CC BY-SA 4.0 | https://commons.wikimedia.org/wiki/File:Virat_Kohli_batting_2013.jpg | Yes — credited in figure caption |
| `frontend/public/images/virat-kohli-greenfield-2018.jpg` (opposition card, 800px) | Wikimedia Commons | Jishith | CC BY-SA 4.0 | https://commons.wikimedia.org/wiki/File:Virat_Kohli_at_Greenfield_Stadium_1.11.2018.jpg | Yes — exact West Indies fixture, captioned on card |
| `frontend/public/images/virat-kohli-batting-2010.jpg` (opposition card, 800px) | Wikimedia Commons | lensbug.chandru | CC BY 2.0 | https://commons.wikimedia.org/wiki/File:Virat_Kohli_Batting.jpg | Yes — exact New Zealand fixture (Dec 2010), captioned on card |
| `frontend/public/images/virat-kohli-aus-2023.jpg` (opposition card, 800px) | Wikimedia Commons (PMO India) | Prime Minister's Office (India) | GODL-India | https://commons.wikimedia.org/wiki/File:Virat_Kohli_during_the_India_vs_Aus_4th_Test_match_at_Narendra_Modi_Stadium_on_09_March_2023.jpg | Yes — exact Australia fixture (ceremony photo), captioned on card |
| `frontend/public/images/virat-kohli-england-2018.jpg` (opposition card, 800px) | Wikimedia Commons | It's No Game (Duncan Hull) | CC BY 2.0 | https://commons.wikimedia.org/wiki/File:Captain_Kohli_(51821389332).jpg | Yes — exact England fixture (Trent Bridge 2018, Buttler/Stokes visible), captioned on card |

## Verification table (opposition cards)

| Opposition | Image | Exact match? | Same opposition? | License verified? |
| ---------- | ----- | -----------: | ---------------: | ----------------: |
| Pakistan | none (ball-graphic fallback) | n/a | n/a | n/a — no reusable source found (Commons: 0 hits) |
| Australia | virat-kohli-aus-2023.jpg | No | Yes (Ahmedabad 2023 fixture) | Yes (GODL-India) |
| England | virat-kohli-england-2018.jpg | No | Yes (Trent Bridge 2018) | Yes (CC BY 2.0) |
| South Africa | virat-kohli-batting-2013.jpg | No | Yes (Champions Trophy 2013) | Yes (CC BY-SA 4.0) |
| New Zealand | virat-kohli-batting-2010.jpg | No | Yes (Dec 2010 fixture) | Yes (CC BY 2.0) |
| Sri Lanka | none (ball-graphic fallback) | n/a | n/a | n/a — no reusable source found (Commons: 0 hits) |
| Bangladesh | none (ball-graphic fallback) | n/a | n/a | n/a — only fan photos found |
| West Indies | virat-kohli-greenfield-2018.jpg | No | Yes (Thiruvananthapuram 2018) | Yes (CC BY-SA 4.0) |
| Afghanistan | none (ball-graphic fallback) | n/a | n/a | n/a — no reusable source found |
| Zimbabwe | none (ball-graphic fallback) | n/a | n/a | n/a — no reusable source found |
| Ireland | none (ball-graphic fallback) | n/a | n/a | n/a — no reusable source found |
| IPL franchises + associates | none (ball-graphic fallback) | n/a | n/a | n/a — out of scope for fixture photos |

## Exact-knock registry (Tier 1, all match-verified, rights stated separately)

| Opposition | Image | Match association | Exact match | Same opposition | Source | Rights status |
| ---------- | ----- | ----------------- | ----------- | --------------- | ------ | ------------- |
| Pakistan | kohli-183-pakistan-2012.jpg | 183, Asia Cup, Mirpur, 18 Mar 2012 (match 535798) | Yes (exact knock) | Yes | ESPNcricinfo gallery, AFP photo | copyrighted |
| Pakistan | kohli-82-pakistan-2022.jpg | 82*, T20 World Cup, MCG, 23 Oct 2022 (match 1298150) | Yes (exact knock) | Yes | ESPNcricinfo gallery, Getty photo | copyrighted |
| South Africa | kohli-160-sa-2018.jpg | 160*, Newlands, 7 Feb 2018 (match 1122281) | Yes (exact knock) | Yes | Rediff, BCCI photo | copyrighted |
| Sri Lanka | kohli-166-sl-2023.jpg | 166*, Thiruvananthapuram, 15 Jan 2023 (match 1348645) | Yes (exact knock) | Yes | ESPNcricinfo gallery, AP photo | copyrighted |
| New Zealand | kohli-154-nz-2016.jpg | 154*, Mohali, 23 Oct 2016 (match 1030223) | Yes (exact knock) | Yes | Rediff, BCCI photo | copyrighted |
| West Indies | kohli-140-wi-2018.jpg | 140, Guwahati, 21 Oct 2018 (match 1157754) | Yes (exact knock) | Yes | ESPNcricinfo gallery, AP photo | copyrighted |
| Bangladesh | kohli-136-ban-2014.jpg | 136, Fatullah, 26 Feb 2014 (match 710293) | Yes (exact knock) | Yes | ESPNcricinfo gallery, AFP photo | copyrighted |
| Afghanistan | kohli-122-afg-2022.jpg | 122*, Dubai, 8 Sep 2022 (match 1327279) | Yes (exact knock) | Yes | ESPNcricinfo gallery, Getty photo | copyrighted |

Opposition cards prefer the iconic exact knock (Pakistan→183, SA→160*,
SL→166*, NZ→154*, WI→140*, Ban→136*, Afg→122*); England and Australia
keep their verified same-opposition photos. Knocks without an exact photo
(Zimbabwe, Ireland, IPL franchises, remaining innings) show "Exact match
image unavailable" — never a mismatched photograph. Mismatched images: 0.

Notes:

- Original: `Virat Kohli portrait.jpg` (1899×2012); project copy is a
  1280px thumbnail served locally (no hotlinking).
- All other visuals are hand-built CSS/SVG (ball, seam, pitch lines, glows).
- No Pinterest or unclear-rights images are used anywhere.
