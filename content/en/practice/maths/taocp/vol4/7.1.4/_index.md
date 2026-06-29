---
title: "TAOCP 7.1.4: Binary Decision Diagrams"
description: "Section 7.1.4 exercises: 189/267 solved."
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

Exercises from [TAOCP Volume 4](../) Section 7.1.4: 189/267 solved.

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
| [15](15.md) |  [*M23*] | math-medium | solved | 5m38s |
| [16](16.md) | &#9654; [*22*] | medium | solved | 2m21s |
| [17](17.md) |  [*32*] | hard | solved | 2m16s |
| [18](18.md) |  [*13*] | simple | solved | 3m30s |
| [19](19.md) |  [*20*] | medium | solved | 1m08s |
| [20](20.md) |  [*15*] | simple | verified | 2m12s |
| [21](21.md) |  [*05*] | simple | verified | 1m05s |
| [22](22.md) | &#9654; [*M21*] | math-medium | solved | 3m51s |
| [23](23.md) | &#9654; [*M20*] | math-medium | verified | 2m09s |
| [24](24.md) |  [*M22*] | math-medium | solved | 59s |
| [25](25.md) |  [*M20*] | math-medium | verified | 2m24s |
| [26](26.md) |  [*M20*] | math-medium | verified | 1m08s |
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
| [147](147.md) | &#9654; [*27*] | hard | solved | 5m01s |
| [148](148.md) |  [*M21*] | math-medium | solved | 2m42s |
| [149](149.md) |  [*M20*] | math-medium | solved | 50s |
| [150](150.md) |  [*30*] | hard | solved | 4m35s |
| [151](151.md) |  [*20*] | medium | verified | 2m16s |
| [152](152.md) |  [*25*] | medium | solved | 1m08s |
| [153](153.md) |  [*30*] | hard | solved | 2m34s |
| [154](154.md) |  [*20*] | medium | solved | 1m13s |
| [155](155.md) | &#9654; [*25*] | medium | solved | 2m35s |
| [156](156.md) |  [*30*] | hard | verified | 4m18s |
| [157](157.md) |  [*M24*] | math-medium | solved | 4m20s |
| [158](158.md) |  [*M24*] | math-medium | solved | 4m27s |
| [159](159.md) |  [*20*] | medium | solved | 2m30s |
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
| [185](185.md) |  [*M25*] | math-medium | solved | 2m47s |
| [186](186.md) |  [*10*] | simple | verified | 1m16s |
| [187](187.md) | &#9654; [*20*] | medium | solved | 3m43s |
| [188](188.md) |  [*16*] | medium | solved | 1m05s |
| [189](189.md) |  [*18*] | medium | solved | 2m24s |
| [190](190.md) |  [*20*] | medium | solved | 4m07s |
| [191](191.md) | &#9654; [*HM25*] | hm-medium | verified | 1m16s |
| [192](192.md) |  [*M20*] | math-medium | solved | 4m32s |
| [193](193.md) |  [*M21*] | math-medium | verified | 2m31s |
| [194](194.md) |  [*M25*] | math-medium | solved | 4m32s |
| [195](195.md) |  [*24*] | medium | solved | 4m |
| [196](196.md) |  [*M21*] | math-medium | solved | 1m11s |
| [197](197.md) |  [*25*] | medium | verified | 1m09s |
| [198](198.md) | &#9654; [*23*] | medium | solved | 1m13s |
| [199](199.md) |  [*21*] | medium | solved | 1m09s |
| [200](200.md) |  [*21*] | medium | solved | 3m46s |
| [201](201.md) |  [*22*] | medium | verified | 2m45s |
| [202](202.md) |  [*24*] | medium | verified | 1m19s |
| [203](203.md) | &#9654; [*M24*] | math-medium | solved | 6m31s |
| [204](204.md) | &#9654; [*M25*] | math-medium | solved | 5m21s |
| [205](205.md) |  [*M25*] | math-medium | solved | 3m32s |
| [206](206.md) |  [*M46*] | math-research | verified | 3m44s |
| [207](207.md) | &#9654; [*M25*] | math-medium | solved | 1m11s |
| [208](208.md) | &#9654; [*16*] | medium | verified | 2m43s |
| [209](209.md) |  [*M21*] | math-medium | verified | 2m52s |
| [210](210.md) | &#9654; [*23*] | medium | verified | 1m13s |
| [211](211.md) |  [*M20*] | math-medium | solved | 3m58s |
| [212](212.md) | &#9654; [*25*] | medium | verified | 2m48s |
| [213](213.md) |  [*16*] | medium | verified | 1m |
| [214](214.md) | &#9654; [*21*] | medium | solved | 4m21s |
| [215](215.md) |  [*21*] | medium | solved | 4m44s |
| [216](216.md) | &#9654; [*30*] | hard | solved | 4m33s |
| [217](217.md) |  [*29*] | hard | solved | 4m07s |
| [218](218.md) | &#9654; [*24*] | medium | verified | 1m23s |
| [219](219.md) |  [*20*] | medium | verified | 3m33s |
| [220](220.md) | &#9654; [*21*] | medium | solved | 1m08s |
| [221](221.md) | &#9654; [*M27*] | math-hard | verified | 1m23s |
| [222](222.md) | &#9654; [*27*] | hard | verified | 4m14s |
| [223](223.md) |  [*28*] | hard | solved | 2m03s |
| [224](224.md) | &#9654; [*20*] | medium | solved | 3m04s |
| [225](225.md) | &#9654; [*30*] | hard | verified | 1m31s |
| [226](226.md) | &#9654; [*20*] | medium | solved | 4m |
| [227](227.md) |  [*20*] | medium | verified | 2m30s |
| [228](228.md) |  [*21*] | medium | solved | 3m29s |
| [229](229.md) |  [*15*] | simple | solved | 57s |
| [230](230.md) |  [*25*] | medium | solved | 1m51s |
| [231](231.md) |  [*23*] | medium | solved | 4m08s |
| [232](232.md) | &#9654; [*23*] | medium | solved | 4m43s |
| [233](233.md) | &#9654; [*25*] | medium | solved | 2m04s |
| [234](234.md) |  [*22*] | medium | solved | 1m31s |
| [235](235.md) |  [*22*] | medium | solved | 5m02s |
| [236](236.md) | &#9654; [*M25*] | math-medium | solved | 4m36s |
| [237](237.md) |  [*25*] | medium | solved | 4m29s |
| [238](238.md) | &#9654; [*22*] | medium | solved | 1m30s |
| [239](239.md) | &#9654; [*21*] | medium | verified | 1m15s |
| [240](240.md) | &#9654; [*22*] | medium | solved | 2m12s |
| [241](241.md) | &#9654; [*28*] | hard | solved | 4m08s |
| [242](242.md) |  [*24*] | medium | solved | 3m48s |
| [243](243.md) |  [*M23*] | math-medium | solved | 4m21s |
| [244](244.md) |  [*25*] | medium | verified | 2m36s |
| [245](245.md) | &#9654; [*M22*] | math-medium | solved | 4m09s |
| [246](246.md) |  [*M21*] | math-medium | verified | 2m32s |
| [247](247.md) | &#9654; [*M27*] | math-hard | solved | 2m14s |
| [248](248.md) |  [*M22*] | math-medium | solved | 3m44s |
| [249](249.md) |  [*HM31*] | hm-hard | solved | 3m48s |
| [250](250.md) |  [*28*] | hard | solved | 4m03s |
| [251](251.md) |  [*M46*] | math-research | verified | 2m58s |
| [252](252.md) |  [*M30*] | math-hard | solved | 4m03s |
| [253](253.md) | &#9654; [*M26*] | math-hard | verified | 2m05s |
| [254](254.md) | &#9654; [*M23*] | math-medium | solved | 2m26s |
| [255](255.md) | &#9654; [*25*] | medium | verified | 1m23s |
| [256](256.md) |  [*M32*] | math-hard | solved | 4m52s |
| [257](257.md) |  [*40*] | project | verified | 4m48s |
| [258](258.md) | &#9654; [*25*] | medium | verified | 4m22s |
| [259](259.md) | &#9654; [*25*] | medium | solved | 1m54s |
| [260](260.md) | &#9654; [*M27*] | math-hard | solved | 4m39s |
| [261](261.md) |  [*HM21*] | hm-medium | verified | 1m09s |
| [262](262.md) |  [*M26*] | math-hard | solved | 4m20s |
| [263](263.md) |  [*HM25*] | hm-medium | solved | 4m30s |
| [264](264.md) |  [*M46*] | math-research | solved | 3m53s |
| [265](265.md) | &#9654; [*21*] | medium | verified | 2m39s |
| 266 | &#9654; [*20*] | medium | - | - |
| 267 |  [*HM32*] | hm-hard | - | - |
