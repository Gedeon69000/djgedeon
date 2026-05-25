import { getEntry } from 'astro:content';

export async function getSiteSettings() {
  const entry = await getEntry('settings', 'site');
  if (!entry) {
    throw new Error('Fichier de paramètres site.md introuvable dans src/content/settings/');
  }
  return entry.data;
}
