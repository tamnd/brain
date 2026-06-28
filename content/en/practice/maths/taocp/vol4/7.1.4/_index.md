---
title: "TAOCP 7.1.4: Binary Decision Diagrams"
description: "Section 7.1.4 exercises: 88/267 solved."
tags: ["taocp", "mathematics", "algorithms"]
categories: ["mathematics"]
section: "7.1.4"
section_title: "Binary Decision Diagrams"
chapter: 7
chapter_title: "Combinatorial Searching"
volume: 4
weight: 7010400
draft: false
---

# Section 7.1.4. Binary Decision Diagrams

Exercises from [TAOCP Volume 4](../) Section 7.1.4: 88/267 solved.

| # | Rating | Category | Status | Time |
|---|--------|----------|--------|------|
| [1](01.md) | &#9654; [*20*] | medium | verified | 2m09s |
| [2](02.md) | &#9654; [*21*] | medium | solved | 4m20s |
| [3](03.md) |  [*16*] | medium | verified | 1m13s |
| [4](04.md) |  [*21*] | medium | verified | 2m42s |
| [5](05.md) |  [*20*] | medium | verified | 1m06s |
| [6](06.md) |  [*10*] | simple | verified | 4m19s |
| [7](07.md) |  [*21*] | medium | solved | 5m28s |
| [8](08.md) |  [*22*] | medium | solved | 1m04s |
| [9](09.md) |  [*16*] | medium | verified | 1m05s |
| [10](10.md) | &#9654; [*21*] | medium | solved | 1m04s |
| [11](11.md) |  [*20*] | medium | verified | 1m13s |
| [12](12.md) | &#9654; [*M21*] | math-medium | verified | 2m53s |
| [13](13.md) |  [*M15*] | math-simple | verified | 1m23s |
| [14](14.md) |  [*M24*] | math-medium | verified | 5m14s |
| 15 |  [*M23*] | math-medium | - | - |
| 16 | &#9654; [*22*] | medium | - | - |
| [17](17.md) |  [*32*] | hard | solved | 2m16s |
| [18](18.md) |  [*13*] | simple | solved | 3m30s |
| 19 |  [*20*] | medium | - | - |
| 20 |  [*15*] | simple | - | - |
| 21 |  [*05*] | simple | - | - |
| 22 | &#9654; [*M21*] | math-medium | - | - |
| [23](23.md) | &#9654; [*M20*] | math-medium | verified | 2m09s |
| 24 |  [*M22*] | math-medium | - | - |
| 25 |  [*M20*] | math-medium | - | - |
| 26 |  [*M20*] | math-medium | - | - |
| 27 | &#9654; [*M26*] | math-hard | - | - |
| 28 |  [*M16*] | math-medium | - | - |
| 29 |  [*HM20*] | hm-medium | - | - |
| 30 | &#9654; [*M21*] | math-medium | - | - |
| 31 |  [*M21*] | math-medium | - | - |
| 32 | &#9654; [*M20*] | math-medium | - | - |
| 33 | &#9654; [*M22*] | math-medium | - | - |
| 34 |  [*M25*] | math-medium | - | - |
| 35 | &#9654; [*22*] | medium | - | - |
| 36 |  [*25*] | medium | - | - |
| 37 |  [*M20*] | math-medium | - | - |
| 38 | &#9654; [*27*] | hard | - | - |
| 39 |  [*M20*] | math-medium | - | - |
| 40 | &#9654; [*22*] | medium | - | - |
| 41 |  [*M25*] | math-medium | - | - |
| 42 |  [*22*] | medium | - | - |
| 43 | &#9654; [*22*] | medium | - | - |
| 44 | &#9654; [*M32*] | math-hard | - | - |
| 45 |  [*22*] | medium | - | - |
| 46 |  [*M23*] | math-medium | - | - |
| 47 |  [*M21*] | math-medium | - | - |
| 48 |  [*M22*] | math-medium | - | - |
| 49 |  [*20*] | medium | - | - |
| 50 |  [*22*] | medium | - | - |
| 51 |  [*22*] | medium | - | - |
| 52 |  [*20*] | medium | - | - |
| 53 | &#9654; [*23*] | medium | - | - |
| 54 |  [*17*] | medium | - | - |
| 55 |  [*M30*] | math-hard | - | - |
| 56 |  [*20*] | medium | - | - |
| 57 |  [*25*] | medium | - | - |
| 58 |  [*20*] | medium | - | - |
| 59 | &#9654; [*M28*] | math-hard | - | - |
| 60 |  [*M22*] | math-medium | - | - |
| 61 | &#9654; [*M27*] | math-hard | - | - |
| 62 | &#9654; [*M21*] | math-medium | - | - |
| 63 |  [*M27*] | math-hard | - | - |
| 64 |  [*M21*] | math-medium | - | - |
| 65 | &#9654; [*M25*] | math-medium | - | - |
| 66 |  [*20*] | medium | - | - |
| 67 |  [*24*] | medium | - | - |
| 68 |  [*20*] | medium | - | - |
| 69 |  [*21*] | medium | - | - |
| 70 |  [*21*] | medium | - | - |
| 71 |  [*20*] | medium | - | - |
| 72 |  [*25*] | medium | - | - |
| 73 | &#9654; [*25*] | medium | - | - |
| 74 | &#9654; [*M23*] | math-medium | - | - |
| 75 |  [*M20*] | math-medium | - | - |
| 76 | &#9654; [*M22*] | math-medium | - | - |
| 77 | &#9654; [*M35*] | math-hard | - | - |
| 78 | &#9654; [*25*] | medium | - | - |
| 79 |  [*20*] | medium | - | - |
| 80 |  [*23*] | medium | - | - |
| 81 | &#9654; [*20*] | medium | - | - |
| 82 | &#9654; [*25*] | medium | - | - |
| 83 |  [*M20*] | math-medium | - | - |
| 84 |  [*24*] | medium | - | - |
| 85 |  [*16*] | medium | - | - |
| 86 | &#9654; [*21*] | medium | - | - |
| 87 |  [*20*] | medium | - | - |
| 88 | &#9654; [*M25*] | math-medium | - | - |
| 89 |  [*15*] | simple | - | - |
| 90 |  [*M20*] | math-medium | - | - |
| 91 | &#9654; [*26*] | hard | - | - |
| 92 |  [*M27*] | math-hard | - | - |
| 93 |  [*36*] | project | - | - |
| 94 |  [*21*] | medium | - | - |
| 95 | &#9654; [*20*] | medium | - | - |
| 96 |  [*20*] | medium | - | - |
| 97 |  [*M20*] | math-medium | - | - |
| 98 | &#9654; [*22*] | medium | - | - |
| 99 |  [*20*] | medium | - | - |
| [100](100.md) | &#9654; [*24*] | medium | solved | 1m37s |
| [101](101.md) |  [*20*] | medium | solved | 3m50s |
| [102](102.md) |  [*23*] | medium | verified | 4m12s |
| [103](103.md) | &#9654; [*20*] | medium | verified | 1m03s |
| [104](104.md) | &#9654; [*21*] | medium | verified | 2m53s |
| [105](105.md) |  [*25*] | medium | verified | 5m27s |
| [106](106.md) |  [*25*] | medium | verified | 2m50s |
| [107](107.md) |  [*26*] | hard | verified | 4m06s |
| [108](108.md) |  [*HM24*] | hm-medium | solved | 4m31s |
| [109](109.md) | &#9654; [*HM17*] | hm-medium | solved | 3m55s |
| [110](110.md) |  [*25*] | medium | solved | 3m06s |
| [111](111.md) |  [*M22*] | math-medium | verified | 2m23s |
| [112](112.md) |  [*HM23*] | hm-medium | solved | 1m52s |
| [113](113.md) |  [*20*] | medium | solved | 49s |
| [114](114.md) |  [*20*] | medium | solved | 2m22s |
| 115 | &#9654; [*M22*] | math-medium | - | - |
| [116](116.md) |  [*M21*] | math-medium | verified | 3m34s |
| 117 |  [*M20*] | math-medium | - | - |
| [118](118.md) |  [*M23*] | math-medium | solved | 4m16s |
| [119](119.md) |  [*20*] | medium | verified | 1m44s |
| [120](120.md) |  [*18*] | medium | verified | 4m |
| [121](121.md) | &#9654; [*M22*] | math-medium | solved | 2m40s |
| [122](122.md) |  [*27*] | hard | solved | 3m21s |
| [123](123.md) |  [*M20*] | math-medium | solved | 2m07s |
| 124 | &#9654; [*27*] | hard | - | - |
| [125](125.md) | &#9654; [*HM34*] | hm-hard | solved | 4m11s |
| [126](126.md) |  [*HM42*] | hm-project | solved | 4m11s |
| [127](127.md) |  [*46*] | research | verified | 2m47s |
| [128](128.md) | &#9654; [*25*] | medium | solved | 1m46s |
| [129](129.md) |  [*M25*] | math-medium | solved | 59s |
| [130](130.md) |  [*HM31*] | hm-hard | solved | 4m48s |
| [131](131.md) |  [*M28*] | math-hard | solved | 6m17s |
| [132](132.md) |  [*32*] | hard | solved | 4m25s |
| [133](133.md) |  [*20*] | medium | solved | 55s |
| [134](134.md) |  [*24*] | medium | solved | 4m43s |
| [135](135.md) |  [*M27*] | math-hard | solved | 4m38s |
| [136](136.md) | &#9654; [*M34*] | math-hard | solved | 3m39s |
| [137](137.md) |  [*M38*] | math-project | solved | 4m30s |
| [138](138.md) | &#9654; [*M36*] | math-project | solved | 4m34s |
| [139](139.md) |  [*22*] | medium | solved | 4m45s |
| [140](140.md) |  [*27*] | hard | verified | 3m02s |
| [141](141.md) |  [*30*] | hard | solved | 2m26s |
| [142](142.md) | &#9654; [*HM32*] | hm-hard | solved | 3m50s |
| [143](143.md) |  [*24*] | medium | solved | 1m58s |
| [144](144.md) |  [*16*] | medium | solved | 1m02s |
| [145](145.md) |  [*24*] | medium | solved | 3m41s |
| [146](146.md) | &#9654; [*M22*] | math-medium | solved | 4m28s |
| 147 | &#9654; [*27*] | hard | - | - |
| 148 |  [*M21*] | math-medium | - | - |
| 149 |  [*M20*] | math-medium | - | - |
| 150 |  [*30*] | hard | - | - |
| 151 |  [*20*] | medium | - | - |
| 152 |  [*25*] | medium | - | - |
| 153 |  [*30*] | hard | - | - |
| 154 |  [*20*] | medium | - | - |
| 155 | &#9654; [*25*] | medium | - | - |
| 156 |  [*30*] | hard | - | - |
| 157 |  [*M24*] | math-medium | - | - |
| 158 |  [*M24*] | math-medium | - | - |
| 159 |  [*20*] | medium | - | - |
| [160](160.md) | &#9654; [*24*] | medium | solved | 4m48s |
| [161](161.md) |  [*28*] | hard | solved | 4m07s |
| [162](162.md) | &#9654; [*30*] | hard | solved | 4m33s |
| [163](163.md) |  [*23*] | medium | solved | 4m24s |
| [164](164.md) | &#9654; [*M27*] | math-hard | solved | 4m24s |
| [165](165.md) |  [*M21*] | math-medium | solved | 4m21s |
| [166](166.md) |  [*M29*] | math-hard | verified | 3m59s |
| [167](167.md) |  [*21*] | medium | solved | 4m23s |
| [168](168.md) | &#9654; [*HM40*] | hm-project | solved | 3m15s |
| [169](169.md) |  [*M46*] | math-research | solved | 2m15s |
| [170](170.md) | &#9654; [*M25*] | math-medium | solved | 6m35s |
| [171](171.md) |  [*M26*] | math-hard | solved | 5m18s |
| [172](172.md) |  [*M28*] | math-hard | solved | 5m43s |
| [173](173.md) | &#9654; [*HM33*] | hm-hard | solved | 4m19s |
| [174](174.md) | &#9654; [*M39*] | math-project | solved | 4m17s |
| [175](175.md) |  [*M30*] | math-hard | verified | 1m18s |
| [176](176.md) |  [*M35*] | math-hard | solved | 4m26s |
| [177](177.md) |  [*M22*] | math-medium | verified | 2m27s |
| [178](178.md) |  [*M24*] | math-medium | solved | 3m54s |
| [179](179.md) |  [*M47*] | math-research | solved | 4m41s |
| [180](180.md) |  [*M27*] | math-hard | verified | 3m30s |
| [181](181.md) |  [*M21*] | math-medium | verified | 2m13s |
| [182](182.md) |  [*M38*] | math-project | verified | 2m33s |
| [183](183.md) | &#9654; [*M25*] | math-medium | solved | 4m15s |
| [184](184.md) |  [*M23*] | math-medium | solved | 3m31s |
| 185 |  [*M25*] | math-medium | - | - |
| 186 |  [*10*] | simple | - | - |
| 187 | &#9654; [*20*] | medium | - | - |
| 188 |  [*16*] | medium | - | - |
| 189 |  [*18*] | medium | - | - |
| 190 |  [*20*] | medium | - | - |
| 191 | &#9654; [*HM25*] | hm-medium | - | - |
| 192 |  [*M20*] | math-medium | - | - |
| 193 |  [*M21*] | math-medium | - | - |
| 194 |  [*M25*] | math-medium | - | - |
| 195 |  [*24*] | medium | - | - |
| 196 |  [*M21*] | math-medium | - | - |
| 197 |  [*25*] | medium | - | - |
| 198 | &#9654; [*23*] | medium | - | - |
| 199 |  [*21*] | medium | - | - |
| 200 |  [*21*] | medium | - | - |
| 201 |  [*22*] | medium | - | - |
| 202 |  [*24*] | medium | - | - |
| 203 | &#9654; [*M24*] | math-medium | - | - |
| 204 | &#9654; [*M25*] | math-medium | - | - |
| 205 |  [*M25*] | math-medium | - | - |
| 206 |  [*M46*] | math-research | - | - |
| 207 | &#9654; [*M25*] | math-medium | - | - |
| 208 | &#9654; [*16*] | medium | - | - |
| 209 |  [*M21*] | math-medium | - | - |
| 210 | &#9654; [*23*] | medium | - | - |
| 211 |  [*M20*] | math-medium | - | - |
| 212 | &#9654; [*25*] | medium | - | - |
| 213 |  [*16*] | medium | - | - |
| 214 | &#9654; [*21*] | medium | - | - |
| 215 |  [*21*] | medium | - | - |
| 216 | &#9654; [*30*] | hard | - | - |
| 217 |  [*29*] | hard | - | - |
| 218 | &#9654; [*24*] | medium | - | - |
| 219 |  [*20*] | medium | - | - |
| 220 | &#9654; [*21*] | medium | - | - |
| 221 | &#9654; [*M27*] | math-hard | - | - |
| 222 | &#9654; [*27*] | hard | - | - |
| 223 |  [*28*] | hard | - | - |
| 224 | &#9654; [*20*] | medium | - | - |
| 225 | &#9654; [*30*] | hard | - | - |
| 226 | &#9654; [*20*] | medium | - | - |
| 227 |  [*20*] | medium | - | - |
| 228 |  [*21*] | medium | - | - |
| [229](229.md) |  [*15*] | simple | solved | 57s |
| [230](230.md) |  [*25*] | medium | solved | 1m51s |
| 231 |  [*23*] | medium | - | - |
| 232 | &#9654; [*23*] | medium | - | - |
| 233 | &#9654; [*25*] | medium | - | - |
| 234 |  [*22*] | medium | - | - |
| 235 |  [*22*] | medium | - | - |
| 236 | &#9654; [*M25*] | math-medium | - | - |
| 237 |  [*25*] | medium | - | - |
| 238 | &#9654; [*22*] | medium | - | - |
| 239 | &#9654; [*21*] | medium | - | - |
| 240 | &#9654; [*22*] | medium | - | - |
| 241 | &#9654; [*28*] | hard | - | - |
| 242 |  [*24*] | medium | - | - |
| 243 |  [*M23*] | math-medium | - | - |
| 244 |  [*25*] | medium | - | - |
| 245 | &#9654; [*M22*] | math-medium | - | - |
| 246 |  [*M21*] | math-medium | - | - |
| 247 | &#9654; [*M27*] | math-hard | - | - |
| 248 |  [*M22*] | math-medium | - | - |
| 249 |  [*HM31*] | hm-hard | - | - |
| 250 |  [*28*] | hard | - | - |
| 251 |  [*M46*] | math-research | - | - |
| 252 |  [*M30*] | math-hard | - | - |
| 253 | &#9654; [*M26*] | math-hard | - | - |
| 254 | &#9654; [*M23*] | math-medium | - | - |
| 255 | &#9654; [*25*] | medium | - | - |
| 256 |  [*M32*] | math-hard | - | - |
| 257 |  [*40*] | project | - | - |
| 258 | &#9654; [*25*] | medium | - | - |
| 259 | &#9654; [*25*] | medium | - | - |
| 260 | &#9654; [*M27*] | math-hard | - | - |
| 261 |  [*HM21*] | hm-medium | - | - |
| 262 |  [*M26*] | math-hard | - | - |
| 263 |  [*HM25*] | hm-medium | - | - |
| 264 |  [*M46*] | math-research | - | - |
| 265 | &#9654; [*21*] | medium | - | - |
| 266 | &#9654; [*20*] | medium | - | - |
| 267 |  [*HM32*] | hm-hard | - | - |
