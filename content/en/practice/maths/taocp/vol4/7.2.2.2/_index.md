---
title: "TAOCP 7.2.2.2: Satisfiability"
description: "Section 7.2.2.2 exercises: 105/522 solved."
tags: ["taocp", "mathematics", "algorithms"]
categories: ["mathematics"]
section: "7.2.2.2"
section_title: "Satisfiability"
chapter: 7
chapter_title: "Combinatorial Searching"
volume: 4
weight: 7020202
draft: false
---

# Section 7.2.2.2. Satisfiability

Exercises from [TAOCP Volume 4](../) Section 7.2.2.2: 105/522 solved.

| # | Rating | Category | Status | Time |
|---|--------|----------|--------|------|
| [1](01.md) |  [*10*] | simple | verified | 51s |
| [2](02.md) |  [*20*] | medium | solved | 58s |
| [3](03.md) | &#9654; [*M21*] | math-medium | verified | 1m30s |
| [4](04.md) | &#9654; [*22*] | medium | solved | 1m30s |
| [5](05.md) |  [*M20*] | math-medium | solved | 2m55s |
| [6](06.md) | &#9654; [*HM27*] | hm-hard | verified | 1m50s |
| [7](07.md) |  [*25*] | medium | solved | 1m47s |
| [8](08.md) | &#9654; [*22*] | medium | verified | 1m23s |
| [9](09.md) |  [*M21*] | math-medium | solved | 2m13s |
| [10](10.md) | &#9654; [*21*] | medium | solved | 1m53s |
| [13](13.md) |  [*24*] | medium | solved | 2m48s |
| [14](14.md) |  [*22*] | medium | verified | 56s |
| [15](15.md) |  [*24*] | medium | verified | 1m03s |
| [16](16.md) |  [*21*] | medium | verified | 1m08s |
| [17](17.md) |  [*26*] | hard | solved | 3m21s |
| [18](18.md) | &#9654; [*28*] | hard | solved | 5m49s |
| 19 | &#9654; [*29*] | hard | - | - |
| 20 |  [*40*] | project | - | - |
| 21 |  [*22*] | medium | - | - |
| 22 |  [*20*] | medium | - | - |
| 23 |  [*20*] | medium | - | - |
| 24 | &#9654; [*M32*] | math-hard | - | - |
| 25 |  [*21*] | medium | - | - |
| 26 |  [*22*] | medium | - | - |
| 27 |  [*20*] | medium | - | - |
| 28 | &#9654; [*20*] | medium | - | - |
| 29 | &#9654; [*20*] | medium | - | - |
| 30 | &#9654; [*22*] | medium | - | - |
| 31 |  [*28*] | hard | - | - |
| 32 |  [*15*] | simple | - | - |
| 33 |  [*21*] | medium | - | - |
| 34 |  [*HM26*] | hm-hard | - | - |
| 37 |  [*20*] | medium | - | - |
| 38 |  [*M25*] | math-medium | - | - |
| 39 |  [*M46*] | math-research | - | - |
| 40 |  [*01*] | simple | - | - |
| 41 |  [*M31*] | math-hard | - | - |
| 42 |  [*21*] | medium | - | - |
| 43 | &#9654; [*21*] | medium | - | - |
| 44 | &#9654; [*30*] | hard | - | - |
| 45 |  [*20*] | medium | - | - |
| 46 |  [*30*] | hard | - | - |
| 47 |  [*30*] | hard | - | - |
| 48 |  [*20*] | medium | - | - |
| 49 |  [*21*] | medium | - | - |
| 50 |  [*24*] | medium | - | - |
| 51 |  [*40*] | project | - | - |
| 52 |  [*15*] | simple | - | - |
| 53 | &#9654; [*M20*] | math-medium | - | - |
| 54 | &#9654; [*29*] | hard | - | - |
| 55 |  [*21*] | medium | - | - |
| 56 | &#9654; [*22*] | medium | - | - |
| 57 |  [*29*] | hard | - | - |
| 58 | &#9654; [*20*] | medium | - | - |
| 59 |  [*M20*] | math-medium | - | - |
| 60 |  [*24*] | medium | - | - |
| 61 |  [*30*] | hard | - | - |
| 62 |  [*29*] | hard | - | - |
| 63 | &#9654; [*29*] | hard | - | - |
| 64 |  [*26*] | hard | - | - |
| 65 | &#9654; [*28*] | hard | - | - |
| 66 |  [*24*] | medium | - | - |
| 67 |  [**] |  | - | - |
| 68 |  [*39*] | project | - | - |
| 69 |  [*23*] | medium | - | - |
| 70 |  [*21*] | medium | - | - |
| 71 | &#9654; [*22*] | medium | - | - |
| 72 |  [*28*] | hard | - | - |
| 73 | &#9654; [*21*] | medium | - | - |
| 74 |  [*M28*] | math-hard | - | - |
| 75 |  [*M22*] | math-medium | - | - |
| 76 |  [*41*] | project | - | - |
| 77 |  [*20*] | medium | - | - |
| 78 |  [*21*] | medium | - | - |
| 79 |  [*29*] | hard | - | - |
| 80 |  [*21*] | medium | - | - |
| 81 |  [*21*] | medium | - | - |
| 82 | &#9654; [*22*] | medium | - | - |
| 83 |  [*21*] | medium | - | - |
| 84 |  [*33*] | hard | - | - |
| 85 | &#9654; [*39*] | project | - | - |
| 86 |  [*M29*] | math-hard | - | - |
| 87 |  [*21*] | medium | - | - |
| 88 |  [*15*] | simple | - | - |
| 89 |  [*21*] | medium | - | - |
| 90 |  [*20*] | medium | - | - |
| 91 |  [*M21*] | math-medium | - | - |
| 92 |  [*20*] | medium | - | - |
| 93 |  [*20*] | medium | - | - |
| 94 | &#9654; [*21*] | medium | - | - |
| 95 |  [*20*] | medium | - | - |
| 96 |  [*22*] | medium | - | - |
| 97 |  [*20*] | medium | - | - |
| 98 | &#9654; [*M23*] | math-medium | - | - |
| 99 |  [*25*] | medium | - | - |
| [100](100.md) |  [*22*] | medium | verified | 1m31s |
| [101](101.md) | &#9654; [*31*] | hard | solved | 2m13s |
| [102](102.md) |  [*22*] | medium | solved | 1m53s |
| [103](103.md) |  [*18*] | medium | verified | 1m36s |
| [104](104.md) |  [*M21*] | math-medium | solved | 5m50s |
| [105](105.md) | &#9654; [*M28*] | math-hard | solved | 5m46s |
| [106](106.md) |  [*M20*] | math-medium | verified | 2m16s |
| [107](107.md) | &#9654; [*22*] | medium | solved | 2m17s |
| [108](108.md) |  [*23*] | medium | solved | 2m07s |
| [109](109.md) | &#9654; [*20*] | medium | verified | 1m34s |
| [110](110.md) |  [*19*] | medium | solved | 3m22s |
| [111](111.md) |  [*40*] | project | solved | 4m39s |
| [112](112.md) |  [*46*] | research | solved | 2m04s |
| [113](113.md) | &#9654; [*30*] | hard | solved | 2m42s |
| [114](114.md) |  [*27*] | hard | solved | 2m15s |
| [115](115.md) |  [*25*] | medium | solved | 2m15s |
| [116](116.md) |  [*22*] | medium | verified | 3m05s |
| [117](117.md) |  [*23*] | medium | verified | 1m03s |
| [118](118.md) |  [*20*] | medium | solved | 1m22s |
| [119](119.md) |  [*18*] | medium | solved | 2m |
| [120](120.md) |  [*M20*] | math-medium | verified | 1m23s |
| [121](121.md) |  [*21*] | medium | solved | 1m37s |
| [122](122.md) | &#9654; [*21*] | medium | solved | 2m23s |
| [123](123.md) |  [*17*] | medium | solved | 3m07s |
| [124](124.md) | &#9654; [*21*] | medium | solved | 2m40s |
| [125](125.md) | &#9654; [*20*] | medium | verified | 1m40s |
| [126](126.md) |  [*20*] | medium | solved | 3m06s |
| [127](127.md) |  [*17*] | medium | solved | 2m17s |
| [128](128.md) |  [*19*] | medium | solved | 1m26s |
| [129](129.md) |  [*20*] | medium | solved | 2m32s |
| [130](130.md) |  [*22*] | medium | solved | 2m27s |
| [131](131.md) | &#9654; [*30*] | hard | solved | 2m06s |
| [132](132.md) | &#9654; [*32*] | hard | solved | 4m04s |
| [133](133.md) | &#9654; [*25*] | medium | solved | 3m06s |
| [134](134.md) |  [*22*] | medium | solved | 2m04s |
| [135](135.md) | &#9654; [*16*] | medium | verified | 1m20s |
| [136](136.md) |  [*15*] | simple | verified | 2m04s |
| [137](137.md) |  [*24*] | medium | solved | 1m28s |
| [138](138.md) |  [*20*] | medium | solved | 1m55s |
| [139](139.md) |  [*25*] | medium | verified | 1m31s |
| [140](140.md) |  [*21*] | medium | solved | 1m21s |
| [141](141.md) |  [*18*] | medium | solved | 2m03s |
| [142](142.md) |  [*24*] | medium | solved | 2m |
| [143](143.md) | &#9654; [*30*] | hard | solved | 2m09s |
| [144](144.md) |  [*15*] | simple | solved | 3m05s |
| [145](145.md) |  [*23*] | medium | solved | 3m05s |
| [146](146.md) |  [*25*] | medium | solved | 3m53s |
| [147](147.md) |  [*05*] | simple | verified | 57s |
| [148](148.md) |  [*21*] | medium | verified | 59s |
| [149](149.md) | &#9654; [*26*] | hard | verified | 1m03s |
| [150](150.md) |  [*21*] | medium | solved | 3m40s |
| [151](151.md) | &#9654; [*26*] | hard | solved | 2m43s |
| [152](152.md) |  [*22*] | medium | verified | 3m30s |
| [153](153.md) |  [*17*] | medium | verified | 1m53s |
| [154](154.md) |  [*20*] | medium | verified | 3m28s |
| [155](155.md) |  [*32*] | hard | verified | 1m10s |
| [156](156.md) |  [*05*] | simple | verified | 1m03s |
| [157](157.md) |  [*10*] | simple | verified | 58s |
| [158](158.md) |  [*15*] | simple | solved | 1m32s |
| [159](159.md) |  [*M17*] | math-medium | verified | 1m18s |
| [160](160.md) |  [*18*] | medium | verified | 1m12s |
| [161](161.md) | &#9654; [*21*] | medium | verified | 1m17s |
| [162](162.md) |  [*21*] | medium | verified | 2m42s |
| [163](163.md) |  [*M25*] | math-medium | solved | 1m44s |
| [164](164.md) |  [*M30*] | math-hard | verified | 1m19s |
| [165](165.md) | &#9654; [*26*] | hard | verified | 2m37s |
| [166](166.md) |  [*30*] | hard | solved | 3m41s |
| [167](167.md) | &#9654; [*21*] | medium | solved | 5m52s |
| [168](168.md) |  [*26*] | hard | verified | 1m04s |
| [169](169.md) | &#9654; [*HM30*] | hm-hard | solved | 59s |
| [170](170.md) |  [*25*] | medium | solved | 1m03s |
| [171](171.md) |  [*20*] | medium | solved | 1m03s |
| [172](172.md) |  [*21*] | medium | verified | 1m14s |
| [173](173.md) |  [*40*] | project | verified | 2m08s |
| [174](174.md) |  [*15*] | simple | solved | 50s |
| [175](175.md) |  [*32*] | hard | solved | 1m12s |
| [176](176.md) |  [*M25*] | math-medium | solved | 4m30s |
| [177](177.md) |  [*HM26*] | hm-hard | solved | 4m |
| [178](178.md) | &#9654; [*M23*] | math-medium | solved | 2m25s |
| [179](179.md) |  [*25*] | medium | solved | 5m44s |
| [180](180.md) | &#9654; [*25*] | medium | solved | 5m49s |
| [181](181.md) | &#9654; [*25*] | medium | solved | 5m36s |
| [182](182.md) |  [*M16*] | math-medium | solved | 5m27s |
| [183](183.md) |  [*M30*] | math-hard | verified | 2m51s |
| [184](184.md) |  [*M20*] | math-medium | verified | 4m03s |
| [185](185.md) |  [*M20*] | math-medium | solved | 1m37s |
| [186](186.md) |  [*M21*] | math-medium | solved | 3m05s |
| 187 |  [*M20*] | math-medium | - | - |
| 188 |  [*HM25*] | hm-medium | - | - |
| 189 |  [*27*] | hard | - | - |
| 190 |  [*M20*] | math-medium | - | - |
| 191 |  [*M25*] | math-medium | - | - |
| 192 | &#9654; [*HM21*] | hm-medium | - | - |
| 193 |  [*HM48*] | hm-research | - | - |
| 194 |  [*HM19*] | hm-medium | - | - |
| 195 |  [*HM21*] | hm-medium | - | - |
| 196 | &#9654; [*HM25*] | hm-medium | - | - |
| 197 |  [*HM21*] | hm-medium | - | - |
| 198 | &#9654; [*HM30*] | hm-hard | - | - |
| 199 |  [*M21*] | math-medium | - | - |
| 200 | &#9654; [*M21*] | math-medium | - | - |
| 201 |  [*HM29*] | hm-hard | - | - |
| 202 |  [*HM21*] | hm-medium | - | - |
| 203 |  [*HM93*] | hm-research | - | - |
| 204 | &#9654; [*28*] | hard | - | - |
| 205 |  [*26*] | hard | - | - |
| 206 |  [*M22*] | math-medium | - | - |
| 207 |  [*22*] | medium | - | - |
| 208 |  [*25*] | medium | - | - |
| 209 |  [*25*] | medium | - | - |
| 210 |  [*M36*] | math-project | - | - |
| 211 |  [*30*] | hard | - | - |
| 212 |  [*32*] | hard | - | - |
| 213 | &#9654; [*M26*] | math-hard | - | - |
| 214 |  [*HM38*] | hm-project | - | - |
| 215 | &#9654; [*HM23*] | hm-medium | - | - |
| 216 |  [*HM38*] | hm-project | - | - |
| 217 |  [*20*] | medium | - | - |
| 218 |  [*20*] | medium | - | - |
| 219 | &#9654; [*M20*] | math-medium | - | - |
| 220 |  [*M24*] | math-medium | - | - |
| 221 |  [*16*] | medium | - | - |
| 222 |  [*M30*] | math-hard | - | - |
| 223 |  [*HM40*] | hm-project | - | - |
| 224 |  [*M20*] | math-medium | - | - |
| 225 | &#9654; [*M31*] | math-hard | - | - |
| 226 |  [*M30*] | math-hard | - | - |
| 227 |  [*M27*] | math-hard | - | - |
| 228 | &#9654; [*M21*] | math-medium | - | - |
| 229 |  [*M21*] | math-medium | - | - |
| 230 |  [*M22*] | math-medium | - | - |
| 231 |  [*M30*] | math-hard | - | - |
| 232 |  [*M28*] | math-hard | - | - |
| 233 |  [*16*] | medium | - | - |
| 234 |  [*20*] | medium | - | - |
| 235 |  [*30*] | hard | - | - |
| 236 |  [*8*] | simple | - | - |
| 237 |  [*28*] | hard | - | - |
| 238 |  [*HM21*] | hm-medium | - | - |
| 239 | &#9654; [*M21*] | math-medium | - | - |
| 240 |  [*HM23*] | hm-medium | - | - |
| 241 |  [*20*] | medium | - | - |
| 242 |  [*M20*] | math-medium | - | - |
| 243 |  [*HM31*] | hm-hard | - | - |
| 244 |  [*M20*] | math-medium | - | - |
| 245 | &#9654; [*M27*] | math-hard | - | - |
| 246 | &#9654; [*M28*] | math-hard | - | - |
| 247 |  [*18*] | medium | - | - |
| 248 |  [*M20*] | math-medium | - | - |
| 249 |  [*18*] | medium | - | - |
| 250 |  [**] |  | - | - |
| 251 | &#9654; [*30*] | hard | - | - |
| 252 |  [*M26*] | math-hard | - | - |
| 253 | &#9654; [*18*] | medium | - | - |
| 254 |  [*16*] | medium | - | - |
| 255 | &#9654; [*20*] | medium | - | - |
| 256 |  [*20*] | medium | - | - |
| 257 | &#9654; [*30*] | hard | - | - |
| 258 |  [*21*] | medium | - | - |
| 259 |  [*M20*] | math-medium | - | - |
| 260 |  [*21*] | medium | - | - |
| 261 |  [*21*] | medium | - | - |
| 262 |  [*20*] | medium | - | - |
| 263 |  [*21*] | medium | - | - |
| 264 |  [*20*] | medium | - | - |
| 265 |  [*21*] | medium | - | - |
| 266 |  [*20*] | medium | - | - |
| 267 |  [*25*] | medium | - | - |
| 268 |  [*21*] | medium | - | - |
| 269 |  [*29*] | hard | - | - |
| 270 |  [*25*] | medium | - | - |
| 271 | &#9654; [*25*] | medium | - | - |
| 272 |  [*30*] | hard | - | - |
| 273 |  [*27*] | hard | - | - |
| 274 |  [*35*] | hard | - | - |
| 275 | &#9654; [*22*] | medium | - | - |
| 276 |  [*M15*] | math-simple | - | - |
| 277 |  [*M18*] | math-medium | - | - |
| 278 |  [*22*] | medium | - | - |
| 279 |  [*M20*] | math-medium | - | - |
| 280 | &#9654; [*M26*] | math-hard | - | - |
| 281 |  [*21*] | medium | - | - |
| 282 | &#9654; [*M33*] | math-hard | - | - |
| 283 |  [*HM46*] | hm-research | - | - |
| 284 |  [*23*] | medium | - | - |
| 285 |  [*19*] | medium | - | - |
| 286 |  [*M24*] | math-medium | - | - |
| 287 |  [*25*] | medium | - | - |
| 288 |  [*28*] | hard | - | - |
| 289 |  [*M20*] | math-medium | - | - |
| 290 |  [*17*] | medium | - | - |
| 291 |  [*20*] | medium | - | - |
| 292 |  [*M21*] | math-medium | - | - |
| 293 |  [*21*] | medium | - | - |
| 294 |  [*HM21*] | hm-medium | - | - |
| 295 |  [*M23*] | math-medium | - | - |
| 296 |  [*HM20*] | hm-medium | - | - |
| 297 | &#9654; [*HM26*] | hm-hard | - | - |
| 298 |  [*HM22*] | hm-medium | - | - |
| 299 |  [*HM23*] | hm-medium | - | - |
| 300 | &#9654; [*25*] | medium | - | - |
| 301 | &#9654; [*25*] | medium | - | - |
| 302 |  [*26*] | hard | - | - |
| 303 |  [*HM20*] | hm-medium | - | - |
| 304 |  [*HM34*] | hm-hard | - | - |
| 305 | &#9654; [*M25*] | math-medium | - | - |
| 306 | &#9654; [*HM32*] | hm-hard | - | - |
| 307 |  [*HM28*] | hm-hard | - | - |
| 308 |  [*M29*] | math-hard | - | - |
| 309 |  [*20*] | medium | - | - |
| 310 |  [*M25*] | math-medium | - | - |
| 311 |  [*21*] | medium | - | - |
| 312 |  [*HM24*] | hm-medium | - | - |
| 313 | &#9654; [*22*] | medium | - | - |
| 314 |  [*36*] | project | - | - |
| 315 |  [*M18*] | math-medium | - | - |
| 316 |  [*HM20*] | hm-medium | - | - |
| 317 | &#9654; [*M26*] | math-hard | - | - |
| 318 |  [*HM27*] | hm-hard | - | - |
| 319 |  [*HM20*] | hm-medium | - | - |
| 320 |  [*HM24*] | hm-medium | - | - |
| 321 |  [*M24*] | math-medium | - | - |
| 322 | &#9654; [*HM35*] | hm-hard | - | - |
| 323 |  [*10*] | simple | - | - |
| 324 | &#9654; [*22*] | medium | - | - |
| 325 |  [*20*] | medium | - | - |
| 326 |  [*20*] | medium | - | - |
| 327 |  [*22*] | medium | - | - |
| 328 |  [*20*] | medium | - | - |
| 329 |  [*21*] | medium | - | - |
| 330 | &#9654; [*21*] | medium | - | - |
| 331 |  [*M20*] | math-medium | - | - |
| 332 |  [*20*] | medium | - | - |
| 333 | &#9654; [*M20*] | math-medium | - | - |
| 334 |  [*25*] | medium | - | - |
| 335 |  [*HM26*] | hm-hard | - | - |
| 336 | &#9654; [*M20*] | math-medium | - | - |
| 337 |  [*M20*] | math-medium | - | - |
| 338 |  [*M21*] | math-medium | - | - |
| 339 | &#9654; [*HM26*] | hm-hard | - | - |
| 340 | &#9654; [*M20*] | math-medium | - | - |
| 341 |  [*M25*] | math-medium | - | - |
| 342 |  [*HM25*] | hm-medium | - | - |
| 343 | &#9654; [*M25*] | math-medium | - | - |
| 344 |  [*M33*] | math-hard | - | - |
| 345 |  [*M30*] | math-hard | - | - |
| 346 | &#9654; [*HM28*] | hm-hard | - | - |
| 347 | &#9654; [*M28*] | math-hard | - | - |
| 348 |  [*HM26*] | hm-hard | - | - |
| 349 | &#9654; [*M24*] | math-medium | - | - |
| 350 | &#9654; [*HM26*] | hm-hard | - | - |
| 351 |  [*25*] | medium | - | - |
| 352 |  [*M21*] | math-medium | - | - |
| 353 |  [*M21*] | math-medium | - | - |
| 354 |  [*HM20*] | hm-medium | - | - |
| 355 |  [*HM21*] | hm-medium | - | - |
| 356 | &#9654; [*M35*] | math-hard | - | - |
| 357 | &#9654; [*M20*] | math-medium | - | - |
| 358 |  [*M20*] | math-medium | - | - |
| 359 |  [*20*] | medium | - | - |
| 360 |  [*M23*] | math-medium | - | - |
| 361 | &#9654; [*M25*] | math-medium | - | - |
| 362 |  [*20*] | medium | - | - |
| 363 | &#9654; [*M30*] | math-hard | - | - |
| 364 | &#9654; [*M21*] | math-medium | - | - |
| 365 |  [*M37*] | math-project | - | - |
| 366 | &#9654; [*18*] | medium | - | - |
| 367 | &#9654; [*20*] | medium | - | - |
| 368 |  [*76*] | research | - | - |
| 369 | &#9654; [**] |  | - | - |
| 370 |  [*20*] | medium | - | - |
| 371 |  [*24*] | medium | - | - |
| 372 |  [*25*] | medium | - | - |
| 373 |  [*35*] | hard | - | - |
| 374 | &#9654; [*32*] | hard | - | - |
| 375 |  [*21*] | medium | - | - |
| 376 | &#9654; [*32*] | hard | - | - |
| 377 |  [*22*] | medium | - | - |
| 378 |  [*39*] | project | - | - |
| 379 | &#9654; [*20*] | medium | - | - |
| 380 |  [*21*] | medium | - | - |
| 381 |  [*22*] | medium | - | - |
| 382 |  [*30*] | hard | - | - |
| 383 | &#9654; [*23*] | medium | - | - |
| 384 |  [*25*] | medium | - | - |
| 385 |  [**] |  | - | - |
| 386 | &#9654; [*M25*] | math-medium | - | - |
| 387 |  [*21*] | medium | - | - |
| 388 |  [*20*] | medium | - | - |
| 389 |  [*22*] | medium | - | - |
| 390 |  [*23*] | medium | - | - |
| 391 |  [*M25*] | math-medium | - | - |
| 392 |  [*22*] | medium | - | - |
| 393 |  [*25*] | medium | - | - |
| 394 |  [*25*] | medium | - | - |
| 395 |  [*20*] | medium | - | - |
| 396 | &#9654; [*23*] | medium | - | - |
| 397 |  [*22*] | medium | - | - |
| 398 |  [*18*] | medium | - | - |
| 399 |  [*23*] | medium | - | - |
| 400 |  [*25*] | medium | - | - |
| 401 |  [*16*] | medium | - | - |
| 402 |  [*18*] | medium | - | - |
| 403 |  [*20*] | medium | - | - |
| 404 | &#9654; [*21*] | medium | - | - |
| 405 | &#9654; [*M25*] | math-medium | - | - |
| 406 |  [*M24*] | math-medium | - | - |
| 407 |  [*M22*] | math-medium | - | - |
| 408 | &#9654; [*25*] | medium | - | - |
| 409 | &#9654; [*M26*] | math-hard | - | - |
| 410 |  [*24*] | medium | - | - |
| 411 |  [*25*] | medium | - | - |
| 412 |  [*40*] | project | - | - |
| 413 |  [*M23*] | math-medium | - | - |
| 414 |  [*M20*] | math-medium | - | - |
| 415 |  [*M22*] | math-medium | - | - |
| 416 |  [*20*] | medium | - | - |
| 417 |  [*21*] | medium | - | - |
| 418 |  [*23*] | medium | - | - |
| 419 |  [*M21*] | math-medium | - | - |
| 420 |  [*18*] | medium | - | - |
| 421 |  [*18*] | medium | - | - |
| 422 |  [*11*] | simple | - | - |
| 423 |  [*22*] | medium | - | - |
| 424 | &#9654; [*20*] | medium | - | - |
| 425 |  [*18*] | medium | - | - |
| 426 | &#9654; [*M20*] | math-medium | - | - |
| 427 |  [*M30*] | math-hard | - | - |
| 428 |  [*M27*] | math-hard | - | - |
| 429 |  [*22*] | medium | - | - |
| 430 |  [*25*] | medium | - | - |
| 431 | &#9654; [*20*] | medium | - | - |
| 432 |  [*34*] | hard | - | - |
| 433 |  [*25*] | medium | - | - |
| 434 |  [*21*] | medium | - | - |
| 435 | &#9654; [*28*] | hard | - | - |
| 436 |  [*M32*] | math-hard | - | - |
| 437 |  [*M21*] | math-medium | - | - |
| 438 |  [*21*] | medium | - | - |
| 439 |  [*20*] | medium | - | - |
| 440 |  [*M33*] | math-hard | - | - |
| 441 |  [*M35*] | math-hard | - | - |
| 442 | &#9654; [*M27*] | math-hard | - | - |
| 443 |  [**] |  | - | - |
| 444 |  [*M26*] | math-hard | - | - |
| 445 | &#9654; [*22*] | medium | - | - |
| 446 |  [*M10*] | math-simple | - | - |
| 447 | &#9654; [*22*] | medium | - | - |
| 448 |  [*M23*] | math-medium | - | - |
| 449 |  [*21*] | medium | - | - |
| 450 |  [*25*] | medium | - | - |
| 451 | &#9654; [*28*] | hard | - | - |
| 452 |  [*34*] | hard | - | - |
| 453 |  [*M23*] | math-medium | - | - |
| 454 |  [*15*] | simple | - | - |
| 455 |  [*M20*] | math-medium | - | - |
| 456 |  [*M21*] | math-medium | - | - |
| 457 |  [*HM19*] | hm-medium | - | - |
| 458 |  [*20*] | medium | - | - |
| 459 | &#9654; [*20*] | medium | - | - |
| 460 |  [*21*] | medium | - | - |
| 461 |  [*20*] | medium | - | - |
| 462 |  [*22*] | medium | - | - |
| 463 | &#9654; [*M21*] | math-medium | - | - |
| 464 | &#9654; [*M25*] | math-medium | - | - |
| 465 |  [*M21*] | math-medium | - | - |
| 466 |  [*M23*] | math-medium | - | - |
| 467 |  [*20*] | medium | - | - |
| 468 |  [*20*] | medium | - | - |
| 469 | &#9654; [**] |  | - | - |
| 470 | &#9654; [**] |  | - | - |
| 471 |  [*16*] | medium | - | - |
| 472 |  [**] |  | - | - |
| 473 | &#9654; [**] |  | - | - |
| 474 |  [**] |  | - | - |
| 475 |  [**] |  | - | - |
| 476 |  [**] |  | - | - |
| 477 | &#9654; [*23*] | medium | - | - |
| 478 | &#9654; [*23*] | medium | - | - |
| 479 | &#9654; [*25*] | medium | - | - |
| 480 |  [*25*] | medium | - | - |
| 481 | &#9654; [*28*] | hard | - | - |
| 482 | &#9654; [*26*] | hard | - | - |
| 483 |  [*21*] | medium | - | - |
| 484 |  [*22*] | medium | - | - |
| 485 | &#9654; [*23*] | medium | - | - |
| 486 |  [*21*] | medium | - | - |
| 487 | &#9654; [*27*] | hard | - | - |
| 488 |  [*24*] | medium | - | - |
| 489 |  [*M21*] | math-medium | - | - |
| 490 |  [*15*] | simple | - | - |
| 491 |  [*22*] | medium | - | - |
| 492 |  [*M20*] | math-medium | - | - |
| 493 |  [*20*] | medium | - | - |
| 494 |  [*21*] | medium | - | - |
| 495 |  [*M22*] | math-medium | - | - |
| 496 |  [*M20*] | math-medium | - | - |
| 497 |  [*22*] | medium | - | - |
| 498 |  [*22*] | medium | - | - |
| 499 |  [*21*] | medium | - | - |
| 500 |  [*16*] | medium | - | - |
| 501 |  [*22*] | medium | - | - |
| 502 |  [*16*] | medium | - | - |
| 503 |  [*M20*] | math-medium | - | - |
| 504 | &#9654; [*M21*] | math-medium | - | - |
| 505 |  [*21*] | medium | - | - |
| 506 |  [*22*] | medium | - | - |
| 507 | &#9654; [*21*] | medium | - | - |
| 508 |  [*M20*] | math-medium | - | - |
| 509 |  [*20*] | medium | - | - |
| 510 |  [*18*] | medium | - | - |
| 511 |  [*22*] | medium | - | - |
| 512 |  [*29*] | hard | - | - |
| 513 |  [*24*] | medium | - | - |
| 514 |  [*24*] | medium | - | - |
| 515 | &#9654; [*23*] | medium | - | - |
| 516 |  [*M9*] | math-simple | - | - |
| 517 |  [*25*] | medium | - | - |
| 518 |  [*M32*] | math-hard | - | - |
| 519 |  [*20*] | medium | - | - |
| 520 | &#9654; [*24*] | medium | - | - |
| 521 |  [*30*] | hard | - | - |
| 522 | &#9654; [*26*] | hard | - | - |
| 523 |  [*20*] | medium | - | - |
| 524 | &#9654; [*22*] | medium | - | - |
| 525 | &#9654; [*40*] | project | - | - |
| 526 |  [*M25*] | math-medium | - | - |
