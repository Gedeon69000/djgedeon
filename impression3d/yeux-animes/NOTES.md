# Yeux animés — 2 × Waveshare ESP32-S3-LCD-1.85 (sans soudure)

Statut : programme à écrire et compiler **sur le Mac**, avec les écrans branchés.

## Matériel
- 2 × Waveshare ESP32-S3-LCD-1.85 (non tactile), un par œil.
- ESP32-S3R8 : 8 Mo de PSRAM octale et 16 Mo de flash.
- Écran rond 1,85" de 360 × 360, contrôleur ST77916 en QSPI.

## Brochage (vérifié dans 2 sources concordantes : le wiki Waveshare, via deux dépôts tiers)
| Signal | GPIO |
|---|---|
| LCD D0 / D1 / D2 / D3 | 46 / 45 / 42 / 41 |
| LCD SCK | 40 |
| LCD CS | 21 |
| LCD TE | 18 |
| Rétroéclairage | 5 (PWM) |
| Reset LCD | **EXIO2 de l'expandeur TCA9554** (I2C 0x20), pas un GPIO |
| I2C (TCA9554, IMU QMI8658 0x6B, RTC PCF85063 0x51) | SDA 11 / SCL 10 |
| Micro ICS-43434 (I2S) | WS 2 / SCK 15 / SD 39 |
| Haut-parleur PCM5101 (I2S) | BCK 48 / LRCK 38 / DIN 47, ampli sur EXIO1 |

Sans initialiser le TCA9554 (EXIO2 à l'état haut), l'écran reste en reset et donc noir.

## Initialisation de l'écran : 2 révisions de dalle
La démo Waveshare lit le registre 0x04 en QSPI à 5 MHz :
- `00 7F 7F 7F` : séquence par défaut du composant Espressif `esp_lcd_st77916`.
- `00 02 7F 7F` : séquence Waveshare `vendor_specific_init_new` (184 commandes, qui se termine par 0x21 INVON, 0x11 avec 120 ms, puis 0x29).

Bus : SPI2, mode 0, QSPI, 80 MHz, commandes sur 32 bits, paramètres sur 8 bits.
Référence lisible : `ashchan/hornet-esp32-gauges`, dossier `lib/waveshare185/` (copie de la démo Waveshare).

## Plan du programme
- Rendu procédural des yeux par bandes (environ 40 lignes en RAM interne), envoyé avec `esp_lcd_panel_draw_bitmap`.
- Synchronisation par ESP-NOW, avec le même programme sur les 2 cartes. Celle qui a la plus petite adresse MAC devient le « meneur » et diffuse le regard, le clignement et la taille de pupille environ 30 fois par seconde. Si une carte ne reçoit plus rien pendant 1 seconde, elle devient meneuse à son tour, ce qui lui permet aussi de fonctionner seule.
- Plus tard : yeux qui réagissent à la musique (micro intégré) et au mouvement (IMU).
