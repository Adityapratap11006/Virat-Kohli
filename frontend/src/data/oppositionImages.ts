// Strict opposition-matched Kohli imagery. A record exists ONLY with
// source metadata tying the photo to that opposition (Level 2).
// exactMatch=true is reserved for a photo from the exact displayed knock
// (Level 1; none verified yet). Anything else renders the Level-3
// editorial fallback (ball graphic, "Image unavailable") — never a
// generic Kohli photograph.
export type ImageLevel = 'exact' | 'opposition';

export interface OppositionImage {
  opposition: string;
  imagePath: string;
  sourceUrl: string;
  sourceName: string;
  creator: string;
  license: string;
  attribution: string;
  matchAssociation: string;
  matchDate: string;
  matchDescription: string;
  exactMatch: boolean;
  level: ImageLevel;
}

const images: OppositionImage[] = [
  {
    opposition: 'South Africa',
    imagePath: '/images/virat-kohli-batting-2013.jpg',
    sourceUrl: 'https://commons.wikimedia.org/wiki/File:Virat_Kohli_batting_2013.jpg',
    sourceName: 'Wikimedia Commons',
    creator: 'Dee03',
    license: 'CC BY-SA 4.0',
    attribution: 'Dee03, CC BY-SA 4.0, via Wikimedia Commons',
    matchAssociation: 'India vs South Africa, ICC Champions Trophy 2013',
    matchDate: '2013-06-06',
    matchDescription: 'Kohli batting vs South Africa',
    exactMatch: false,
    level: 'opposition',
  },
  {
    opposition: 'West Indies',
    imagePath: '/images/virat-kohli-greenfield-2018.jpg',
    sourceUrl:
      'https://commons.wikimedia.org/wiki/File:Virat_Kohli_at_Greenfield_Stadium_1.11.2018.jpg',
    sourceName: 'Wikimedia Commons',
    creator: 'Jishith',
    license: 'CC BY-SA 4.0',
    attribution: 'Jishith, CC BY-SA 4.0, via Wikimedia Commons',
    matchAssociation: 'India vs West Indies, Greenfield Stadium, 1 Nov 2018',
    matchDate: '2018-11-01',
    matchDescription: 'Kohli at the crease vs West Indies',
    exactMatch: false,
    level: 'opposition',
  },
  {
    opposition: 'New Zealand',
    imagePath: '/images/virat-kohli-batting-2010.jpg',
    sourceUrl: 'https://commons.wikimedia.org/wiki/File:Virat_Kohli_Batting.jpg',
    sourceName: 'Wikimedia Commons',
    creator: 'lensbug.chandru',
    license: 'CC BY 2.0',
    attribution: 'lensbug.chandru, CC BY 2.0, via Wikimedia Commons',
    matchAssociation: 'India v New Zealand, 10 December 2010',
    matchDate: '2010-12-10',
    matchDescription: 'Kohli batting vs New Zealand',
    exactMatch: false,
    level: 'opposition',
  },
  {
    opposition: 'Australia',
    imagePath: '/images/virat-kohli-aus-2023.jpg',
    sourceUrl:
      'https://commons.wikimedia.org/wiki/File:Virat_Kohli_during_the_India_vs_Aus_4th_Test_match_at_Narendra_Modi_Stadium_on_09_March_2023.jpg',
    sourceName: 'Wikimedia Commons (PMO India)',
    creator: "Prime Minister's Office (India)",
    license: 'GODL-India',
    attribution: "Prime Minister's Office (GODL-India), via Wikimedia Commons",
    matchAssociation: 'India vs Australia, 4th Test, Ahmedabad, 9 Mar 2023',
    matchDate: '2023-03-09',
    matchDescription: 'Kohli with the Prime Ministers at the fixture (ceremony photo)',
    exactMatch: false,
    level: 'opposition',
  },
  {
    opposition: 'England',
    imagePath: '/images/virat-kohli-england-2018.jpg',
    sourceUrl: 'https://commons.wikimedia.org/wiki/File:Captain_Kohli_(51821389332).jpg',
    sourceName: 'Wikimedia Commons',
    creator: "It's No Game (Duncan Hull)",
    license: 'CC BY 2.0',
    attribution: "It's No Game, CC BY 2.0, via Wikimedia Commons",
    matchAssociation: 'India vs England, 3rd Test, Trent Bridge, Aug 2018',
    matchDate: '2018-08-18',
    matchDescription: 'Kohli batting vs England (Buttler keeping, Stokes at slip)',
    exactMatch: false,
    level: 'opposition',
  },
];

export function imageFor(opposition: string): OppositionImage | null {
  return images.find((i) => i.opposition === opposition) ?? null;
}
