// Exact-match knock photographs. Every record ties a Kohli innings
// (sourceMatchId from our database) to a photograph captioned as coming
// from that precise match. matchAssociation tiers:
// exact_knock (batting/celebrating during that innings) > exact_match
// (same match) > same_opposition. Rights are stated independently:
// verified = open license established; copyrighted = commercial/agency
// or board photo reused here as a visual prototype with provenance.
export type MatchAssociation =
  | 'exact_knock'
  | 'exact_match'
  | 'same_opposition';
export type RightsStatus = 'verified' | 'copyrighted' | 'unknown' | 'unverified';

export interface KnockImage {
  matchId: string;
  sourceMatchId: string;
  opposition: string;
  matchDate: string;
  venue?: string;
  format: string;
  kohliRuns: number;
  imagePath: string;
  sourceUrl: string;
  sourceName: string;
  creator: string;
  license: string;
  licenseStatus: 'verified' | 'unverified';
  attribution: string;
  matchAssociation: MatchAssociation;
  exactMatch: boolean;
  sameOpposition: boolean;
  rightsVerified: boolean;
  rightsStatus: RightsStatus;
  caption: string;
}

const knocks: KnockImage[] = [
  {
    matchId: '535798',
    sourceMatchId: '535798',
    opposition: 'Pakistan',
    matchDate: '2012-03-18',
    venue: 'Shere Bangla National Stadium, Mirpur',
    format: 'ODI',
    kohliRuns: 183,
    imagePath: '/images/kohli-183-pakistan-2012.jpg',
    sourceUrl:
      'https://www.espncricinfo.com/series/asia-cup-2011-12-524504/india-vs-pakistan-5th-match-535798/match-photo',
    sourceName: 'ESPNcricinfo match gallery (AFP photo)',
    creator: 'AFP',
    license: 'copyrighted',
    licenseStatus: 'unverified',
    attribution: 'AFP, via ESPNcricinfo match gallery',
    matchAssociation: 'exact_knock',
    exactMatch: true,
    sameOpposition: true,
    rightsVerified: false,
    rightsStatus: 'copyrighted',
    caption: 'Kohli — 183 vs Pakistan, Asia Cup 2012',
  },
  {
    matchId: '1122281',
    sourceMatchId: '1122281',
    opposition: 'South Africa',
    matchDate: '2018-02-07',
    venue: 'Newlands, Cape Town',
    format: 'ODI',
    kohliRuns: 160,
    imagePath: '/images/kohli-160-sa-2018.jpg',
    sourceUrl:
      'https://www.rediff.com/cricket/report/photos-all-round-india-thrash-south-africa-by-124-runs-pix-kohli-chahal-yadav/20180208.htm',
    sourceName: 'Rediff (BCCI photograph)',
    creator: 'BCCI',
    license: 'copyrighted',
    licenseStatus: 'unverified',
    attribution: 'BCCI, via Rediff',
    matchAssociation: 'exact_knock',
    exactMatch: true,
    sameOpposition: true,
    rightsVerified: false,
    rightsStatus: 'copyrighted',
    caption: 'Kohli — 160* vs South Africa, Newlands 2018',
  },
  {
    matchId: '1348645',
    sourceMatchId: '1348645',
    opposition: 'Sri Lanka',
    matchDate: '2023-01-15',
    venue: 'Greenfield International Stadium, Thiruvananthapuram',
    format: 'ODI',
    kohliRuns: 166,
    imagePath: '/images/kohli-166-sl-2023.jpg',
    sourceUrl:
      'https://www.espncricinfo.com/series/sri-lanka-in-india-2022-23-1348629/india-vs-sri-lanka-3rd-odi-1348645/match-photo',
    sourceName: 'ESPNcricinfo match gallery (AP photo)',
    creator: 'Associated Press',
    license: 'copyrighted',
    licenseStatus: 'unverified',
    attribution: 'Associated Press, via ESPNcricinfo match gallery',
    matchAssociation: 'exact_knock',
    exactMatch: true,
    sameOpposition: true,
    rightsVerified: false,
    rightsStatus: 'copyrighted',
    caption: 'Kohli — 166* vs Sri Lanka, Thiruvananthapuram 2023',
  },
  {
    matchId: '1030223',
    sourceMatchId: '1030223',
    opposition: 'New Zealand',
    matchDate: '2016-10-23',
    venue: 'Punjab Cricket Association Stadium, Mohali',
    format: 'ODI',
    kohliRuns: 154,
    imagePath: '/images/kohli-154-nz-2016.jpg',
    sourceUrl:
      'https://www.rediff.com/cricket/report/kohli-masterclass-sinks-kiwis-to-take-2-1-lead-mohali-odi-pix/20161023.htm',
    sourceName: 'Rediff (BCCI photograph)',
    creator: 'BCCI',
    license: 'copyrighted',
    licenseStatus: 'unverified',
    attribution: 'BCCI, via Rediff',
    matchAssociation: 'exact_knock',
    exactMatch: true,
    sameOpposition: true,
    rightsVerified: false,
    rightsStatus: 'copyrighted',
    caption: 'Kohli — 154* vs New Zealand, Mohali 2016',
  },
  {
    matchId: '1157754',
    sourceMatchId: '1157754',
    opposition: 'West Indies',
    matchDate: '2018-10-21',
    venue: 'Barsapara Cricket Stadium, Guwahati',
    format: 'ODI',
    kohliRuns: 140,
    imagePath: '/images/kohli-140-wi-2018.jpg',
    sourceUrl:
      'https://www.espncricinfo.com/series/west-indies-in-india-2018-19-1157747/india-vs-west-indies-1st-odi-1157754/match-photo',
    sourceName: 'ESPNcricinfo match gallery (AP photo)',
    creator: 'Associated Press',
    license: 'copyrighted',
    licenseStatus: 'unverified',
    attribution: 'Associated Press, via ESPNcricinfo match gallery',
    matchAssociation: 'exact_knock',
    exactMatch: true,
    sameOpposition: true,
    rightsVerified: false,
    rightsStatus: 'copyrighted',
    caption: 'Kohli — 140 vs West Indies, Guwahati 2018',
  },
  {
    matchId: '710293',
    sourceMatchId: '710293',
    opposition: 'Bangladesh',
    matchDate: '2014-02-26',
    venue: 'Khan Shaheb Osman Ali Stadium, Fatullah',
    format: 'ODI',
    kohliRuns: 136,
    imagePath: '/images/kohli-136-ban-2014.jpg',
    sourceUrl:
      'https://www.espncricinfo.com/series/asia-cup-2013-14-671665/bangladesh-vs-india-2nd-match-710293/match-photo',
    sourceName: 'ESPNcricinfo match gallery (AFP photo)',
    creator: 'AFP',
    license: 'copyrighted',
    licenseStatus: 'unverified',
    attribution: 'AFP, via ESPNcricinfo match gallery',
    matchAssociation: 'exact_knock',
    exactMatch: true,
    sameOpposition: true,
    rightsVerified: false,
    rightsStatus: 'copyrighted',
    caption: 'Kohli — 136 vs Bangladesh, Fatullah 2014',
  },
  {
    matchId: '1298150',
    sourceMatchId: '1298150',
    opposition: 'Pakistan',
    matchDate: '2022-10-23',
    venue: 'Melbourne Cricket Ground',
    format: 'T20I',
    kohliRuns: 82,
    imagePath: '/images/kohli-82-pakistan-2022.jpg',
    sourceUrl:
      'https://www.espncricinfo.com/series/icc-men-s-t20-world-cup-2022-23-1298134/india-vs-pakistan-16th-match-group-2-1298150/match-photo',
    sourceName: 'ESPNcricinfo match gallery (Getty Images photo)',
    creator: 'Getty Images',
    license: 'copyrighted',
    licenseStatus: 'unverified',
    attribution: 'Getty Images, via ESPNcricinfo match gallery',
    matchAssociation: 'exact_knock',
    exactMatch: true,
    sameOpposition: true,
    rightsVerified: false,
    rightsStatus: 'copyrighted',
    caption: 'Kohli — 82* vs Pakistan, MCG 2022',
  },
  {
    matchId: '1327279',
    sourceMatchId: '1327279',
    opposition: 'Afghanistan',
    matchDate: '2022-09-08',
    venue: 'Dubai International Cricket Stadium',
    format: 'T20I',
    kohliRuns: 122,
    imagePath: '/images/kohli-122-afg-2022.jpg',
    sourceUrl:
      'https://www.espncricinfo.com/series/men-s-t20-asia-cup-2022-1327237/afghanistan-vs-india-11th-match-super-four-1327279/match-photo',
    sourceName: 'ESPNcricinfo match gallery (Getty Images photo)',
    creator: 'Getty Images',
    license: 'copyrighted',
    licenseStatus: 'unverified',
    attribution: 'Getty Images, via ESPNcricinfo match gallery',
    matchAssociation: 'exact_knock',
    exactMatch: true,
    sameOpposition: true,
    rightsVerified: false,
    rightsStatus: 'copyrighted',
    caption: 'Kohli — 122* vs Afghanistan, Dubai 2022',
  },
  {
    matchId: '1157755',
    sourceMatchId: '1157755',
    opposition: 'West Indies',
    matchDate: '2018-10-24',
    venue: 'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam',
    format: 'ODI',
    kohliRuns: 157,
    imagePath: '/images/kohli-157-wi-2018.jpg',
    sourceUrl:
      'https://www.espncricinfo.com/series/west-indies-in-india-2018-19-1157747/india-vs-west-indies-2nd-odi-1157755/match-photo',
    sourceName: 'ESPNcricinfo match gallery (AP photo)',
    creator: 'Associated Press',
    license: 'copyrighted',
    licenseStatus: 'unverified',
    attribution: 'Associated Press, via ESPNcricinfo match gallery',
    matchAssociation: 'exact_knock',
    exactMatch: true,
    sameOpposition: true,
    rightsVerified: false,
    rightsStatus: 'copyrighted',
    caption: 'Kohli — 157* vs West Indies, Visakhapatnam 2018',
  },
  {
    matchId: '1187018',
    sourceMatchId: '1187018',
    opposition: 'West Indies',
    matchDate: '2019-12-06',
    venue: 'Rajiv Gandhi International Stadium, Hyderabad',
    format: 'T20I',
    kohliRuns: 94,
    imagePath: '/images/kohli-94-wi-2019.jpg',
    sourceUrl:
      'https://www.espncricinfo.com/series/west-indies-in-india-2019-20-1186986/india-vs-west-indies-1st-t20i-1187018/match-photo',
    sourceName: 'ESPNcricinfo match gallery (BCCI photo)',
    creator: 'BCCI',
    license: 'copyrighted',
    licenseStatus: 'unverified',
    attribution: 'BCCI, via ESPNcricinfo match gallery',
    matchAssociation: 'exact_knock',
    exactMatch: true,
    sameOpposition: true,
    rightsVerified: false,
    rightsStatus: 'copyrighted',
    caption: 'Kohli — 94* vs West Indies, Hyderabad 2019',
  },
  {
    matchId: '980999',
    sourceMatchId: '980999',
    opposition: 'Punjab Kings',
    matchDate: '2016-05-18',
    venue: 'M Chinnaswamy Stadium, Bengaluru',
    format: 'IPL',
    kohliRuns: 113,
    imagePath: '/images/kohli-113-pbks-2016.jpg',
    sourceUrl:
      'https://www.rediff.com/cricket/report/ipl-photos-chinnaswamy-match-report-virat-kohlis-fourth-ton-helps-royal-challengers-bangalore-move-up-to-second-punjab/20160519.htm',
    sourceName: 'Rediff (BCCI photograph)',
    creator: 'BCCI',
    license: 'copyrighted',
    licenseStatus: 'unverified',
    attribution: 'BCCI, via Rediff',
    matchAssociation: 'exact_knock',
    exactMatch: true,
    sameOpposition: true,
    rightsVerified: false,
    rightsStatus: 'copyrighted',
    caption: 'Kohli — 113 vs Punjab Kings, Bengaluru 2016',
  },
  {
    matchId: '1422137',
    sourceMatchId: '1422137',
    opposition: 'Rajasthan Royals',
    matchDate: '2024-04-06',
    venue: 'Sawai Mansingh Stadium, Jaipur',
    format: 'IPL',
    kohliRuns: 113,
    imagePath: '/images/kohli-113-rr-2024.jpg',
    sourceUrl:
      'https://www.rediff.com/cricket/report/ipl-pix-rr-vs-rcb-virat-kohlis-masterclass-takes-bengaluru-to-1833-faf-samson-buttler-chahal/20240406.htm',
    sourceName: 'Rediff (BCCI photograph)',
    creator: 'BCCI',
    license: 'copyrighted',
    licenseStatus: 'unverified',
    attribution: 'BCCI, via Rediff',
    matchAssociation: 'exact_knock',
    exactMatch: true,
    sameOpposition: true,
    rightsVerified: false,
    rightsStatus: 'copyrighted',
    caption: 'Kohli — 113* vs Rajasthan Royals, Jaipur 2024',
  },
  {
    matchId: '980987',
    sourceMatchId: '980987',
    opposition: 'Gujarat Lions',
    matchDate: '2016-05-14',
    venue: 'M Chinnaswamy Stadium, Bengaluru',
    format: 'IPL',
    kohliRuns: 109,
    imagePath: '/images/kohli-109-gl-2016.jpg',
    sourceUrl:
      'https://www.espncricinfo.com/series/ipl-2016-968923/royal-challengers-bangalore-vs-gujarat-lions-44th-match-980987/match-photo',
    sourceName: 'ESPNcricinfo match gallery (AFP photo)',
    creator: 'AFP',
    license: 'copyrighted',
    licenseStatus: 'unverified',
    attribution: 'AFP, via ESPNcricinfo match gallery',
    matchAssociation: 'exact_knock',
    exactMatch: true,
    sameOpposition: true,
    rightsVerified: false,
    rightsStatus: 'copyrighted',
    caption: 'Kohli — 109 vs Gujarat Lions, Bengaluru 2016',
  },
];

// Opposition card image: exact-knock photo preferred (most iconic first),
// else the licensed same-opposition record from oppositionImages.
const oppositionPreference: Record<string, string> = {
  Pakistan: '535798',
  'South Africa': '1122281',
  'Sri Lanka': '1348645',
  'New Zealand': '1030223',
  'West Indies': '1157754',
  Bangladesh: '710293',
  Afghanistan: '1327279',
  'Punjab Kings': '980999',
  'Rajasthan Royals': '1422137',
  'Gujarat Lions': '980987',
};

export function knockImageFor(sourceMatchId: string): KnockImage | null {
  return knocks.find((k) => k.sourceMatchId === sourceMatchId) ?? null;
}

export function preferredKnockFor(opposition: string): KnockImage | null {
  const id = oppositionPreference[opposition];
  if (!id) return null;
  return knockImageFor(id);
}

export function allKnockImages(): KnockImage[] {
  return knocks;
}
