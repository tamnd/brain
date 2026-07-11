---
title: "TAOCP 7.2.2.2: Satisfiability"
description: "Section 7.2.2.2 exercises: 432/522 solved."
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

Exercises from [TAOCP Volume 4](../) Section 7.2.2.2: 432/522 solved.

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
| [15](15.md) |  [*24*] | medium | solved | 1m36s |
| [16](16.md) |  [*21*] | medium | solved | 2m20s |
| [17](17.md) |  [*26*] | hard | solved | 2m34s |
| [18](18.md) | &#9654; [*28*] | hard | solved | 4m15s |
| [19](19.md) | &#9654; [*29*] | hard | solved | 2m15s |
| [20](20.md) |  [*40*] | project | solved | 5m34s |
| [21](21.md) |  [*22*] | medium | solved | 4m21s |
| 22 |  [*20*] | medium | - | - |
| [23](23.md) |  [*20*] | medium | solved | 2m24s |
| [24](24.md) | &#9654; [*M32*] | math-hard | solved | 3m07s |
| 25 |  [*21*] | medium | - | - |
| [26](26.md) |  [*22*] | medium | verified | 3m35s |
| [27](27.md) |  [*20*] | medium | solved | 3m27s |
| [28](28.md) | &#9654; [*20*] | medium | verified | 2m03s |
| [29](29.md) | &#9654; [*20*] | medium | solved | 5m44s |
| [30](30.md) | &#9654; [*22*] | medium | solved | 2m40s |
| 31 |  [*28*] | hard | - | - |
| [32](32.md) |  [*15*] | simple | solved | 12m25s |
| [33](33.md) |  [*21*] | medium | solved | 5m47s |
| [34](34.md) |  [*HM26*] | hm-hard | verified | 3m49s |
| [37](37.md) |  [*20*] | medium | solved | 10m29s |
| [38](38.md) |  [*M25*] | math-medium | solved | 12m37s |
| [39](39.md) |  [*M46*] | math-research | solved | 6m30s |
| [40](40.md) |  [*01*] | simple | solved | 3m50s |
| [41](41.md) |  [*M31*] | math-hard | solved | 3m51s |
| [42](42.md) |  [*21*] | medium | solved | 3m47s |
| [43](43.md) | &#9654; [*21*] | medium | solved | 3m51s |
| [44](44.md) | &#9654; [*30*] | hard | solved | 10m13s |
| [45](45.md) |  [*20*] | medium | verified | 14m08s |
| [46](46.md) |  [*30*] | hard | solved | 11m46s |
| [47](47.md) |  [*30*] | hard | solved | 3m37s |
| [48](48.md) |  [*20*] | medium | solved | 5m49s |
| [49](49.md) |  [*21*] | medium | solved | 11m36s |
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
| [144](144.md) |  [*15*] | simple | solved | 2m09s |
| [145](145.md) |  [*23*] | medium | solved | 3m28s |
| [146](146.md) |  [*25*] | medium | verified | 1m44s |
| [147](147.md) |  [*05*] | simple | verified | 1m46s |
| [148](148.md) |  [*21*] | medium | verified | 1m26s |
| [149](149.md) | &#9654; [*26*] | hard | verified | 1m39s |
| [150](150.md) |  [*21*] | medium | verified | 5m52s |
| [151](151.md) | &#9654; [*26*] | hard | solved | 5m14s |
| [152](152.md) |  [*22*] | medium | solved | 3m28s |
| [153](153.md) |  [*17*] | medium | solved | 2m21s |
| [154](154.md) |  [*20*] | medium | verified | 1m47s |
| [155](155.md) |  [*32*] | hard | solved | 2m08s |
| [156](156.md) |  [*05*] | simple | verified | 1m14s |
| [157](157.md) |  [*10*] | simple | solved | 1m57s |
| [158](158.md) |  [*15*] | simple | solved | 2m23s |
| [159](159.md) |  [*M17*] | math-medium | verified | 1m29s |
| [160](160.md) |  [*18*] | medium | verified | 1m33s |
| [161](161.md) | &#9654; [*21*] | medium | solved | 2m48s |
| [162](162.md) |  [*21*] | medium | verified | 1m43s |
| [163](163.md) |  [*M25*] | math-medium | solved | 2m37s |
| [164](164.md) |  [*M30*] | math-hard | solved | 2m06s |
| [165](165.md) | &#9654; [*26*] | hard | verified | 1m46s |
| [166](166.md) |  [*30*] | hard | solved | 1m04s |
| [167](167.md) | &#9654; [*21*] | medium | solved | 1m44s |
| [168](168.md) |  [*26*] | hard | verified | 49s |
| [169](169.md) | &#9654; [*HM30*] | hm-hard | solved | 2m57s |
| [170](170.md) |  [*25*] | medium | solved | 3m17s |
| [171](171.md) |  [*20*] | medium | solved | 8m46s |
| [172](172.md) |  [*21*] | medium | solved | 2m45s |
| [173](173.md) |  [*40*] | project | solved | 3m28s |
| [174](174.md) |  [*15*] | simple | verified | 1m13s |
| [175](175.md) |  [*32*] | hard | solved | 31s |
| [176](176.md) |  [*M25*] | math-medium | solved | 3m45s |
| [177](177.md) |  [*HM26*] | hm-hard | solved | 3m51s |
| [178](178.md) | &#9654; [*M23*] | math-medium | solved | 2m58s |
| [179](179.md) |  [*25*] | medium | verified | 2m21s |
| [180](180.md) | &#9654; [*25*] | medium | solved | 36s |
| [181](181.md) | &#9654; [*25*] | medium | verified | 2m40s |
| [182](182.md) |  [*M16*] | math-medium | solved | 5m07s |
| [183](183.md) |  [*M30*] | math-hard | solved | 4m17s |
| [184](184.md) |  [*M20*] | math-medium | solved | 4m38s |
| [185](185.md) |  [*M20*] | math-medium | solved | 5m55s |
| [186](186.md) |  [*M21*] | math-medium | solved | 1m47s |
| [187](187.md) |  [*M20*] | math-medium | verified | 7m01s |
| [188](188.md) |  [*HM25*] | hm-medium | solved | 6m11s |
| [189](189.md) |  [*27*] | hard | solved | 2m16s |
| [190](190.md) |  [*M20*] | math-medium | verified | 1m14s |
| [191](191.md) |  [*M25*] | math-medium | solved | 6m51s |
| [192](192.md) | &#9654; [*HM21*] | hm-medium | solved | 3m36s |
| [193](193.md) |  [*HM48*] | hm-research | solved | 2m04s |
| [194](194.md) |  [*HM19*] | hm-medium | verified | 1m30s |
| [195](195.md) |  [*HM21*] | hm-medium | verified | 1m33s |
| [196](196.md) | &#9654; [*HM25*] | hm-medium | solved | 2m24s |
| [197](197.md) |  [*HM21*] | hm-medium | verified | 2m54s |
| [198](198.md) | &#9654; [*HM30*] | hm-hard | solved | 3m21s |
| [199](199.md) |  [*M21*] | math-medium | verified | 2m26s |
| [200](200.md) | &#9654; [*M21*] | math-medium | solved | 2m24s |
| [201](201.md) |  [*HM29*] | hm-hard | solved | 2m29s |
| [202](202.md) |  [*HM21*] | hm-medium | solved | 4m43s |
| [203](203.md) |  [*HM93*] | hm-research | solved | 2m13s |
| [204](204.md) | &#9654; [*28*] | hard | solved | 6m06s |
| [205](205.md) |  [*26*] | hard | verified | 2m48s |
| [206](206.md) |  [*M22*] | math-medium | solved | 1m32s |
| [207](207.md) |  [*22*] | medium | solved | 10m |
| [208](208.md) |  [*25*] | medium | solved | 7m45s |
| [209](209.md) |  [*25*] | medium | solved | 4m41s |
| [210](210.md) |  [*M36*] | math-project | solved | 6m32s |
| [211](211.md) |  [*30*] | hard | solved | 4m42s |
| [212](212.md) |  [*32*] | hard | solved | 2m30s |
| [213](213.md) | &#9654; [*M26*] | math-hard | verified | 1m47s |
| [214](214.md) |  [*HM38*] | hm-project | solved | 4m37s |
| [215](215.md) | &#9654; [*HM23*] | hm-medium | verified | 3m13s |
| [216](216.md) |  [*HM38*] | hm-project | solved | 5m16s |
| [217](217.md) |  [*20*] | medium | verified | 2m36s |
| [218](218.md) |  [*20*] | medium | solved | 1m15s |
| 219 | &#9654; [*M20*] | math-medium | - | - |
| 220 |  [*M24*] | math-medium | - | - |
| 221 |  [*16*] | medium | - | - |
| 222 |  [*M30*] | math-hard | - | - |
| 223 |  [*HM40*] | hm-project | - | - |
| [224](224.md) |  [*M20*] | math-medium | solved | 1m37s |
| [225](225.md) | &#9654; [*M31*] | math-hard | solved | 3m17s |
| [226](226.md) |  [*M30*] | math-hard | verified | 2m10s |
| [227](227.md) |  [*M27*] | math-hard | solved | 4m14s |
| [228](228.md) | &#9654; [*M21*] | math-medium | solved | 5m29s |
| [229](229.md) |  [*M21*] | math-medium | solved | 6m36s |
| [230](230.md) |  [*M22*] | math-medium | solved | 5m42s |
| [231](231.md) |  [*M30*] | math-hard | solved | 5m01s |
| [232](232.md) |  [*M28*] | math-hard | solved | 4m29s |
| [233](233.md) |  [*16*] | medium | verified | 2m55s |
| [234](234.md) |  [*20*] | medium | solved | 1m56s |
| [235](235.md) |  [*30*] | hard | solved | 4m58s |
| [236](236.md) |  [*8*] | simple | solved | 2m50s |
| [237](237.md) |  [*28*] | hard | solved | 1m59s |
| [238](238.md) |  [*HM21*] | hm-medium | solved | 1m51s |
| [239](239.md) | &#9654; [*M21*] | math-medium | solved | 2m35s |
| [240](240.md) |  [*HM23*] | hm-medium | solved | 3m29s |
| [241](241.md) |  [*20*] | medium | verified | 6m09s |
| [242](242.md) |  [*M20*] | math-medium | solved | 1m07s |
| [243](243.md) |  [*HM31*] | hm-hard | solved | 6m15s |
| [244](244.md) |  [*M20*] | math-medium | solved | 1m22s |
| [245](245.md) | &#9654; [*M27*] | math-hard | solved | 6m06s |
| [246](246.md) | &#9654; [*M28*] | math-hard | solved | 3m35s |
| [247](247.md) |  [*18*] | medium | solved | 4m04s |
| [248](248.md) |  [*M20*] | math-medium | solved | 2m06s |
| [249](249.md) |  [*18*] | medium | solved | 1m17s |
| [250](250.md) |  [**] |  | solved | 1m17s |
| [251](251.md) | &#9654; [*30*] | hard | solved | 2m39s |
| [252](252.md) |  [*M26*] | math-hard | solved | 1m31s |
| [253](253.md) | &#9654; [*18*] | medium | solved | 6m50s |
| [254](254.md) |  [*16*] | medium | solved | 1m42s |
| [255](255.md) | &#9654; [*20*] | medium | solved | 3m12s |
| [256](256.md) |  [*20*] | medium | solved | 9m15s |
| [257](257.md) | &#9654; [*30*] | hard | verified | 4m43s |
| [258](258.md) |  [*21*] | medium | solved | 3m51s |
| [259](259.md) |  [*M20*] | math-medium | solved | 3m39s |
| [260](260.md) |  [*21*] | medium | solved | 3m |
| [261](261.md) |  [*21*] | medium | verified | 7m |
| [262](262.md) |  [*20*] | medium | solved | 4m17s |
| [263](263.md) |  [*21*] | medium | solved | 3m56s |
| [264](264.md) |  [*20*] | medium | solved | 2m50s |
| [265](265.md) |  [*21*] | medium | solved | 4m23s |
| [266](266.md) |  [*20*] | medium | solved | 2m56s |
| [267](267.md) |  [*25*] | medium | solved | 4m22s |
| [268](268.md) |  [*21*] | medium | solved | 3m10s |
| [269](269.md) |  [*29*] | hard | solved | 6m47s |
| [270](270.md) |  [*25*] | medium | solved | 10m53s |
| [271](271.md) | &#9654; [*25*] | medium | solved | 4m23s |
| [272](272.md) |  [*30*] | hard | solved | 7m21s |
| [273](273.md) |  [*27*] | hard | solved | 1m48s |
| [274](274.md) |  [*35*] | hard | verified | 3m20s |
| [275](275.md) | &#9654; [*22*] | medium | solved | 2m01s |
| [276](276.md) |  [*M15*] | math-simple | verified | 1m56s |
| [277](277.md) |  [*M18*] | math-medium | solved | 1m50s |
| [278](278.md) |  [*22*] | medium | solved | 11m54s |
| [279](279.md) |  [*M20*] | math-medium | verified | 12m23s |
| [280](280.md) | &#9654; [*M26*] | math-hard | solved | 5m23s |
| [281](281.md) |  [*21*] | medium | solved | 5m42s |
| [282](282.md) | &#9654; [*M33*] | math-hard | solved | 3m13s |
| [283](283.md) |  [*HM46*] | hm-research | solved | 2m09s |
| [284](284.md) |  [*23*] | medium | solved | 2m19s |
| [285](285.md) |  [*19*] | medium | solved | 2m17s |
| [286](286.md) |  [*M24*] | math-medium | solved | 6m37s |
| [287](287.md) |  [*25*] | medium | solved | 2m35s |
| [288](288.md) |  [*28*] | hard | solved | 5m44s |
| [289](289.md) |  [*M20*] | math-medium | solved | 5m50s |
| [290](290.md) |  [*17*] | medium | solved | 5m43s |
| [291](291.md) |  [*20*] | medium | solved | 4m45s |
| [292](292.md) |  [*M21*] | math-medium | solved | 2m48s |
| [293](293.md) |  [*21*] | medium | solved | 3m07s |
| [294](294.md) |  [*HM21*] | hm-medium | solved | 3m46s |
| [295](295.md) |  [*M23*] | math-medium | solved | 3m46s |
| [296](296.md) |  [*HM20*] | hm-medium | solved | 3m49s |
| [297](297.md) | &#9654; [*HM26*] | hm-hard | solved | 3m45s |
| [298](298.md) |  [*HM22*] | hm-medium | solved | 3m54s |
| [299](299.md) |  [*HM23*] | hm-medium | solved | 5m30s |
| [300](300.md) | &#9654; [*25*] | medium | solved | 10m10s |
| [301](301.md) | &#9654; [*25*] | medium | solved | 11m26s |
| [302](302.md) |  [*26*] | hard | solved | 4m27s |
| [303](303.md) |  [*HM20*] | hm-medium | solved | 3m50s |
| [304](304.md) |  [*HM34*] | hm-hard | solved | 3m43s |
| [305](305.md) | &#9654; [*M25*] | math-medium | solved | 4m46s |
| [306](306.md) | &#9654; [*HM32*] | hm-hard | solved | 3m47s |
| [307](307.md) |  [*HM28*] | hm-hard | solved | 10m20s |
| [308](308.md) |  [*M29*] | math-hard | solved | 10m44s |
| [309](309.md) |  [*20*] | medium | solved | 9m33s |
| [310](310.md) |  [*M25*] | math-medium | verified | 9m18s |
| [311](311.md) |  [*21*] | medium | solved | 7m03s |
| [312](312.md) |  [*HM24*] | hm-medium | solved | 4m55s |
| [313](313.md) | &#9654; [*22*] | medium | solved | 5m54s |
| [314](314.md) |  [*36*] | project | solved | 4m52s |
| [315](315.md) |  [*M18*] | math-medium | verified | 4m03s |
| [316](316.md) |  [*HM20*] | hm-medium | solved | 3m36s |
| [317](317.md) | &#9654; [*M26*] | math-hard | verified | 9m05s |
| [318](318.md) |  [*HM27*] | hm-hard | verified | 9m06s |
| [319](319.md) |  [*HM20*] | hm-medium | solved | 5m30s |
| [320](320.md) |  [*HM24*] | hm-medium | verified | 4m56s |
| [321](321.md) |  [*M24*] | math-medium | solved | 4m47s |
| [322](322.md) | &#9654; [*HM35*] | hm-hard | solved | 5m39s |
| [323](323.md) |  [*10*] | simple | solved | 4m51s |
| [324](324.md) | &#9654; [*22*] | medium | solved | 5m09s |
| [325](325.md) |  [*20*] | medium | solved | 5m41s |
| [326](326.md) |  [*20*] | medium | solved | 5m39s |
| [327](327.md) |  [*22*] | medium | solved | 5m38s |
| [328](328.md) |  [*20*] | medium | solved | 5m44s |
| [329](329.md) |  [*21*] | medium | solved | 5m43s |
| [330](330.md) | &#9654; [*21*] | medium | solved | 5m47s |
| [331](331.md) |  [*M20*] | math-medium | solved | 5m45s |
| [332](332.md) |  [*20*] | medium | solved | 5m48s |
| [333](333.md) | &#9654; [*M20*] | math-medium | solved | 4m37s |
| 334 |  [*25*] | medium | - | - |
| [335](335.md) |  [*HM26*] | hm-hard | solved | 5m43s |
| [336](336.md) | &#9654; [*M20*] | math-medium | solved | 12m21s |
| [337](337.md) |  [*M20*] | math-medium | solved | 13m17s |
| [338](338.md) |  [*M21*] | math-medium | solved | 13m20s |
| [339](339.md) | &#9654; [*HM26*] | hm-hard | verified | 10m01s |
| [340](340.md) | &#9654; [*M20*] | math-medium | verified | 3m49s |
| [341](341.md) |  [*M25*] | math-medium | verified | 3m48s |
| [342](342.md) |  [*HM25*] | hm-medium | verified | 3m47s |
| [343](343.md) | &#9654; [*M25*] | math-medium | verified | 3m47s |
| [344](344.md) |  [*M33*] | math-hard | verified | 3m43s |
| [345](345.md) |  [*M30*] | math-hard | verified | 3m50s |
| [346](346.md) | &#9654; [*HM28*] | hm-hard | verified | 3m49s |
| [347](347.md) | &#9654; [*M28*] | math-hard | verified | 3m49s |
| [348](348.md) |  [*HM26*] | hm-hard | verified | 3m49s |
| [349](349.md) | &#9654; [*M24*] | math-medium | verified | 3m51s |
| [350](350.md) | &#9654; [*HM26*] | hm-hard | verified | 3m52s |
| [351](351.md) |  [*25*] | medium | verified | 3m46s |
| [352](352.md) |  [*M21*] | math-medium | verified | 3m48s |
| [353](353.md) |  [*M21*] | math-medium | verified | 3m49s |
| [354](354.md) |  [*HM20*] | hm-medium | verified | 3m49s |
| [355](355.md) |  [*HM21*] | hm-medium | verified | 3m46s |
| [356](356.md) | &#9654; [*M35*] | math-hard | verified | 3m46s |
| [357](357.md) | &#9654; [*M20*] | math-medium | verified | 3m51s |
| [358](358.md) |  [*M20*] | math-medium | verified | 3m49s |
| [359](359.md) |  [*20*] | medium | verified | 3m46s |
| [360](360.md) |  [*M23*] | math-medium | verified | 3m49s |
| [361](361.md) | &#9654; [*M25*] | math-medium | verified | 3m50s |
| [362](362.md) |  [*20*] | medium | verified | 3m49s |
| [363](363.md) | &#9654; [*M30*] | math-hard | verified | 3m50s |
| [364](364.md) | &#9654; [*M21*] | math-medium | verified | 3m58s |
| [365](365.md) |  [*M37*] | math-project | verified | 3m50s |
| [366](366.md) | &#9654; [*18*] | medium | verified | 3m50s |
| [367](367.md) | &#9654; [*20*] | medium | verified | 3m51s |
| [368](368.md) |  [*76*] | research | verified | 3m51s |
| [369](369.md) | &#9654; [**] |  | verified | 5m14s |
| [370](370.md) |  [*20*] | medium | solved | 3m57s |
| [371](371.md) |  [*24*] | medium | solved | 3m48s |
| [372](372.md) |  [*25*] | medium | solved | 3m49s |
| [373](373.md) |  [*35*] | hard | solved | 5m51s |
| [374](374.md) | &#9654; [*32*] | hard | solved | 3m52s |
| [375](375.md) |  [*21*] | medium | solved | 3m47s |
| [376](376.md) | &#9654; [*32*] | hard | solved | 3m48s |
| [377](377.md) |  [*22*] | medium | solved | 3m42s |
| [378](378.md) |  [*39*] | project | solved | 3m46s |
| [379](379.md) | &#9654; [*20*] | medium | solved | 10m33s |
| [380](380.md) |  [*21*] | medium | solved | 5m42s |
| [381](381.md) |  [*22*] | medium | solved | 5m03s |
| [382](382.md) |  [*30*] | hard | solved | 5m55s |
| [383](383.md) | &#9654; [*23*] | medium | solved | 7m59s |
| [384](384.md) |  [*25*] | medium | solved | 10m51s |
| [385](385.md) |  [**] |  | solved | 9m20s |
| [386](386.md) | &#9654; [*M25*] | math-medium | solved | 8m52s |
| [387](387.md) |  [*21*] | medium | solved | 5m06s |
| [388](388.md) |  [*20*] | medium | solved | 5m |
| [389](389.md) |  [*22*] | medium | solved | 13m48s |
| [390](390.md) |  [*23*] | medium | solved | 6m29s |
| [391](391.md) |  [*M25*] | math-medium | solved | 3m48s |
| [392](392.md) |  [*22*] | medium | solved | 3m24s |
| [393](393.md) |  [*25*] | medium | solved | 5m16s |
| [394](394.md) |  [*25*] | medium | solved | 3m45s |
| [395](395.md) |  [*20*] | medium | solved | 3m45s |
| [396](396.md) | &#9654; [*23*] | medium | solved | 3m48s |
| [397](397.md) |  [*22*] | medium | solved | 3m51s |
| [398](398.md) |  [*18*] | medium | solved | 3m53s |
| [399](399.md) |  [*23*] | medium | solved | 3m48s |
| [400](400.md) |  [*25*] | medium | solved | 3m49s |
| [401](401.md) |  [*16*] | medium | solved | 3m50s |
| [402](402.md) |  [*18*] | medium | solved | 3m47s |
| [403](403.md) |  [*20*] | medium | solved | 3m48s |
| [404](404.md) | &#9654; [*21*] | medium | solved | 3m59s |
| [405](405.md) | &#9654; [*M25*] | math-medium | solved | 3m48s |
| [406](406.md) |  [*M24*] | math-medium | solved | 3m51s |
| [407](407.md) |  [*M22*] | math-medium | solved | 3m46s |
| [408](408.md) | &#9654; [*25*] | medium | solved | 3m47s |
| [409](409.md) | &#9654; [*M26*] | math-hard | solved | 3m48s |
| [410](410.md) |  [*24*] | medium | solved | 3m50s |
| [411](411.md) |  [*25*] | medium | solved | 3m49s |
| [412](412.md) |  [*40*] | project | solved | 4m45s |
| [413](413.md) |  [*M23*] | math-medium | solved | 2m48s |
| [414](414.md) |  [*M20*] | math-medium | solved | 3m53s |
| [415](415.md) |  [*M22*] | math-medium | solved | 3m50s |
| [416](416.md) |  [*20*] | medium | solved | 3m48s |
| [417](417.md) |  [*21*] | medium | solved | 3m47s |
| [418](418.md) |  [*23*] | medium | solved | 3m48s |
| [419](419.md) |  [*M21*] | math-medium | solved | 3m46s |
| [420](420.md) |  [*18*] | medium | solved | 3m47s |
| [421](421.md) |  [*18*] | medium | solved | 3m47s |
| [422](422.md) |  [*11*] | simple | solved | 3m46s |
| [423](423.md) |  [*22*] | medium | solved | 3m45s |
| [424](424.md) | &#9654; [*20*] | medium | solved | 3m49s |
| [425](425.md) |  [*18*] | medium | solved | 10m32s |
| [426](426.md) | &#9654; [*M20*] | math-medium | solved | 11m35s |
| [427](427.md) |  [*M30*] | math-hard | solved | 9m16s |
| [428](428.md) |  [*M27*] | math-hard | solved | 3m46s |
| [429](429.md) |  [*22*] | medium | solved | 3m48s |
| [430](430.md) |  [*25*] | medium | solved | 3m51s |
| [431](431.md) | &#9654; [*20*] | medium | solved | 3m50s |
| [432](432.md) |  [*34*] | hard | solved | 3m45s |
| [433](433.md) |  [*25*] | medium | solved | 3m52s |
| [434](434.md) |  [*21*] | medium | solved | 3m46s |
| [435](435.md) | &#9654; [*28*] | hard | solved | 2m40s |
| [436](436.md) |  [*M32*] | math-hard | solved | 9m35s |
| [437](437.md) |  [*M21*] | math-medium | solved | 8m16s |
| [438](438.md) |  [*21*] | medium | verified | 6m53s |
| [439](439.md) |  [*20*] | medium | solved | 7m50s |
| [440](440.md) |  [*M33*] | math-hard | verified | 7m32s |
| [441](441.md) |  [*M35*] | math-hard | solved | 6m21s |
| [442](442.md) | &#9654; [*M27*] | math-hard | solved | 7m24s |
| [443](443.md) |  [**] |  | solved | 3m10s |
| [444](444.md) |  [*M26*] | math-hard | solved | 3m24s |
| [445](445.md) | &#9654; [*22*] | medium | solved | 8m33s |
| [446](446.md) |  [*M10*] | math-simple | solved | 8m32s |
| [447](447.md) | &#9654; [*22*] | medium | solved | 5m25s |
| [448](448.md) |  [*M23*] | math-medium | solved | 2m53s |
| [449](449.md) |  [*21*] | medium | solved | 5m32s |
| [450](450.md) |  [*25*] | medium | solved | 9m03s |
| [451](451.md) | &#9654; [*28*] | hard | verified | 24m22s |
| [452](452.md) |  [*34*] | hard | solved | 4m33s |
| [453](453.md) |  [*M23*] | math-medium | solved | 5m03s |
| [454](454.md) |  [*15*] | simple | solved | 4m34s |
| [455](455.md) |  [*M20*] | math-medium | verified | 6m26s |
| [456](456.md) |  [*M21*] | math-medium | solved | 4m52s |
| [457](457.md) |  [*HM19*] | hm-medium | solved | 4m54s |
| [458](458.md) |  [*20*] | medium | solved | 4m54s |
| [459](459.md) | &#9654; [*20*] | medium | solved | 3m50s |
| [460](460.md) |  [*21*] | medium | solved | 4m05s |
| [461](461.md) |  [*20*] | medium | solved | 5m13s |
| [462](462.md) |  [*22*] | medium | solved | 4m53s |
| [463](463.md) | &#9654; [*M21*] | math-medium | solved | 11m33s |
| [464](464.md) | &#9654; [*M25*] | math-medium | solved | 4m11s |
| [465](465.md) |  [*M21*] | math-medium | solved | 4m57s |
| [466](466.md) |  [*M23*] | math-medium | solved | 15m58s |
| [467](467.md) |  [*20*] | medium | solved | 10m15s |
| [468](468.md) |  [*20*] | medium | solved | 4m |
| [469](469.md) | &#9654; [**] |  | solved | 5m53s |
| [470](470.md) | &#9654; [**] |  | solved | 4m59s |
| [471](471.md) |  [*16*] | medium | solved | 5m40s |
| [472](472.md) |  [**] |  | solved | 5m42s |
| [473](473.md) | &#9654; [**] |  | solved | 12m01s |
| [474](474.md) |  [**] |  | solved | 13m29s |
| [475](475.md) |  [**] |  | solved | 4m43s |
| [476](476.md) |  [**] |  | solved | 5m46s |
| [477](477.md) | &#9654; [*23*] | medium | solved | 4m58s |
| [478](478.md) | &#9654; [*23*] | medium | solved | 5m51s |
| [479](479.md) | &#9654; [*25*] | medium | solved | 5m08s |
| [480](480.md) |  [*25*] | medium | solved | 5m10s |
| [481](481.md) | &#9654; [*28*] | hard | solved | 5m47s |
| [482](482.md) | &#9654; [*26*] | hard | verified | 4m51s |
| [483](483.md) |  [*21*] | medium | solved | 4m26s |
| [484](484.md) |  [*22*] | medium | solved | 3m39s |
| [485](485.md) | &#9654; [*23*] | medium | solved | 3m50s |
| [486](486.md) |  [*21*] | medium | solved | 3m55s |
| [487](487.md) | &#9654; [*27*] | hard | solved | 6m15s |
| [488](488.md) |  [*24*] | medium | solved | 7m18s |
| [489](489.md) |  [*M21*] | math-medium | solved | 10m40s |
| [490](490.md) |  [*15*] | simple | solved | 11m34s |
| [491](491.md) |  [*22*] | medium | solved | 11m41s |
| [492](492.md) |  [*M20*] | math-medium | solved | 11m32s |
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
