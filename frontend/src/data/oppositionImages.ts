// Licensed Kohli imagery keyed by opposition. exactOppositionMatch=true
// only when the source caption ties the photo to that opposition.
// Otherwise a representative licensed image is used and labelled as such.
export interface OppositionImage {
  opposition: string;
  src: string;
  alt: string;
  creator: string;
  license: string;
  sourceUrl: string;
  exactOppositionMatch: boolean;
  caption: string;
}

export const FALLBACK_IMAGE: OppositionImage = {
  opposition: '*',
  src: '/images/virat-kohli-portrait.jpg',
  alt: 'Portrait of Virat Kohli (representative image)',
  creator: 'Anand Anil',
  license: 'CC BY-SA 4.0',
  sourceUrl: 'https://commons.wikimedia.org/wiki/File:Virat_Kohli_portrait.jpg',
  exactOppositionMatch: false,
  caption: 'Representative image',
};

const images: OppositionImage[] = [
  {
    opposition: 'South Africa',
    src: '/images/virat-kohli-batting-2013.jpg',
    alt: 'Virat Kohli batting against South Africa, 2013 Champions Trophy',
    creator: 'Dee03',
    license: 'CC BY-SA 4.0',
    sourceUrl: 'https://commons.wikimedia.org/wiki/File:Virat_Kohli_batting_2013.jpg',
    exactOppositionMatch: true,
    caption: 'vs South Africa · Champions Trophy 2013',
  },
  {
    opposition: 'West Indies',
    src: '/images/virat-kohli-greenfield-2018.jpg',
    alt: 'Virat Kohli at Greenfield Stadium during the West Indies series, 2018',
    creator: 'Jishith',
    license: 'CC BY-SA 4.0',
    sourceUrl:
      'https://commons.wikimedia.org/wiki/File:Virat_Kohli_at_Greenfield_Stadium_1.11.2018.jpg',
    exactOppositionMatch: true,
    caption: 'vs West Indies · Thiruvananthapuram 2018',
  },
  {
    opposition: 'New Zealand',
    src: '/images/virat-kohli-batting-2010.jpg',
    alt: 'Virat Kohli batting against New Zealand, December 2010',
    creator: 'lensbug.chandru',
    license: 'CC BY 2.0',
    sourceUrl: 'https://commons.wikimedia.org/wiki/File:Virat_Kohli_Batting.jpg',
    exactOppositionMatch: true,
    caption: 'vs New Zealand · December 2010',
  },
  {
    opposition: 'Australia',
    src: '/images/virat-kohli-aus-2023.jpg',
    alt: 'Virat Kohli with the Prime Ministers at the India vs Australia Test, Ahmedabad 2023',
    creator: "Prime Minister's Office (India)",
    license: 'GODL-India',
    sourceUrl:
      'https://commons.wikimedia.org/wiki/File:Virat_Kohli_during_the_India_vs_Aus_4th_Test_match_at_Narendra_Modi_Stadium_on_09_March_2023.jpg',
    exactOppositionMatch: true,
    caption: 'India vs Australia · Ahmedabad 2023 (ceremony)',
  },
];

export function imageFor(opposition: string): OppositionImage {
  return images.find((i) => i.opposition === opposition) ?? {
    ...FALLBACK_IMAGE,
    opposition,
  };
}
