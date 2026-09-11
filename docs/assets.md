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
| `frontend/public/images/virat-kohli-portrait.jpg` (hero, 1280px) | Wikimedia Commons | Anand Anil | CC BY-SA 4.0 | https://commons.wikimedia.org/wiki/File:Virat_Kohli_portrait.jpg | Yes — credited in hero caption and footer |
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

No exact-knock (Level 1) photograph is verified for any displayed knock;
per-knock "exact match" claims are therefore never made. Pakistan 183 has
no verified photo — the card correctly shows the fallback.

Notes:

- Original: `Virat Kohli portrait.jpg` (1899×2012); project copy is a
  1280px thumbnail served locally (no hotlinking).
- All other visuals are hand-built CSS/SVG (ball, seam, pitch lines, glows).
- No Pinterest or unclear-rights images are used anywhere.
