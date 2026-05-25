# The Dark Room — djgedeon.com

Site statique pour les émissions, mixs et playlists de Dj Gedeon.
Construit avec [Astro](https://astro.build) + [Decap CMS](https://decapcms.org).

---

## Comment ça marche

- **Astro** génère un site statique ultra-rapide. Aucune base de données, aucun plugin à mettre à jour.
- **Decap CMS** fournit une interface d'admin à l'adresse `djgedeon.com/admin` pour publier mixs, playlists et annonces sans toucher au code.
- **Mixcloud** héberge les mixs eux-mêmes. Tu colles juste l'URL Mixcloud dans le formulaire de l'admin, le widget officiel apparaît automatiquement.
- **Netlify** héberge et déploie automatiquement le site dès qu'un contenu est modifié.

---

## Démarrage en local (pour tester avant déploiement)

Prérequis : [Node.js](https://nodejs.org) version 20 ou plus récent.

```bash
# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```

Le site est ensuite accessible sur http://localhost:4321

---

## Déploiement sur Netlify (pas-à-pas)

### 1. Créer un dépôt GitHub

1. Va sur [github.com](https://github.com) et crée un compte (ou connecte-toi).
2. Crée un nouveau dépôt nommé `djgedeon`.
3. Sur ton ordinateur, dans le dossier du projet :

```bash
git init
git add .
git commit -m "Premier commit"
git branch -M main
git remote add origin https://github.com/TON-USERNAME/djgedeon.git
git push -u origin main
```

### 2. Connecter Netlify

1. Va sur [netlify.com](https://www.netlify.com) et crée un compte (avec ton compte GitHub).
2. Clique sur **"Add new site" → "Import an existing project"**.
3. Choisis **GitHub** et sélectionne le dépôt `djgedeon`.
4. Netlify détecte automatiquement la config (grâce au fichier `netlify.toml`). Clique sur **"Deploy"**.
5. En 30 secondes, le site est en ligne sur une URL Netlify temporaire (ex: `random-name-123456.netlify.app`).

### 3. Brancher le domaine djgedeon.com

1. Dans Netlify : **Site settings → Domain management → Add a domain**.
2. Entre `djgedeon.com`.
3. Netlify te donne deux choix :
   - **Option A (plus simple)** : déléguer les DNS à Netlify en changeant les nameservers chez ton registrar.
   - **Option B** : ajouter des enregistrements DNS chez ton registrar actuel (Netlify te donne les valeurs exactes).
4. Le HTTPS est configuré automatiquement par Netlify avec Let's Encrypt.

### 4. Activer l'admin Decap CMS

Pour pouvoir publier depuis `djgedeon.com/admin` :

1. Dans Netlify : **Site settings → Identity → Enable Identity**.
2. **Identity → Registration → Invite only** (pour que personne d'autre ne puisse créer un compte).
3. **Identity → Services → Git Gateway → Enable Git Gateway**.
4. **Identity → Invite users** : invite ton adresse email (Ged).
5. Tu reçois un email avec un lien pour définir ton mot de passe.
6. Va sur `djgedeon.com/admin`, connecte-toi, et tu peux publier.

---

## Comment publier un nouveau mix

1. Upload ton mix sur Mixcloud (comme d'habitude).
2. Copie l'URL Mixcloud (ex: `https://www.mixcloud.com/djgedeon/session-048/`).
3. Va sur `djgedeon.com/admin`, connecte-toi.
4. Clique sur **"Mixs" → "New Mix"**.
5. Remplis le formulaire : numéro, titre, date, durée, genre, URL Mixcloud, tracklist, cover.
6. Clique sur **"Publish"**.
7. En 30 secondes, le mix apparaît sur le site (Netlify reconstruit automatiquement).

Même logique pour **Playlists** et **Annonces**.

---

## Structure du projet

```
djgedeon/
├── src/
│   ├── content/
│   │   ├── mixs/           ← un fichier .md par mix
│   │   ├── playlists/      ← un fichier .md par playlist
│   │   ├── annonces/       ← un fichier .md par annonce
│   │   └── config.ts       ← schéma des collections
│   ├── components/
│   │   ├── MixcloudPlayer.astro
│   │   └── MixCard.astro
│   ├── layouts/
│   │   └── BaseLayout.astro
│   ├── pages/              ← chaque .astro devient une URL
│   │   ├── index.astro     ← /
│   │   ├── mixs/
│   │   │   ├── index.astro      ← /mixs/
│   │   │   └── [slug].astro     ← /mixs/session-047/
│   │   ├── playlists/
│   │   └── annonces/
│   └── styles/
│       └── global.css
├── public/
│   ├── admin/              ← interface CMS (Decap)
│   │   ├── index.html
│   │   └── config.yml      ← configuration du CMS
│   └── images/
│       └── darkroom-logo.png
├── astro.config.mjs
├── netlify.toml
├── package.json
└── README.md
```

---

## Modifier le design

Tout le style est dans `src/styles/global.css`. Les couleurs principales sont en haut, dans `:root`.
Pour changer la police de titre, modifie `font-family: Impact, ...` dans la classe `.hero-title`.

---

## Coût

Tout est gratuit jusqu'à un trafic confortable :

- **Netlify** : 100 Go de bande passante/mois et 300 minutes de build/mois en gratuit.
- **GitHub** : illimité pour les dépôts publics et privés.
- **Mixcloud** : compte gratuit suffisant.
- Seule dépense : le nom de domaine `djgedeon.com` (~10 €/an).

---

## Besoin d'aide ?

Toute la doc Astro est ici : https://docs.astro.build
Toute la doc Decap CMS est ici : https://decapcms.org/docs
