import { defineCollection, z } from 'astro:content';

const mixs = defineCollection({
  type: 'content',
  schema: z.object({
    titre: z.string(),
    numero: z.number(),
    date: z.date(),
    duree: z.string(),
    genre: z.string(),
    hearthisId: z.union([z.string(), z.number()]),
    cover: z.string().optional(),
    tracklist: z.array(z.object({
      artiste: z.string(),
      titre: z.string()
    })).optional(),
    description: z.string().optional()
  })
});

const playlists = defineCollection({
  type: 'content',
  schema: z.object({
    titre: z.string(),
    date: z.date(),
    tracks: z.array(z.object({
      artiste: z.string(),
      titre: z.string()
    }))
  })
});

const annonces = defineCollection({
  type: 'content',
  schema: z.object({
    titre: z.string(),
    date: z.date(),
    dateEvenement: z.string().optional(),
    resume: z.string()
  })
});

const settings = defineCollection({
  type: 'content',
  schema: z.object({
    nomSite: z.string(),
    titreOnglet: z.string(),
    descriptionSeo: z.string(),
    logo: z.string(),
    favicon: z.string(),
    imagePartage: z.string(),
    couleurAccent: z.string(),
    couleurFond: z.string(),
    couleurTexte: z.string(),
    policeTitres: z.string(),
    policeCorps: z.string(),
    labelArchives: z.string(),
    labelPlaylists: z.string(),
    labelAnnonces: z.string(),
    labelDerniereEmission: z.string(),
    labelAccueil: z.string(),
    labelMixs: z.string(),
    labelMenuPlaylists: z.string(),
    labelLive: z.string(),
    labelApropos: z.string(),
    texteFooter: z.string(),
    emailContact: z.string(),
    lienHearthis: z.string().optional().default(''),
    lienSoundcloud: z.string().optional().default(''),
    lienMixcloud: z.string().optional().default(''),
    lienInstagram: z.string().optional().default(''),
    lienFacebook: z.string().optional().default(''),
    lienYoutube: z.string().optional().default(''),
    afficherRss: z.boolean().optional().default(true)
  })
});

const pages = defineCollection({
  type: 'content',
  schema: z.object({
    titre: z.string(),
    sousTitre: z.string().optional()
  })
});

export const collections = { mixs, playlists, annonces, settings, pages };
