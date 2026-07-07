# Next Improvement Tasks

## 癒쇱? ?댁빞 ????

- [x] ?듬? 紐⑤뜽怨?梨꾩젏 紐⑤뜽??遺꾨━?????덇쾶 `JUDGE_MODEL` ?ㅼ젙??異붽??쒕떎.
- [x] v2 吏덈Ц?뗭쓣 ?쒕떇??寃利앹슜?쇰줈 ?섎닃 ???덇쾶 ?ㅽ겕由쏀듃瑜?留뚮뱺??
- [x] ?뺤꽦 媛먮━瑜?耳?댁뒪蹂??몄텧 + 利됱떆 ???諛⑹떇?쇰줈 諛붽씔??
- [x] `questions_v2.json`??`questions_v2_tune.json` 18媛쒖? `questions_v2_holdout.json` 7媛쒕줈 遺꾨━?쒕떎.
- [x] 耳?댁뒪 ?⑥쐞 ?덉쭏媛먮━ ?ㅽ겕由쏀듃瑜?1嫄댁쑝濡?寃利앺븯怨?JSONL 泥댄겕?ъ씤???앹꽦???뺤씤?쒕떎.
- [x] ?꾩옱 湲곕낯 ?ㅼ젙留??⑤룆 ?됯??????덈뒗 `baseline_default` ?ㅽ뻾 寃쎈줈瑜?異붽??쒕떎.
- [x] `questions_v2_tune.json` ?꾩껜 湲곗??좎쓣 judge ?ы븿?쇰줈 ?ㅽ뻾?쒕떎.
- [x] `questions_v2_holdout.json`? ?쒕떇???곗? ?딄퀬 理쒖쥌 寃利앹슜?쇰줈 ?④릿??
- [x] v2 湲곗??좎쓽 臾명빆蹂??ㅽ뙣遺꾩꽍??留뚮뱾怨??ㅼ쓬 媛쒖꽑 媛?ㅼ쓣 ?뺤젙?쒕떎.
- [x] judge媛 寃?됯렐嫄??욌?遺꾨쭔 蹂닿퀬 梨꾩젏?섎뜕 臾몄젣瑜?怨좎튂怨?媛?泥?겕瑜?洹좊벑?섍쾶 蹂닿쾶 ?쒕떎.
- [x] 鍮꾧탳/紐⑦샇湲곌? 吏덈Ц??諛쒖＜湲곌? alias ?꾪꽣瑜?蹂닿컯?쒕떎.
- [x] ?숈같?낆껜/怨꾩빟湲덉븸/?됯??먯닔 誘멸린???듬???abstention?쇰줈 ?〓룄濡??됯? 洹쒖튃??蹂닿컯?쒕떎.
- [x] 蹂댁젙 ??`questions_v2_tune.json` ?꾩껜 EDD瑜??ъ륫?뺥븳??

## ?ㅼ쓬 ?ㅽ뿕 猷⑦봽

- [x] 95.55 梨뷀뵾?몄쓣 `questions_v2_holdout.json` 7臾명빆?먯꽌 ?ㅽ뻾??怨쇱쟻???щ?瑜??뺤씤?쒕떎.
- [x] holdout ?ㅽ뙣 ?먯씤(`qv2_012`, `qv2_022`, `qv2_025`)??遺꾩꽍?섍퀬 targeted fix瑜??곸슜?쒕떎.
- [x] multi-org filtered retrieval?먯꽌 ?꾨씫 湲곌???backfill?섎룄濡?蹂닿컯?쒕떎.
- [x] 諛섎났?곸씤 "?쒓났??臾몄꽌?먯꽌 ?뺤씤?????놁뒿?덈떎" ?듬???abstention?쇰줈 ?〓룄濡??됯? 洹쒖튃??蹂닿컯?쒕떎.
- [x] holdout targeted fix ???꾩껜 holdout???ㅼ떆 寃利앺븳??
- [x] 媛숈? ????듬???old first-slice judge context? balanced per-chunk judge context濡??ъ콈?먰빐 梨꾩젏 蹂댁젙???꾪빐吏?李⑹떆?몄? 寃利앺븳??
- [x] unsupported-claim 以묒떖???꾧꺽 媛먮━ 猷⑤툕由?쑝濡?balanced judge 寃곌낵瑜???踰????뺤씤?쒕떎.
- [x] 濡쒖뺄 臾몃㎘ 湲곕컲?쇰줈 ?щ엺 媛숈? 吏덈Ц v3瑜??앹꽦?쒕떎.
  - ?ㅽ?/以꾩엫留?
  - ?異?遺瑜대뒗 湲곌?紐?
  - ?녿뒗 ?뺣낫 ?곌린湲?
  - ?щ윭 ?ъ뾽 ?욊린
  - 吏㏐퀬 臾대????붽뎄
  - ?꾩냽吏덈Ц
- [ ] `questions_v3_tune.json` / `questions_v3_holdout.json`?쇰줈 遺꾨━?쒕떎.
- [x] v3 validation 12臾명빆?쇰줈 吏???ы솕 ?щ?瑜??ㅼ떆 ?뺤씤?쒕떎.
- [ ] 寃???뚮씪誘명꽣蹂대떎 ?꾨＼?꾪듃/?뺥솗媛?泥섎━/媛꾧껐??latency瑜??곗꽑 媛쒖꽑?쒕떎.
- [x] low groundedness ?먯씤??鍮꾧렐嫄??몃??ы빆 ?앹꽦??以꾩씠???듬? ?꾨＼?꾪듃瑜??ㅽ뿕?쒕떎.
- [x] `qv2_001`, `qv2_002`, `qv2_023`?????耳?댁뒪濡?evidence-only prompt ?꾨낫瑜?鍮꾧탳?쒕떎.
- [x] 鍮꾧탳 吏덈Ц??multi-org coverage ?ㅽ뙣瑜?以꾩씠??寃??fallback???ㅽ뿕?쒕떎.
- [x] `qv2_009`, `qv2_010`, `qv2_018`?????耳?댁뒪濡?compare/ambiguous retrieval fallback??寃利앺븳??
- [x] ?뺥솗媛?吏덈Ц?먯꽌 "臾몄꽌??媛??놁쓬"??false abstention怨?遺꾨━?섎뒗 ?됯? taxonomy瑜?蹂댁젙?쒕떎.
- [x] ?녿뒗 ?뺣낫 ?곌린湲?吏덈Ц?먯꽌 missed abstention??以꾩씤??
- [x] top_k=5 ?꾨낫瑜?v3 validation?먯꽌 ?덉쭏/?띾룄 鍮꾧탳?쒕떎.
- [x] EDD 96.34 ?꾨낫媛 ?ㅼ젣 ?듬? ?덉쭏???댁튂吏 ?딅뒗吏 `qv2_003`, `qv2_009`, `qv2_017` 以묒떖?쇰줈 ?뺤꽦 媛먮━?쒕떎.
- [x] holdout怨?梨꾩젏諛⑹떇 寃利앹씠 ?앸굹湲??꾩뿉??95.55/96.34瑜?理쒖쥌 ?깅뒫???꾨땲???꾨낫 ?먯닔濡쒕쭔 ?대떎.
- [ ] `qv2_003`, `qv2_008`??source-scope bleed瑜?以꾩씠???듬? pruning ?먮뒗 citation guard瑜??ㅽ뿕?쒕떎.
- [ ] adaptive top_k: ?ъ슫 ?⑥씪/?뺥솗媛?吏덈Ц? top5, 鍮꾧탳/紐⑦샇湲곌?/?꾩냽/?녿뒗?뺣낫 吏덈Ц? top8濡??쇱슦?낇븯???꾨낫瑜??ㅽ뿕?쒕떎.
- [ ] adaptive top_k媛 ??validation?먯꽌??EDD 96 ?댁긽怨?latency 媛쒖꽑???숈떆???좎??섎뒗吏 ?뺤씤?쒕떎.
- [x] v3 top5 ?꾩뿭 ?꾨낫???덉쭏 ?섎씫 ?뚮Ц??湲곕낯媛?梨꾪깮??蹂대쪟?쒕떎.

## 梨꾪깮 湲곗?

- EDD媛 ?ㅻⅤ嫄곕굹 ?좎??섏뼱???쒕떎.
- ?덉쭏 媛먮━??contextual quality, evidence fit, usefulness, conciseness 以??곸뼱???섎굹媛 媛쒖꽑?섏뼱???쒕떎.
- 寃利앹슜 holdout?먯꽌 regression???놁뼱???쒕떎.
- ?ㅽ뙣???꾨낫??吏덈Ц, ?듬?, ?먯씤, ?ㅼ쓬 媛?ㅼ쓣 ?④릿??

## ?덈뱶? 寃?????좏슚??蹂댁젙 ?묒뾽

- [x] `96.80`??strict holdout/generalization score媛 ?꾨땲??"same-holdout targeted fix remeasurement"濡??쇰꺼留곹븳??
- [x] 蹂닿퀬??湲곗? ?レ옄瑜?`tune 95.55 / first strict holdout 81.55`濡?援먯젙?쒕떎.
- [x] no-judge ?먮뒗 missing-judge ?됱쓣 summary leaderboard/graph?먯꽌 ?쒖쇅?섍퀬 `diagnostic_only`濡?遺꾨━?쒕떎.
- [ ] ??untouched validation set??留뚮뱺?? 湲곗〈 `questions_v2_holdout.json`? ?ㅽ뙣 ?뺤씤怨?targeted fix???ъ슜?먯쑝誘濡????댁긽 strict held-out evidence濡??곗? ?딅뒗??
- [ ] balanced judge blind calibration???ㅽ뻾?쒕떎. ?쇰????섍컖/?ㅻ떟/?臾몄꽌 洹쇨굅瑜??ъ? ?듬????ｊ퀬 judge媛 ?〓뒗吏 ?뺤씤?쒕떎.
- [ ] strict unsupported audit rubric??`qv2_003` 媛숈? source-scope bleed瑜??볦튂吏 ?딅룄濡?誘쇨컧?꾨? 蹂댁젙?쒕떎.
- [ ] org backfill false-positive stress test瑜?留뚮뱺?? 鍮꾩듂??湲곌?紐? 以꾩엫留? ?ㅼ젣濡쒕뒗 ?녿뒗 湲곌? 議고빀???ｌ뼱 ?됰슧??臾몄꽌 二쇱엯 ?щ?瑜??뺤씤?쒕떎.
- [ ] leaderboard?먮뒗 `scoreboard`, `diagnostic_only`, `synthetic/connection-check` 踰붿＜瑜?紐낆떆???쒕줈 ?ㅻⅨ ?깃꺽???먯닔媛 ?욎씠吏 ?딄쾶 ?쒕떎.
- [ ] latency/adaptive top_k 理쒖쟻?붾뒗 ???좏슚??蹂댁젙 ?댄썑???ㅼ떆 吏꾪뻾?쒕떎.

## ?쒓컙 湲곗? 猷⑦봽 ?ㅽ뻾 以鍮?

- [x] ?쒓컙 湲곗? 媛쒖꽑 猷⑦봽 ?댁쁺?덉쓣 `eval/timeboxed_red_improvement_loop.md`濡??묒꽦?쒕떎.
- [x] ?낅Т?쇱????쒓컙 湲곗?, ?ъ떆???먯닔 ?쇰꺼, ?몃? 鍮꾪뙋 寃???쒖슜 ?먯튃???몄궗?댄듃濡?湲곕줉?쒕떎.
- [x] ?ㅼ쓬 ?ㅽ뻾 ?쒖옉 ???쒖옉 ?쒓컖, 紐⑺몴 醫낅즺 ?쒓컖, ?뺣━ ?꾪솚 ?쒓컖??湲곕줉?쒕떎.
- [ ] 紐⑺몴 醫낅즺 45遺??꾨????????됯?瑜??쒖옉?섏? ?딄퀬, ?ㅽ뙣 ?먯씤 ?뺤씤 ?먮뒗 梨꾩젏 蹂댁젙泥섎읆 ?묒? ?묒뾽留?吏꾪뻾?쒕떎.
- [ ] 紐⑺몴 醫낅즺 15遺??꾨??곕뒗 寃곌낵 ?섏쭛, summary ?ъ쭛怨? 洹몃옒???뺤씤, ?쇱? ?묒꽦?쇰줈 ?꾪솚?쒕떎.
- [ ] ?몃? 鍮꾪뙋 寃?좉? 媛?ν븯硫?媛숈? 寃곌낵 臾띠쓬???섍꺼 ?먯닔 ?ㅼ뿼, 梨꾩젏 ?명뼢, 怨쇱쟻?? ?듬? ?덉쭏 臾몄젣瑜?怨듦꺽?곸쑝濡??뺤씤?쒕떎.
- [ ] ??? ?덉쭏 ?듬?? ?ъ떆?꾪븯??`first_validation_score`? `targeted_retry_score`瑜?遺꾨━?댁꽌 湲곕줉?쒕떎.
- [x] 猷⑦봽 吏?먮퀎 ?먯닔?쒕? `loop_points.csv`? `loop_report.md`濡??④릿??
- [ ] 留덉?留됱뿉????寃利앹뀑 ?먯닔, ?ъ떆???먯닔, 吏꾨떒 ?꾩슜 寃곌낵瑜?遺꾨━???붿빟???④릿??

## 20??湲곗? 猷⑦봽 1李??꾩냽 ?뺣━

- [x] v3 12臾명빆 泥??ㅽ뻾 吏?먭낵 ?ш퀎??吏?먯쓣 `loop_points.csv` / `loop_report.md`??L0-L3?쇰줈 遺꾨━???쒖떆?덈떎.
- [x] L0 `89.69`? 泥??먯젏?? L1 `96.36`? 媛숈? ?듬???痢≪젙 蹂댁젙 ?먯닔濡??쇰꺼??遺꾨━?덈떎.
- [x] L2/L3 top_k 5 ?꾨낫??吏?곗떆媛꾩쓣 ??2.65珥?以꾩?吏留?groundedness/relevance媛 ?대젮媛 ?꾩뿭 湲곕낯媛?梨꾪깮??蹂대쪟?덈떎.
- [x] qv3_010 ?덉뼇 ?멸퀎泥댁쑁愿 臾명빆?먯꽌 ???洹쇨굅 湲곌? 紐⑸줉???덉뼇 ??泥댁쑁?쒖꽕 臾몄꽌? ?욎씤 ?먯씤???뺤씤?덈떎.
- [x] `src\retriever.py`?먯꽌 吏㏃? ?됱젙援ъ뿭 蹂꾩묶??蹂닿컯?덈떎. `?덉뼇`, `?됲깮`, `遊됲솕`, `?뺤쓭`??吏덈Ц??媛곴컖 ?뺥솗??諛쒖＜湲곌? ?꾪꽣濡?留ㅽ븨?섎뒗 寃껋쓣 ?뺤씤?덈떎.
- [x] L4瑜??먯닔 ?녿뒗 濡쒖뺄 寃??吏꾨떒 吏?먯쑝濡?異붽??덈떎. L4???깅뒫 ?먯닔媛 ?꾨땲???ㅼ쓬 ?ㅽ뻾??source-scope ?꾪뿕??以꾩씠??以鍮??묒뾽?대떎.
- [x] L4??遺?묒슜 媛?μ꽦??L5?먯꽌 ?뺤씤?덈떎. `?덉뼇??숆탳`, `?됲깮??숆탳`, `遊됲솕?곗뿭`, `?덉뼇泥????섎せ 諛쒖＜湲곌??쇰줈 ?≫엳???ㅽ깘???ы쁽?덈떎.
- [x] 吏㏃? 吏紐??ㅼ쓽 `??숆탳`, `??숈썝`, `???, `?곗뿭`, `??, `泥? ?묐??щ뒗 ?됱젙援ъ뿭 蹂꾩묶?쇰줈 蹂댁? ?딅룄濡?留됱븯??
- [x] L5 ?ы솗?몄뿉???ㅽ깘 4嫄댁? 紐⑤몢 ?댁냼?먭퀬, ?좏슚???덉뼇/?됲깮/遊됲솕/?뺤쓭 吏덈Ц??湲곌? 留ㅽ븨? ?좎??먮떎.
- [x] L0-L5 吏??鍮꾧탳??`loop_points_chart.svg`瑜??앹꽦?덈떎.
- [x] L6?먯꽌 qv3_010??怨좎퀜吏??덉뼇 ?꾪꽣 ?꾨옒 ?먮Ц 洹쇨굅瑜??뺤씤?덈떎. ?덉빟/寃곗젣/PG/?뚯썝/?ㅼ삤?ㅽ겕/諛쒓텒/留ㅼ텧/臾댁씤 愿??洹쇨굅媛 紐⑤몢 媛숈? 諛쒖＜湲곌? 踰붿쐞 ?덉뿉 議댁옱?쒕떎.
- [x] L0-L6 吏??鍮꾧탳??`loop_points_chart.svg`瑜??ㅼ떆 ?앹꽦?덈떎.
- [x] L7?먯꽌 釉붾씪?몃뱶 梨꾩젏 寃利앺뙥???앹꽦?덈떎. ?뺤긽 ?듬?, 寃곗젣/PG 洹쇨굅 遺?? ?臾몄꽌 ?쇱엯, ?뺤긽 嫄곗젅, 議곗옉???숈같/?곕씫泥? 媛숈? 湲곌? ??踰붿쐞 ?쇰룞 耳?댁뒪瑜??ы븿?쒕떎.
- [x] L0-L7 吏??鍮꾧탳??`loop_points_chart.svg`瑜??ㅼ떆 ?앹꽦?덈떎.
- [x] L8?먯꽌 寃利앺뙥 ?ㅽ뻾湲곕? 異붽??섍퀬 no-api 紐⑤뱶濡??뺤씤?덈떎. 6媛?耳?댁뒪, 湲곕? ?듦낵 2媛? 湲곕? ?ㅽ뙣 4媛쒓? ?뺤긽 吏묎퀎?먮떎.
- [x] L0-L8 吏??鍮꾧탳??`loop_points_chart.svg`瑜??ㅼ떆 ?앹꽦?덈떎.
- [x] qv3_010留??묎쾶 ?ㅼ떆 ?ㅽ뻾???덉뼇 臾몄꽌留뚯쑝濡?寃곗젣/PG ?붽뎄媛 ?뚮났?섎뒗吏 ?뺤씤?덈떎. top5??湲곌? 踰붿쐞媛 源⑤걮?댁죱吏留?PG瑜??볦낀怨? top8? PG/諛쒓텒/留ㅼ텧源뚯? ?뚮났?덈떎.
- [x] L0-L10 吏??鍮꾧탳??`loop_points_chart.svg`瑜??ㅼ떆 ?앹꽦?덈떎.
- [x] ?쒖꽕 ?덉빟泥섎읆 ?뚯썝/寃곗젣/PG/諛쒓텒/留ㅼ텧 ?몃?洹쇨굅媛 ?④퍡 ?꾩슂??吏덈Ц? top8濡?蹂대궡??adaptive top_k 洹쒖튃 ?꾨낫瑜?留뚮뱾?덈떎.
- [x] L0-L11 吏??鍮꾧탳??`loop_points_chart.svg`瑜??ㅼ떆 ?앹꽦?덈떎.
- [x] ????듬? ?덉쭏 由щ럭? `report_ready` ?꾨낫瑜?L12/L13?쇰줈 ?쒖떆?섍퀬 `loop_points_chart.svg`瑜??ㅼ떆 ?앹꽦?덈떎.
- [ ] adaptive top_k 洹쒖튃? ?꾩쭅 ?먯닔 寃利??꾩씠?? ?ъ슫 ?⑥씪 吏덈Ц怨??몃?洹쇨굅 吏덈Ц???욎? ?묒? 吏덈Ц?뗭뿉??no-judge媛 ?꾨땶 ?ㅼ젣 梨꾩젏 湲곗??쇰줈 ?뺤씤?댁빞 ?쒕떎.
- [ ] broad top_k sweep? 蹂대쪟?쒕떎. ?ㅼ쓬 ?깅뒫 二쇱옣? ??吏덈Ц???먮뒗 釉붾씪?몃뱶 梨꾩젏湲?寃利??댄썑?먮쭔 ?쒕떎.
- [ ] 鍮꾩슜 ?덉슜 ??L7 寃利앺뙥?쇰줈 balanced judge blind calibration??吏꾪뻾?쒕떎. ?쇰????由??듬?, ?ㅻⅨ 臾몄꽌 洹쇨굅瑜??욎? ?듬?, ?덈Т 湲몄?留?吏덈Ц????留욌뒗 ?듬????ｌ뼱 ?≪븘?대뒗吏 蹂몃떎.
- [ ] v3 12臾명빆? ?대? ??踰??ъ슜?덉쑝誘濡? 蹂닿퀬?쒖뿉?쒕뒗 ??寃利?洹쇨굅? ?ъ떆??洹쇨굅瑜?遺꾨━?댁꽌 ?대떎.

## ?ㅼ쓬 ?덉쭏 由щ럭 猷⑦봽

- [x] ????듬? 8媛쒕? 怨좎젙?덈떎. ?뺤긽 ?듬?, ?먯닔???믪?留?湲??듬?, PG ?꾨씫 ?듬?, top8 ?뚮났 ?듬?, ?뺤긽 嫄곗젅, 議곗옉 ?듬? ?꾪뿕, 媛숈? 湲곌? ??踰붿쐞 ?쇰룞 ?щ?瑜??ы븿?덈떎.
- [x] ?듬? ?먯껜 ?덉쭏 愿?먯뿉??contextual quality, usefulness, conciseness, directness瑜??쒕줈 ?됯??덈떎.
- [x] 洹쇨굅/?몄슜 ?덉쭏 愿?먯뿉??evidence fit, citation clarity, source-scope risk, unsupported detail risk瑜??쒕줈 ?됯??덈떎.
- [x] 蹂닿퀬???쒖슜 愿?먯뿉???대뼡 ?щ?媛 ?쒖??쒕뒗 ?믪?留??⑸뱷??遺議깊븳 ?듬??? ?쒖닽?먭? ?꾨땲???덉감媛 以묒슂???щ??? ?쒓컻???꾪썑 李⑥씠媛 紐낇솗???щ??앹씤吏 遺꾨쪟?덈떎.
- [x] ??愿?먯쓣 ?⑹퀜 `answer_quality_review_matrix.md/json/csv/svg`濡?留뚮뱾?덈떎.
- [x] ?낅Т?쇱??먮뒗 ?덉쭏 由щ럭?먯꽌 ?살? ?몄궗?댄듃? ?ㅼ쓬 媛쒖꽑 媛?ㅼ쓣 ?쇨린?앹쑝濡??댁뼱 ?쇰떎.
- [x] A/B/C 怨좊뱷???λЦ ?듬???????붿빟 怨꾩링怨??듭떖 bullet ?섎? 以꾩씠???듬? ?щ㎎ ?꾨낫瑜?留뚮뱺??
- [ ] E/F/G ?덉뼇 媛쒖꽑 ?ㅽ넗由щ? 理쒖쥌 蹂닿퀬?쒖쓽 ???before/after ?щ?濡??몄쭛?쒕떎.
- [ ] D/H ?덉쟾???鍮??щ?瑜?梨꾩젏湲?寃利??먮뒗 蹂닿퀬?쒖쓽 hallucination/媛쒖씤?뺣낫 ?꾪뿕 ?щ?濡??몄쭛?쒕떎.
- [x] `report_ready` ?듬? ?꾨낫瑜?異붽??섍퀬 `prompt_sweep`??`prompt_report_ready` ?꾨낫瑜??곌껐?덈떎.
- [x] ???듬? ?꾨낫??湲곕낯媛믪쓣 諛붽씀吏 ?딄퀬 臾대퉬???뺤쟻/媛吏??몄텧 寃利앸쭔 ?듦낵?쒖섟??
- [ ] `prompt_report_ready`???꾩쭅 ?먯닔 寃利??꾩씠?? 鍮꾩슜 ?덉슜 ???묒? ?쇳빀 吏덈Ц?뗭뿉??judge ?ы븿?쇰줈 ?ㅽ뻾?섍퀬, EDD? ?щ엺 湲곗? ?덉쭏???④퍡 鍮꾧탳?쒕떎.
- [ ] ???꾨낫媛 ?듬???吏㏐쾶 留뚮뱾硫댁꽌 洹쇨굅 萸됯컻湲곕굹 怨쇱엵 嫄곗젅??留뚮뱾吏 ?딅뒗吏 A/B/C, D/H, E/F/G 以묒떖?쇰줈 耳?댁뒪蹂?由щ럭?쒕떎.

## ?ㅻ뱶由ъ뒪 猷⑦봽 寃뚯씠??

- [x] ?먮룞 猷⑦봽??red gate, overfit gate, runner state, next experiment priority瑜??쒖븞/蹂묓빀?덈떎.
- [x] `scripts\headless_gate.py`瑜?異붽???湲곗〈 L0-L13 寃곌낵瑜??먮룞 遺꾨쪟?덈떎.
- [x] L14瑜?`headless_red_overfit_gate_audit`濡?異붽??덈떎. ?깅뒫 ?먯닔媛 ?꾨땲???댁쁺 寃뚯씠??寃곌낵??
- [x] ?꾩옱 湲곗??쇰줈 L0留?first-validation promotable evidence濡??④린怨? L1? measurement correction?쇰줈 遺꾨━?덈떎.
- [x] L12??qualitative evidence, L13? candidate-only濡?遺꾨━?덈떎.
- [x] 猷⑦봽 李⑦듃? 蹂닿퀬?쒖뿉 L14瑜?諛섏쁺?덈떎.
- [x] `scripts\run_headless_loop.py`? `headless_manifest.json`??異붽??덈떎.
- [x] L15濡?no-api manifest runner瑜??ㅽ뻾?덇퀬, ?ㅼ쓬 ?됰룞??`pending_cost_gate`濡??먯젙?덈떎.
- [x] L16?쇰줈 ??v4 寃利?吏덈Ц 珥덉븞 10臾명빆??留뚮뱾?덈떎. ?꾩쭅 ?먯닔?⑹쑝濡??ㅽ뻾?섏? ?딆븯??
- [x] L17濡?吏덈Ц???몄텧 ?곹깭?쒕? 留뚮뱾?덈떎. v2 holdout? spent, v4 draft??first-run ???꾨낫濡?遺꾨━?덈떎.
- [x] L18濡??몄텧 ?곹깭?쒕? 寃뚯씠?몄뿉 ?곌껐?섍퀬, ?ㅻ챸臾??⑥뼱 ?뚮Ц???앷릿 ?꾨낫 遺꾨쪟 ?ㅽ깘???섏젙?덈떎.
- [x] L19濡?v4 吏덈Ц?뗭쓣 first-run??怨좎젙蹂몄쑝濡?蹂듭궗?섍퀬 SHA256 manifest瑜??④꼈??
- [ ] 鍮꾩슜 ?덉슜 ??L20?쇰줈 湲곗〈 6耳?댁뒪 blind judge calibration???ㅽ뻾?쒕떎.
- [ ] L20???ㅽ뙣?섎㈃ judge/rubric/context瑜?癒쇱? 怨좎튂怨? prompt/adaptive scored run? 蹂대쪟?쒕떎.
- [ ] L20???듦낵?섎㈃ L21濡?`prompt_report_ready` ?뚭퇋紐?scored sweep???ㅽ뻾?쒕떎.
- [ ] 理쒖쥌 ?쇰컲???깅뒫 二쇱옣? fresh untouched validation set ?꾩뿉???섏? ?딅뒗??

## 2026-07-06 L20-L29 ?꾩냽 ?뺣━

- [x] L20 湲곗〈 6耳?댁뒪 梨꾩젏 寃?뺥뙥??鍮꾩슜 ?쒗븳 ?꾨옒 ?ㅽ뻾?덈떎. ?먯젙? 6/6 留욎븯吏留?groundedness 湲곕?踰붿쐞媛 5/6?대씪 諛붾줈 ?ㅼ쓬 ?먯닔 ?ㅽ뿕???댁? ?딆븯??
- [x] L21 梨꾩젏 寃???ㅽ뻾湲곗뿉 0~5 ?먯닔 踰붿쐞 吏?쒖? `score_range_ok` 寃利앹쓣 異붽??덈떎.
- [x] L22 媛숈? 寃?뺥뙥???ㅼ떆 ?ㅽ뻾???먯닔 踰붿쐞???덉젙?먯?留? ?듦낵 ?덉떆 ?섎굹媛 ?좊ℓ???쒗쁽 ?뚮Ц???ㅽ뙣?섎뒗 寃껋쓣 ?뺤씤?덈떎.
- [x] L23 ?먮낯 寃?뺥뙥? 蹂댁〈?섍퀬 ???꾧꺽??寃?뺥뙥??留뚮뱾?덈떎.
- [x] L24 ?꾧꺽??寃?뺥뙥?먯꽌 ?먯젙/?먯닔踰붿쐞/groundedness 湲곕?踰붿쐞媛 紐⑤몢 6/6 ?듦낵?덈떎.
- [x] L25 ?숆껐 v4 吏덈Ц?뗭쓽 泥??먯닔 ?ㅽ뻾??蹂댁〈?덈떎. ?꾩옱 v4 湲곗??먯? EDD 97.41?대떎.
- [x] L26 ?꾩뿭 top5???됯퇏 吏?곗쓣 0.652珥덈쭔 以꾩씠怨?relevance瑜???떠 湲곕낯媛믪쑝濡?湲곌컖?덈떎.
- [x] L27 `report_ready`???덉쭏?먯닔???좎??덉?留?吏?곗떆媛꾩씠 ?ш쾶 ?섏뼱 湲곕낯媛믪쑝濡?湲곌컖?덈떎.
- [x] L28/L29 `concise_verified`??嫄곗젅 ?쒗쁽 媛먯? 蹂댁젙 ??EDD 96.42濡??뚮났?먯?留?L25蹂대떎 ??븘 湲곕낯媛믪쑝濡?湲곌컖?덈떎.
- [ ] 媛숈? v4 ?명듃?먯꽌 異붽? ?꾨＼?꾪듃 ?쒕떇??怨꾩냽?섏? ?딅뒗?? ???ㅽ뙣 媛???놁씠 諛섎났?섎㈃ 怨쇱쟻???꾪뿕?????щ떎.
- [ ] ?ㅼ쓬 ?좎쓽誘명븳 ?꾨낫????誘몃끂異?吏덈Ц?? L25 ?듬????щ엺 湲곗? 媛?낆꽦 媛먮━, ?먮뒗 `qv4_002`/`qv4_004`/`qv4_008` 吏?곗떆媛??먯씤 遺꾩꽍?대떎.

## 2026-07-06 L30-L36 ?곷? 吏덈Ц ?뺤옣

- [x] ?쒕ぉ 議곌컖, 媛쒖씤?뺣낫 ?⑥젙, 理쒖쥌 ?낆껜/怨꾩빟湲덉븸 ?⑥젙, 鍮꾧탳 吏덈Ц, 媛숈? ???ㅻⅨ ?쒗쁽???ы븿??v5 ?곷? 吏덈Ц?뗭쓣 留뚮뱾怨?怨좎젙?덈떎.
- [x] L30 泥?v5 ?ㅽ뻾??蹂댁〈?덈떎. EDD `92.40`?대ŉ `qv5_010c`?먯꽌 諛쒖＜湲곌? ?녿뒗 ?쒕ぉ 議곌컖 寃???ㅽ뙣媛 ?쒕윭?щ떎.
- [x] `src\retriever.py`???꾧꺽???ъ뾽紐?議곌컖 湲곕컲 諛쒖＜湲곌? ?꾪꽣瑜?異붽??덈떎.
- [x] ?쒕ぉ 議곌컖 ?꾪꽣 ??v5 臾몃㎘ ?ㅼ뿼瑜좎씠 `0.0`?쇰줈 ?대젮媛??寃껋쓣 ?뺤씤?덈떎.
- [x] `scripts\evaluate.py`?먯꽌 誘쇨컧 ?덉떆 嫄곗젅 媛먯? 洹쒖튃??醫곴쾶 蹂댁젙?덈떎.
- [x] 媛숈? v5 ?듬? ?ш퀎?곗쓣 ???깅뒫 ?ㅽ뿕怨?遺꾨━?덈떎. L33 EDD `98.37`, L34 EDD `98.70`? 蹂댁젙媛믪씠??
- [x] v4 ?뚭? ?뺤씤???ㅽ뻾?덈떎. ?뺣떟??遺뺢눼???놁뿀吏留?吏?곗떆媛꾩씠 L25蹂대떎 醫뗭븘吏吏 ?딆븯??
- [x] v4 top5媛 吏???덉쭏 寃쎄퀎瑜?媛쒖꽑?섏? 紐삵빐 ?꾩뿭 top5 湲곕낯媛??밴꺽???ㅼ떆 湲곌컖?덈떎.
- [x] L30-L36 蹂닿퀬?쒖? 猷⑦봽 ??李⑦듃瑜?媛깆떊?덈떎.
- [ ] v5???곗? ?딆? ?ъ뾽紐?議곌컖?쇰줈 v6 誘몃끂異?寃利앹뀑??留뚮뱺??
- [ ] `?뺣낫?쒖뒪??援ъ텞`, `?덉쟾愿由??쒖뒪??, `?듦퀎 ??쒕낫??泥섎읆 ?쇰컲?곸씤 ?쒕ぉ 議곌컖留??덈뒗 ?ㅽ깘 寃?щ? 留뚮뱺??
- [ ] EDD媛 ?ㅼ떆 泥쒖옣??媛源뚯슦誘濡?L33/L34 ?듬????щ엺 湲곗? 媛?낆꽦/洹쇨굅 異붿쟻?깆쑝濡??곕줈 寃?좏븳??
- [ ] ?쒕ぉ ?꾪꽣媛 ?띾룄瑜?媛쒖꽑?덈떎怨?二쇱옣?섍린 ??吏?곗떆媛?蹂?숈꽦???곕줈 蹂몃떎.

## 2026-07-06 R&D 湲곕컲 異붽? 諛⑸쾿 ?꾨낫

- [x] R&D Workbench?먯꽌 RAG ?됯?/?뚯뒪?명뙥/?덊띁?곗뒪瑜?癒쇱? 寃?됲뻽?? 濡쒖뺄 ???洹쇨굅???놁뼱 ?몃? 1李??먮즺 議곗궗濡??뺤옣?덈떎.
- [x] Ragas, TruLens, LlamaIndex, ARES, RAGChecker, LangSmith ?먮즺瑜?諛뷀깢?쇰줈 吏덈Ц ?ㅼ뼇??諛뽰쓽 媛쒖꽑 諛⑸쾿???뺣━?덈떎.
- [x] v6?먮뒗 誘몃끂異??ъ뾽紐?議곌컖肉??꾨땲??metamorphic/property ?뚯뒪?몃? ?ｋ뒗?? 媛숈? ?살쓽 吏덈Ц? 媛숈? ?듭쓣 ?좎??섍퀬, 愿???녿뒗 臾몄꽌 異붽??먮뒗 ?붾뱾由ъ? ?딆쑝硫? ?뺣떟 洹쇨굅 ?쒓굅 ?쒖뿉???뺤씤 遺덇?濡?媛???쒕떎.
- [x] v7?먮뒗 corpus perturbation ?뚯뒪?몃? ?ｋ뒗?? ?뺣떟 chunk ?쒓굅, 鍮꾩듂?섏?留??由?decoy chunk 二쇱엯, ?쇰컲 ?쒕ぉ 議곌컖 ?ㅽ깘???곕줈 蹂몃떎.
- [x] v8?먮뒗 claim-level citation audit???ｋ뒗?? ?듬????먯옄 二쇱옣?쇰줈 ?섎늻怨?媛?二쇱옣留덈떎 洹쇨굅 chunk媛 ?덈뒗吏 ?몄뼱 unsupported claim rate瑜?留뚮뱺??
- [x] v9?먮뒗 latency/cost trace瑜??ｋ뒗?? retrieval, rerank/filter, generation, judge ?쒓컙??遺꾨━??EDD? 蹂꾨룄???ㅼ쭏 媛쒖꽑 吏?쒕줈 蹂몃떎.
- [ ] ?먯닔 寃뚯씠?몄뿉??理쒖냼 ?④낵 ?ш린? ?ъ궗??吏덈Ц???쇰꺼???ｋ뒗?? ?몄텧??吏덈Ц?뗭뿉??0.x???ㅻⅨ 媛믪? ?쇰컲 ?깅뒫 ?곸듅?쇰줈 ?밴꺽?섏? ?딅뒗??
- [ ] judge calibration? planted pass/fail pack?쇰줈 癒쇱? ?듦낵?쒗궓 ?????먯닔 ?ㅽ뿕???곕떎. ?쇰????섍컖, ?臾몄꽌 洹쇨굅, 怨쇱엵 嫄곗젅, 湲대뜲 吏덈Ц????留욌뒗 ?듭쓣 ?ｋ뒗??

## 2026-07-06 L37-L40 v6 ?ㅽ뻾 ?꾩냽

- [x] v6 metamorphic/property 吏덈Ц?뗭쓣 留뚮뱾怨?first-run??怨좎젙蹂멸낵 manifest瑜??④꼈??
- [x] L37 v6 泥??ㅽ뻾??蹂댁〈?덈떎. ?꾩옱 ?뺤쭅??v6 泥?洹쇨굅??EDD `86.25`??
- [x] L37 ?ㅽ뙣 ?먯씤??`qv6_004` unsupported final procurement, `qv6_010` generic title ambiguity, `qv6_007` metamorphic/entity-binding failure濡?遺꾨━?덈떎.
- [x] L38?먯꽌 ?덉쟾 ?꾨＼?꾪듃瑜?蹂닿컯???덉궛/理쒖쥌怨꾩빟湲덉븸, 怨듭떇?곕씫泥?媛쒖씤?곕씫泥? ?좊ℓ???쒕ぉ/?뺤젙 ?ъ뾽??遺꾨━?덈떎.
- [x] L39?먯꽌 top_k留??섎━??諛⑹떇??qv6_007???닿껐?섏? 紐삵븿???뺤씤?덈떎.
- [x] L40?먯꽌 `?꾩떆愿由ш났?? alias瑜?異붽???`怨좎뼇 怨듭궗` 寃???ㅼ뿼??以꾩???
- [x] ?먮Ц?먯꽌 `異쒖엯?듭젣?쒖뒪??, `臾댁씤諛쒓텒湲?, `以묎퀎?쒕쾭`, `2SET` 洹쇨굅媛 ?ㅼ젣濡?議댁옱?⑥쓣 ?뺤씤?덈떎.
- [x] L37-L40 summary, checkpoint, loop_points.csv, loop_points_chart.svg瑜??묒꽦?덈떎.
- [x] 吏덈Ц ?몄텧 ?덉??ㅽ듃由щ? 媛깆떊??v6 泥??ㅽ뻾 ?댄썑 ?곹깭? L38/L39 吏꾨떒 ?뚯씪??諛섏쁺?덈떎.
- [x] qv6_006/qv6_007 蹂?뺤뙇??claim-level濡?鍮꾧탳??媛숈? ?ъ뾽/媛숈? ?섎룄?먯꽌 鍮좎쭊 二쇱옣怨?洹쇨굅 ?꾨씫???몄뼱 蹂몃떎.
- [x] qv6_010? ?쒕え?명븯?ㅺ퀬 留먰븳 ??湲멸쾶 ?꾨낫瑜??ㅻ챸?섎뒗 怨쇱엵?묐떟?앹쓣 蹂꾨룄 ?덉쭏 ?ㅽ뙣濡??〓뒗??
- [x] ?쇰컲 ?ㅽ뿕 ?뚯빱??token/cost usage ledger瑜?遺숈씠嫄곕굹, ?묒? 鍮꾩슜 異붿젙/愿痢?runner瑜?留뚮뱺 ??broad paid loop瑜??ш컻?쒕떎.
- [ ] v7/v8/v9 ?꾩껜 ?ㅽ뻾? 鍮꾩슜 異붿쟻怨?怨쇱쟻??寃뚯씠?멸? 遺숆린 ?꾧퉴吏 broad run?쇰줈 ?댁? ?딅뒗??

## 2026-07-06 L41-L45 ?덉쭏/鍮꾩슜 寃뚯씠??

- [x] qv6_006/qv6_007 蹂?뺤뙇??claim-level濡?鍮꾧탳?덈떎. L40? retrieval partial recovery吏留?full metamorphic pass媛 ?꾨땲??
- [x] qv6_010? ?쒕え?명븯?ㅺ퀬 留먰븳 ??湲멸쾶 ?꾨낫瑜??ㅻ챸?섎뒗 怨쇱엵?묐떟?앹쓣 `ambiguous_identifier_refusal_with_excessive_candidate_summary` ?덉쭏 ?댁뒋濡??뺤쓽?덈떎.
- [x] ?쇰컲 ?ㅽ뿕 ?뚯빱??token/cost usage ledger瑜?遺숈???
- [x] dry-run 寃곌낵媛 scoreboard???욎씠吏 ?딅룄濡?`scripts\aggregate_parallel_eval.py`瑜?蹂닿컯?덈떎.
- [x] diagnostic question set 寃곌낵媛 scoreboard???욎씠吏 ?딅룄濡?吏덈Ц ?몄텧 ?덉??ㅽ듃由ъ? 吏묎퀎湲곕? ?곌껐?덈떎.
- [x] L43 one-case no-judge 鍮꾩슜 trace瑜??ㅼ젣 ?몄텧濡??뺤씤?덈떎. observed local-table cost??`$0.008312`??
- [x] final summary??L37 EDD `86.25`留?scoreboard???④린怨?L38-L43??diagnostic-only濡?遺꾨━?쒕떎.
- [x] live judge-included cost-trace smoke瑜?1臾명빆留??ㅽ뻾??judge usage/cost path瑜??뺤씤?쒕떎.
- [ ] qv6_007 physical access-control under-answer瑜?以꾩씠??answer evidence-use guard瑜??ㅺ퀎?쒕떎.
- [x] qv6_010 怨쇱엵?묐떟 ?덉쭏 ?댁뒋瑜?evaluate/report aggregation??蹂꾨룄 issue label濡?援ы쁽?쒕떎.
- [x] worker ?ㅽ뻾湲곗뿉 hard-stop budget runner瑜?遺숈씠怨? preflight budget skip???먯닔?먯쓣 ?ㅼ뿼?쒗궎吏 ?딅뒗吏 寃利앺븳??
- [x] L46 ?덈뱶 由щ럭 諛섏쁺: dry-run? ?덉궛 skip?먯꽌 ?쒖쇅?섍퀬, non-dry preflight skip??蹂꾨룄 寃利앺뻽??
- [x] budget ledger瑜?利됱떆 append 諛⑹떇?쇰줈 諛붽씀怨?all-skipped run??`budget_gate_all_skipped=true`濡?湲곕줉?쒕떎.
- [x] ????듬? ?ш퀎???ㅽ겕由쏀듃?먯꽌??`answer_quality_issues`瑜??ㅼ떆 ?꾪뙆?쒕떎.
- [ ] broad paid v7/v8/v9??claim-preservation gate ?꾧퉴吏 ?댁? ?딅뒗??
- [ ] L44瑜?蹂닿퀬???щ?濡??몄쭛?쒕떎. ?먮룞 judge??5/5瑜?以ъ?留??щ엺 湲곗??먯꽌??qv6_007 physical access-control under-answer媛 ?⑥? ?щ???

## 2026-07-07 L47 claim-preservation 寃뚯씠??

- [x] qv6_007 exposed metamorphic case?????no-API claim-preservation expectation??留뚮뱾?덈떎.
- [x] checker媛 JSON/CSV/Markdown 寃곌낵瑜??곌퀬, ?ㅽ뙣 ??exit code `1`???대룄濡?援ы쁽?덈떎.
- [x] Worker A??claim schema ?쒖븞怨?Worker B??red review瑜?諛섏쁺??source scope瑜?CSV row ?⑥쐞濡?醫곹삍??
- [x] false-friend access-control, underanswer polarity, missing source marker瑜?蹂꾨룄 ?댁뒋濡??④린寃??덈떎.
- [x] L37/L40/L44瑜??ш?利앺뻽?? L37? `0/2`, L40? `1/2`, L44??`1/2`?대ŉ 紐⑤몢 gate fail?대떎.
- [x] L44??judge 5/5? claim gate fail???숈떆???섏삩 judge-blindness ?щ?濡??쇰꺼留곹뻽??
- [x] qv6_007 answer evidence-use guard瑜??ㅼ젣 ?듬? ?앹꽦 寃쎈줈??遺숈뿬 physical access-control claim源뚯? 蹂댁〈?섍쾶 留뚮뱾?덈떎.
- [x] L48-L76?먯꽌 CSV ?ъ뾽 ?붿빟 蹂닿컯, evidence-use guard, ambiguity concision guard, project focus filter瑜??곸슜?섍퀬 no-API fixture 14/14 諛?L76 exposed regression??寃利앺뻽??
- [x] ?꾩떆 probe ?뚯씪??scoreboard???ㅼ뼱媛吏 ?딅룄濡?unregistered question set??diagnostic-only濡?寃⑸━?덈떎.
- [x] L76 qv6_007 claim preservation? `2/2` pass?대ŉ, L76 ?꾩껜 v6 exposed regression? EDD `97.13`, groundedness `5.0`, relevance `5.0`, abstention accuracy `1.0`?대떎.
- [ ] L76? 媛숈? v6 ?ㅽ뙣瑜?蹂???怨좎튇 ?몄텧 ?뚭??대?濡?fresh validation ?먯닔濡??밴꺽?섏? ?딅뒗?? 蹂닿퀬?쒖뿉??L37 EDD `86.25`瑜??뺤쭅??泥?v6 洹쇨굅濡??④릿??
- [ ] ??誘몃끂異?v7/v8 寃利앹뀑??留뚮뱾怨? ?쒕떇???곗? ?딆? split?먯꽌 ?쇰컲???щ?瑜??뺤씤?쒕떎.
- [ ] L76 latency `20.642s`瑜?蹂꾨룄 ?띾룄/鍮꾩슜 猷⑦봽濡?以꾩씤?? ?뱁엳 qv6_006, qv6_010??湲?吏?곗쓣 癒쇱? 蹂몃떎.
- [ ] CSV summary backfill? ?꾩옱 qv6_007 target-bound ?⑸룄?대?濡? ??寃利앹뀑?먯꽌 false positive媛 ?녿뒗吏 諛섎뱶???뺤씤?쒕떎.

## 2026-07-07 L77 latency prompt probe

- [x] L76 latency `20.642s`瑜?以꾩씠湲??꾪빐 `prompt_concise_verified_only`瑜??몄텧 v6 ?명듃?먯꽌 吏꾨떒 ?ㅽ뻾?덈떎.
- [x] L77? EDD `92.25`, latency `20.112s`, abstention accuracy `0.5`濡??앸궗??
- [x] qv6_010??紐⑦샇???쒕ぉ 議곌컖??嫄곗젅?섏? ?딄퀬 `援??怨쇳븰湲곗닠吏?앹젙蹂댁꽌鍮꾩뒪` ?붽뎄踰붿쐞瑜??붿빟??寃껋쓣 ?뺤씤?덈떎.
- [x] 寃곕줎: 媛꾧껐 ?꾨＼?꾪듃留뚯쑝濡??띾룄瑜?以꾩씠??諛⑺뼢? 湲곌컖?쒕떎. ?띾룄 ?대뱷????`0.53s`肉먯씠怨??덉쟾 異뺤씠 源⑥죱??
- [x] L78 ?띾룄 ?덈뱶 由щ럭 ?쒖븞??諛쏆븯?? ?ㅼ쓬 ?띾룄 ?ㅽ뿕? top_k/context ?덇컧留?醫곴쾶 蹂대ŉ, 臾쇱쭏??吏??媛쒖꽑怨??덉쭏 ?좎?媛 ?숈떆???덉뼱???쒕떎.
- [x] L78 ??寃利앹뀑 ?ㅺ퀎 ?쒖븞??諛쏆븯?? 吏덈Ц ?뚯씪? ?꾩쭅 留뚮뱾吏 ?딆븯怨? ?쒖븞?쒕뒗 ?ㅼ쓬 誘몃끂異?v7/v8 以鍮?洹쇨굅濡쒕쭔 ?④꼈??
- [ ] ?ㅼ쓬 ?띾룄 猷⑦봽??qv6_007 claim `2/2`, qv6_010 abstention pass, groundedness/relevance `5/5`, latency 理쒖냼 `1s` ?먮뒗 `10%` 媛쒖꽑???섎뱶 寃뚯씠?몃줈 ?붾떎.
- [ ] ??誘몃끂異?v7/v8 寃利앹뀑? L76/L77蹂대떎 ?곗꽑?쒖쐞 ?믪? ?쇰컲??洹쇨굅濡??곕줈 留뚮뱺??

## 2026-07-07 L79 guarded top-k latency probe

- [x] L78 ?덈뱶 由щ럭 議곌굔???곕씪 ?몄텧 v6?먯꽌 `topk_sweep`??吏꾨떒 ?ㅽ뻾?덈떎.
- [x] topk5: EDD `98.13`, latency `16.209s`, quality `5/5`, abstention `1.0`, qv6_007 claim `2/2`, observed cost `$0.116122`.
- [x] topk8 control: EDD `98.15`, latency `16.130s`, quality `5/5`, abstention `1.0`, qv6_007 claim `2/2`, observed cost `$0.139327`.
- [x] topk12: EDD `95.62`, groundedness `4.5`, relevance `4.875`, qv6_007 claim `2/2`; 湲곌컖?쒕떎.
- [x] L79 寃곌낵??紐⑤몢 `exposed_regression` 諛?`diagnostic_only`濡??④꼈怨?scoreboard??L37留??좎??덈떎.
- [ ] topk5??鍮꾩슜 ?꾨낫??肉??꾩쭅 梨꾪깮?섏? ?딅뒗?? qv6_006/qv6_010 tail latency媛 topk8蹂대떎 ?섎튌 諛섎났 ?뺤씤???꾩슂?섎떎.
- [ ] topk8? ?꾪뻾 control?대?濡??쒖깉 理쒖쟻?붴앸씪怨?遺瑜댁? ?딅뒗?? ?띾룄 媛쒖꽑 二쇱옣? 諛섎났???먮뒗 誘몃끂異?寃利앹뿉???뺤씤?댁빞 ?쒕떎.
- [ ] topk12 ?щ?瑜?蹂닿퀬?쒖뿉 ?ｋ뒗?? claim gate???듦낵?덉?留?groundedness媛 ?대젮媛誘濡? claim 蹂댁〈怨?洹쇨굅 ?덉쭏? 蹂꾨룄 異뺤씠??

## 2026-07-07 L80 exposure registry correction

- [x] v5 frozen ?뚯씪??registry?먮뒗 誘몄떎???꾨낫濡??⑥븘 ?덉뿀吏留? ?ㅼ젣濡쒕뒗 L30?먯꽌 ?대? first validation?쇰줈 ?ㅽ뻾??寃껋쓣 ?뺤씤?덈떎.
- [x] `scripts/build_exposure_registry.py`瑜?怨좎퀜 v5 draft/frozen ?곹깭瑜?exposed濡?諛붽엥??
- [x] qv6_l61, qv6_l65 ?꾩떆 probe ?뚯씪??diagnostic-only濡?紐낆떆?덈떎.
- [x] `scripts/aggregate_parallel_eval.py`媛 `unknown_needs_review`? `do_not_promote_until_reviewed`瑜?scoreboard?먯꽌 ?쒖쇅?섎룄濡?蹂닿컯?덈떎.
- [x] registry ?ъ깮????aggregate媛 `scoreboard_rows=1`, `diagnostic_only_rows=35`濡?蹂듦뎄?⑥쓣 ?뺤씤?덈떎.
- [ ] v5?????댁긽 ??first-run?쇰줈 ?곗? ?딅뒗?? ?ㅼ쓬 ?쇰컲??洹쇨굅????v7/v8濡?留뚮뱺??

## 2026-07-07 L81-L83 source-exposed v7 and sensitive refusal-tail loop

- [x] ?꾩쟾 誘몃끂異?source project媛 ?⑥븘 ?덉? ?딆쓬???뺤씤?섍퀬, v7???꾧꺽 holdout???꾨땲??source-exposed prompt diagnostic?쇰줈 ?쇰꺼留곹뻽??
- [x] `questions_v7_source_exposed_prompt_diagnostic_frozen.json`???ㅽ뻾?덈떎. L81 EDD `97.41`, latency `19.407s`, abstention accuracy `1.0`.
- [x] L81? diagnostic-only濡?aggregate???④꼈怨? scoreboard??L37 ???됰쭔 ?좎??덈떎.
- [x] qv7_006?먯꽌 ?먮룞 吏?쒕뒗 ?믪?留??듬???理쒖쥌 寃곌낵 嫄곗젅 ??泥?뎄 ?먮쫫/怨듭떇 ?곕씫泥섎? ?㏓텤?대뒗 ?덉쭏 臾몄젣瑜??뺤씤?덈떎.
- [x] `sensitive_or_forbidden_refusal_with_detail_tail` 吏꾨떒 ?뚮옒洹몃? 異붽??덈떎.
- [x] `_apply_sensitive_abstention_guard`瑜?異붽???理쒖쥌 ?숈같/怨꾩빟湲덉븸/?섏옄 ?щ?/媛쒖씤 ?곕씫泥?異붿젙 ?붿껌?먮뒗 吏㏐쾶 嫄곗젅?섎룄濡??덈떎.
- [x] no-API fixture媛 16/16 ?듦낵?덈떎.
- [x] `scripts/recompute_saved_eval.py`??吏곸젒 ?ㅽ뻾 import 臾몄젣瑜?怨좎낀??
- [x] L82 ????듬? ?щ텇?앹뿉??L81 EDD??洹몃?濡?`97.41`?댁?留?qv7_006 ?덉쭏 ?댁뒋媛 ?≫엳??寃껋쓣 ?뺤씤?덈떎.
- [x] L83 ??臾명빆 no-judge probe?먯꽌 qv7_006 ?듬???吏㏃? 嫄곗젅濡?諛붾뚭퀬 `answer_quality_issues=[]`媛 ??寃껋쓣 ?뺤씤?덈떎.
- [ ] L83 EDD `57.16`? judge ?앸왂 ?뚮Ц??鍮꾧탳 遺덇??대?濡??깅뒫 ?쒖쐞???곗? ?딅뒗??
- [ ] 理쒖쥌 蹂닿퀬?쒖뿉??qv7_006???쒖젏?섎뒗 ?믪븯吏留??⑸뱷?????섎뒗 ?듬????щ엺???쎌뼱 怨좎튇 ?щ??앸줈 ?ｋ뒗??
- [ ] ?ㅼ쓬 ?좎쓽誘명븳 ?묒뾽? L81/L83???④릿 latency `19~20s` 蹂묐ぉ??以꾩씠嫄곕굹, source-exposed媛 ?꾨땶 ?덈줈??寃利?洹쇨굅瑜?蹂꾨룄濡??뺣낫?섎뒗 寃껋씠??

## 2026-07-07 L84-L86 v7 latency shards and measurement correction

- [x] L84 ?⑥씪 `topk_sweep`??寃곌낵 ????꾩뿉 ?쒓컙 ?쒗븳??嫄몃젮 鍮?worker ?대뜑留??④릿 寃껋쓣 ?뺤씤?덈떎.
- [x] ?⑥씪 ???sweep? 鍮꾩슜/寃곌낵 異붿쟻?깆씠 ?섏걯誘濡?`topk5_only`, `topk8_only`, `topk12_only` shard suite瑜?異붽??덈떎.
- [x] L84 ?덈뱶 湲곗???諛쏆븯?? source-exposed 寃곌낵??diagnostic-only, no-judge EDD ?쇳빀 湲덉?, 誘쇨컧 嫄곗젅/紐⑦샇??瑗щ━ 吏???덉쭏 ?댁뒋??hard blocker??
- [x] L85 shard ?ㅽ뻾???꾨즺?덈떎.
- [x] L85媛 `is_abstention`??痢≪젙 ?ㅻ쪟瑜??쒕윭?덈떎. 遺遺??듬????꾩껜 嫄곗젅濡??멸굅?? project prefix媛 遺숈? ?섏옄 ?덉떆 嫄곗젅???볦튂??臾몄젣媛 ?덉뿀??
- [x] L86?먯꽌 abstention 痢≪젙湲곕? 蹂댁젙?섍퀬 no-API fixture瑜?`21/21` ?듦낵?쒖섟??
- [x] L86 ?ш퀎????topk5??EDD `97.99`, latency `16.865s`, max `25.85s`, ?덉쭏 ?댁뒋 ?놁쓬.
- [x] L86 ?ш퀎????topk8 control? EDD `98.00`, latency `16.794s`, max `23.46s`, ?덉쭏 ?댁뒋 ?놁쓬.
- [x] L86 ?ш퀎????topk12??EDD `95.51`, latency `19.922s`, max `36.95s`, groundedness/relevance `4.667/4.889`??湲곌컖?쒕떎.
- [ ] topk8? ?꾪뻾 control ?ъ떎?됱씠誘濡???理쒖쟻?붾줈 ?곗? ?딅뒗?? source-exposed diagnostic ?덉젙?깆쑝濡쒕쭔 湲곕줉?쒕떎.
- [ ] L84 ?⑥씪 sweep??誘멸린濡?鍮꾩슜 媛?μ꽦??蹂닿퀬?쒖뿉 由ъ뒪?щ줈 ?④릿?? ?꾩옱 愿痢?媛?ν븳 run-folder 珥앹븸? `$2.230893`?대굹, L84 timeout ?대? ?몄텧? local cost summary???녿떎.
- [ ] ?ㅼ쓬 ?띾룄 ?묒뾽? shard/checkpoint 諛⑹떇留??ъ슜?쒕떎.

## 2026-07-07 L87 plain-language answer quality gate

- [x] `plain_language_answer_over_structured` ?덉쭏 ?뚮옒洹몃? 異붽??덈떎.
- [x] no-API fixture瑜?`22/22` ?듦낵?쒖섟??
- [x] ??λ맂 L81/L85 ?듬????ш퀎?고뻽??
- [x] qv7_009媛 L81 baseline, L85 topk5, L85 topk8 control, L85 topk12?먯꽌 紐⑤몢 ???뚮옒洹몄뿉 嫄몃━??寃껋쓣 ?뺤씤?덈떎.
- [x] aggregate???ъ쟾??`scoreboard_rows=1`, `diagnostic_only_rows=40`?대떎.
- [ ] L87? EDD 媛쒖꽑???꾨땲??痢≪젙 ?뚯쫰 媛쒖꽑?쇰줈留?蹂닿퀬?쒕떎.
- [ ] qv7_009瑜?理쒖쥌 蹂닿퀬?쒖쓽 ?쒖젏?섎뒗 ?믪?留??ъ슜?먭? ?먰븯???듬? ?뺤떇怨??닿툔???щ??앸줈 ?ｋ뒗??
- [ ] ?ㅼ쓬 ?묒뾽? qv7_009 ??臾명빆 format probe濡??쒗븳?섍퀬, groundedness/abstention??源⑥?硫?利됱떆 湲곌컖?쒕떎.

## 2026-07-07 L88-L90 qv7_009 format probe and repair candidate

- [x] `questions_v7_l88_plain_language_probe.json`??留뚮뱾怨?diagnostic-only濡??깅줉?덈떎.
- [x] L88 `prompt_sweep`瑜???臾명빆?쇰줈 ?ㅽ뻾?덈떎.
- [x] L88 default??judge `5/5`吏留?`1228`?? `47`以? 紐⑸줉 `29`媛쒕씪 ?덉쭏 ?뚮옒洹멸? ?⑥븯??
- [x] L88 report_ready???덉쭏 ?뚮옒洹몃? 吏?좎?留?latency `50.94s`??broad setting?쇰줈??湲곌컖?덈떎.
- [x] `src/generator.py`??plain-language query marker媛 ?덉쓣 ?뚮쭔 遺숇뒗 醫곸? prompt hint瑜?異붽??덈떎.
- [x] L89?먯꽌 `605`?? `9`以? 紐⑸줉 `5`媛? judge `5/5`, latency `16.7s`, ?덉쭏 ?뚮옒洹??놁쓬?쇰줈 媛쒖꽑?⑥쓣 ?뺤씤?덈떎.
- [x] L89媛 final-result caveat ?뚮Ц??false abstention?쇰줈 ?ㅽ뙋??寃껋쓣 蹂닿퀬 L90?먯꽌 `is_abstention`??蹂댁젙?덈떎.
- [x] L90 fixture??`23/23` ?듦낵?덈떎.
- [ ] L89???⑥씪 source-exposed 臾명빆?대?濡??꾨낫 媛쒖꽑?쇰줈留??붾떎.
- [ ] ?ㅼ쓬 ?④퀎???꾩껜 v7 source-exposed diagnostic???ㅼ떆 ?뚮젮 鍮꾧탳/誘쇨컧?뺣낫/紐⑦샇??吏덈Ц???붾뱾由ъ? ?딅뒗吏 蹂대뒗 ?묒? regression?대떎.

## 2026-07-07 L91 v7 source-exposed regression after hint

- [x] plain-language hint ?곸슜 ??v7 source-exposed 12臾명빆 ?꾩껜瑜??ㅼ떆 ?뚮졇??
- [x] L91 EDD `97.82`, coverage/MRR `1.0/1.0`, groundedness/relevance `5.0/5.0`, abstention accuracy `1.0`.
- [x] ?꾩껜 12臾명빆 `answer_quality_issues=[]`.
- [x] qv7_009??`718`?? `9`以? 紐⑸줉 `5`媛? judge `5/5`, ?덉쭏 ?뚮옒洹??놁쓬?쇰줈 ?좎??먮떎.
- [x] aggregate??`rows=47`, `scoreboard_rows=1`, `diagnostic_only_rows=46`.
- [ ] L91? source-exposed?대?濡?fresh validation?쇰줈 ?곗? ?딅뒗??
- [ ] L91? ?듬? ?뺤떇 媛쒖꽑 ?꾨낫?댁? ?띾룄 媛쒖꽑 claim? ?꾨땲?? L85 topk8蹂대떎 ?됯퇏 吏?곗씠 ?쎄컙 ?먮━怨?qv7_006 tail??`28.81s`??
- [ ] ?ㅼ쓬 ?꾨낫 ?묒뾽: plain-language hint trigger false-positive ?뚯뒪???먮뒗 qv7_006 tail latency 遺꾩꽍.

## 2026-07-07 L92 plain-language hint trigger guard

- [x] `PLAIN_LANGUAGE_NEGATION_MARKERS`瑜?異붽??덈떎.
- [x] positive trigger fixture? negated-request no-trigger fixture瑜?異붽??덈떎.
- [x] fixture pack? `25/25` ?듦낵?덈떎.
- [ ] L92???깅뒫 ?먯닔媛 ?꾨땲??trigger safety guard濡?蹂닿퀬?쒕떎.

## 2026-07-07 L93-L95 sensitive-info preemptive abstention speed loop

- [x] qv7_006 tail latency媛 generation ?④퀎 ??퉬?몄? trace濡??뺤씤?덈떎.
- [x] `_preempt_sensitive_abstention_answer`瑜?異붽??덈떎.
- [x] 誘쇨컧/湲덉??뺣낫 + 異붿젙/?덉쐞?앹꽦 ?뺣컯???덉쓣 ?뚮쭔 preempt?섍퀬, ?뺤긽 boundary ?붿껌? preempt?섏? ?딅뒗 fixture瑜?異붽??덈떎.
- [x] fixture pack? `27/27` ?듦낵?덈떎.
- [x] `questions_v7_l94_sensitive_preempt_probe.json`??留뚮뱾怨?diagnostic-only濡??깅줉?덈떎.
- [x] L94 two-case probe?먯꽌 qv7_006 latency `3.27s`, qv7_012 latency `0.86s`, generation cost `$0.0`???뺤씤?덈떎.
- [x] L95 full v7 source-exposed diagnostic?먯꽌 EDD `98.54`, latency `14.44s`, ?덉쭏 ?댁뒋 `0/12`瑜??뺤씤?덈떎.
- [ ] L95??source-exposed diagnostic?대?濡?fresh validation?쇰줈 ?곗? ?딅뒗??
- [ ] ?ㅼ쓬 ?④퀎??preempt trigger false-positive ??吏덈Ц???먮뒗 fresh validation ?꾨낫 ?뺣낫?대떎.

## 2026-07-07 L96 preempt trigger false-positive correction

- [x] broad `異붿젙` preempt marker瑜?`異붿젙??/`異붿젙?댁꽌`/`異붿젙 媛?? ?깆쑝濡?醫곹삍??
- [x] `異붿젙湲덉븸` ?뺤긽 議곕떖 ?⑹뼱媛 preempt?섏? ?딅뒗 fixture瑜?異붽??덈떎.
- [x] fixture pack? `28/28` ?듦낵?덈떎.
- [ ] L96? trigger safety guard?대ŉ ???깅뒫 ?먯닔濡??곗? ?딅뒗??


## 2026-07-07 L97-L99 deadline package follow-up

- [x] L97 no-API guard fixture pack expanded to `33/33` without paid calls.
- [x] qv8 deadline diagnostic set frozen and registered as `diagnostic_only`.
- [x] L98 qv8 baseline run completed under budget gate: raw EDD `95.81`, observed cost `$0.126294`.
- [x] L99 evaluator correction added for sensitive victim-story refusals; recomputed qv8 EDD `97.81`, fixtures `34/34`.
- [x] Final report draft and graph assets created under the 20260707_122145 run folder.
- [ ] Do not promote qv8 to strict validation. Keep it as deadline diagnostic evidence.
- [ ] Next loop should target qv8 latency tail: q20260707_a01, a02, a06, a07.
- [ ] Add field-level scoring before using official-contact plus personal-contact mixed questions in aggregate metrics.
- [ ] If a truly unused validation set is needed, freeze it before looking at answers and do not tune against it.

## 2026-07-07 L100-L101 qv8 latency-tail follow-up

- [x] Create a five-case qv8 latency-tail diagnostic set and register it as diagnostic-only.
- [x] Compare top8 control, top5, and concise prompt candidates on the five-case tail slice.
- [x] Reject prompt-wide concision because abstention accuracy collapsed to `0.0`.
- [x] Run full-qv8 top5 confirmation after the five-case top5 improvement.
- [x] Record that full-qv8 top5 improved latency to `14.284s` but kept abstention at `0.8`.
- [ ] Do not adopt global top5 yet; qv8_a11 unsupported award-result refusal still needs a focused repair.
- [ ] Build an unsupported-result refusal-shape probe around qv8_a11.
- [ ] Decide whether qv8_a11 is a model-answer issue, an abstention-detector granularity issue, or both.
- [ ] Keep mixed official/private contact scoring out of aggregate EDD until a field-level scorer exists.

## 2026-07-07 L102-L103 award-result boundary follow-up

- [x] Add no-API unsupported award-result fixtures and preserve evaluation-criteria caveat answers.
- [x] Register `questions_v8_l102_award_result_probe.json` as diagnostic-only.
- [x] Verify single qv8_a11 top5 guard probe: abstention `1.0`, latency `2.44s`.
- [x] Verify full qv8 top5 after guard: EDD `98.71`, abstention `1.0`, latency `13.656s`.
- [ ] Do not promote L103 to strict validation.
- [ ] Build a non-qv8 unsupported-result mini-set to test guard false positives and generalization.
- [x] Consider a separate sensitive victim-story preempt loop because qv8_a12 still reached `22.06s` in L103.

## 2026-07-07 L104-L105 victim-story preempt follow-up

- [x] Read qv8_a12 trace evidence and separate measurement repair from generation-time repair.
- [x] Add narrow victim-story / personal-name preempt markers and a support-center false-positive boundary fixture.
- [x] Register `questions_v8_l104_victim_story_probe.json` as diagnostic-only.
- [x] Verify fixture pack: `41/41`.
- [x] Verify single qv8_a12 top5 preempt probe: abstention `1.0`, latency `2.12s`.
- [x] Verify full qv8 top5 after award+victim guards: EDD `99.13`, abstention `1.0`, latency `11.813s`.
- [x] Record L105 as the best qv8 diagnostic row but not strict validation.
- [ ] Build a non-qv8 unsupported-result and sensitive-story mini-set to test generalization and false positives.
- [ ] Add field-level scoring for mixed official-contact / private-contact questions before those rows influence aggregate EDD.
- [ ] Stop additional qv8-only score chasing unless a new failure class appears; otherwise the loop is likely measuring overfit.

## 2026-07-07 L106-L107 non-qv8 guard and field-scoring gate

- [x] Run four-role review after L105: non-qv8 probe design, false-positive red review, field scorer design, and report/promotion gate.
- [x] Patch guard marker boundary so broad guessing words no longer count as sensitive fields by themselves.
- [x] Expand no-API guard fixtures from `41/41` to `49/49`.
- [x] Add deterministic field-level contact/privacy scorer.
- [x] Verify field scorer calibration: expected case outcomes `4/4`.
- [x] Wire optional `field_score` into eval detail output and worker issue summaries without changing EDD.
- [x] Create `questions_l106_nonqv8_guard_generalization_diagnostic_draft.json` and register it diagnostic-only.
- [x] Pass team output smoke for the L106-L107 run.
- [ ] Assign real corpus-backed target projects/orgs to the L106 draft cases before any scored run.
- [ ] Freeze a concrete L108 mini-set before reading answers.
- [ ] Run L108 under budget gate as diagnostic-only unless it is truly untouched and pre-registered.
- [ ] Report field-level metrics beside EDD, not inside EDD.

## 2026-07-07 L108-L112 non-qv8 grounded guard and field-score cleanup

- [x] Create a concrete corpus-backed L108 mini-set and register it diagnostic-only.
- [x] Run L108 no-judge baseline under the local budget gate.
- [x] Split L108 false-abstention causes into measurement artifact, real over-refusal, and official/private field boundary.
- [x] Create L109 scored diagnostic copy with stricter field expectations and register it diagnostic-only.
- [x] Fix L109 marker corruption and record it as a measurement defect, not a model failure.
- [x] Add partial-answer prompt hint for explicit caveat questions.
- [x] Add a narrow sensitive post-trim exception for supported partial answers with unavailable-field caveats.
- [x] Add `evaluation_criteria_partial_answer_not_trimmed`; guard fixtures pass `51/51`.
- [x] Extend field scorer with `required_all_markers` and `refusal_evidence_markers`.
- [x] Reclassify official/private contact's private side as `withhold` when the correct behavior is to avoid leakage, not necessarily repeat every private-contact token.
- [x] Remove generic `媛쒖씤 ?곕씫泥?` from leak markers; keep concrete phone/email leak markers.
- [x] Confirm L112 current-code diagnostic: false abstention `0.0`, abstention accuracy `1.0`, field_score issues `{}`, latency `7.184s`, observed cost `$0.040586`.
- [x] Write L108-L112 report, CSV, and SVG under the L109 run folder.
- [ ] Do not compare L112 no-judge EDD `60.0` to judged EDD rows.
- [ ] Do not promote L108-L112 to strict validation; it is source-exposed and failure-family-driven.
- [ ] If continuing on the same 8 cases, use them for latency profiling only, not stronger performance claims.
- [ ] For a real next performance claim, build a new untouched mini-set before reading answers.
- [ ] Consider a top_k5/top_k8 latency comparison on the clean L112 cohort only if it stays under the budget gate and the report keeps the diagnostic-only label.

## 2026-07-07 L113-L115 two-branch follow-up

- [x] Create `questions_v9_source_inspected_mini_diagnostic_frozen.json` before answer execution.
- [x] Register v9 as `source_inspected_v9_mini_diagnostic_frozen`, `diagnostic_only`.
- [x] Run L113 same-cohort L112 top_k latency profile in no-judge mode.
- [x] Reject L113 top5/top8/top12 as latency improvements because none beat L112 `7.184s`; top12 produced a severe q002 tail.
- [x] Run L114 v9 source-inspected first execution with judge enabled.
- [x] Record L114 raw separately: EDD `93.42`, abstention accuracy `0.5`, latency `14.934s`.
- [x] Add childcare/person-name/inspection-result refusal detector fixture; guard fixtures pass `52/52`.
- [x] Recompute saved L114 as L115 measurement correction: EDD `98.42`, abstention accuracy `1.0`.
- [x] Write two-branch report, CSV, and SVG.
- [ ] Do not promote v9 to strict held-out validation because it was generated from local source inspection.
- [ ] Treat L115 as measurement correction, not a new model run.
- [ ] Investigate q001 metadata usefulness gap: exact amount/deadline were expected by the question proposal, but the answer gave `20??誘몃쭔` and deadline unavailable.
- [ ] Before a future first-run claim, confirm that generated questions do not depend on CSV-only metadata unless that metadata is exposed to the RAG answer context.
- [ ] Avoid further top_k tuning on L112 unless the goal is strictly per-case tail profiling.

## 2026-07-07 L116 v10 realistic user-intent taxonomy gate

- [x] Create a v10 taxonomy run scaffold with four proposal roles.
- [x] Collect intent taxonomy, gate design, corpus feasibility, and red/report proposals.
- [x] Write `analysis/v10_realistic_intent_taxonomy_gate_report.md`.
- [x] Write `analysis/v10_realistic_intent_taxonomy.json`.
- [x] Record that L116 is taxonomy/gate design only and has no EDD point.
- [ ] Before creating v10 questions, assign `answerability_source` to every candidate.
- [ ] Check exposure registry and avoid promoting source-inspected cases as strict validation.
- [ ] Confirm body-visible support for exact budget/deadline cases.
- [ ] Run retrieval-only preview before any paid or judged answer run.
- [ ] Freeze v10 question file and manifest before answer inspection.
- [ ] Preserve raw first execution before any repair or measurement correction.
- [ ] Keep sidecar blockers beside EDD: exact-value usefulness, CSV-only metadata, mixed-field over-refusal, project mixing, privacy leakage, and latency tail.

## 2026-07-07 L117 question bank gap review

- [x] Inspect `C:\Users\peedi\Downloads\rfp_question_bank.md`.
- [x] Inspect `C:\Users\peedi\Downloads\rfp_question_bank.csv`.
- [x] Compare the 95-row bank against the exposure registry and L116 taxonomy.
- [x] Cut pattern-known rows instead of running the full bank.
- [x] Keep all rows that add a new or undercovered signal without using 12-16 as a hard cap.
- [x] Write `eval/question_bank_gap_review_20260707.csv`.
- [x] Write `eval/question_bank_gap_review_20260707.json`.
- [x] Write `eval/question_bank_gap_review_20260707.md`.
- [x] Record that 68 rows are diagnostic candidates and 27 rows are cut for now as pattern-known.
- [ ] Build lane-specific frozen files from the kept candidates.
- [ ] Choose concrete seed projects for selected-project contract/technical/follow-up rows.
- [ ] Add sidecar blockers for exact-value availability, context loss, unsupported guarantee, over-refusal, overlong persona answer, and missing instrumentation.
- [ ] Keep metadata/corpus analytics and RAG ops instrumentation outside ordinary answer-generator EDD.
- [ ] Register each lane file before answer execution and preserve the raw first run.

## 2026-07-07 L118 64-case shard preparation

- [x] Remove four over-scoped/harness-heavy rows from the 68 kept candidates: `Q092`, `Q093`, `Q094`, `Q095`.
- [x] Split the remaining 64 into four 16-case shards.
- [x] Write `eval/question_bank64_shards_20260707.json`.
- [x] Write `eval/question_bank64_shards_20260707.csv`.
- [x] Write `eval/question_bank64_shards_20260707.md`.
- [x] Write `eval/question_bank64_shards_20260707.manifest.json`.
- [x] Create the L118 run folder and ledger.
- [x] Collect four shard review contracts.
- [x] Run team output smoke: pass with `worker_output_count=4`.
- [x] Record that this was preparation only: no answer generation, no judge run, no paid API/model call.
- [ ] Build runnable manifests for each shard with explicit seed projects and seed turns.
- [ ] Preflight source visibility for exact fields, selected-project fields, and corpus-wide metadata fields.
- [ ] Decide whether `Q090-Q091` have retrieval/citation trace artifacts; if not, mark them blocked or move them to a later instrumentation-only run.
- [x] For Shard A, keep `Q033-Q035` in a separate ordinary comparison subtotal.
- [ ] For Shard B/C/D, report sublane scores beside EDD rather than one merged score.

## 2026-07-07 L119 runnable manifest and seed gates

- [x] Create L119 run folder and ledger.
- [x] Write `eval/question_bank64_runnable_manifest_20260707.json`.
- [x] Write `eval/question_bank64_runnable_manifest_20260707.csv`.
- [x] Write `eval/question_bank64_runnable_manifest_20260707.md`.
- [x] Write `eval/question_bank64_runnable_manifest_20260707.manifest.json`.
- [x] Add a 14-seed catalog for selected-project, duplicate-title, wrong-org, missing-budget, and persona/usefulness rows.
- [x] Add metadata sidecar answer keys for whole-corpus and CSV-visible questions.
- [x] Mark ordinary EDD subtotal candidates separately from sidecar/trace-only rows: `49` ordinary EDD candidates, `15` sidecar or trace-only rows.
- [x] Mark `Q090-Q091` as `blocked_until_trace_wrapper`.
- [x] Add no-cross-seed synthesis policy for `Q038-Q045`.
- [x] Add sparse-field not-found fallback policy for `Q046-Q050`.
- [x] Add keyword-sidecar false-positive warning for `Q006-Q011` and `Q065`.
- [x] Preserve raw shard reviews under `worker_outputs/raw_reviews`.
- [x] Wrap worker outputs into `parallel_team_worker_output.v1` after initial smoke failure.
- [x] Rerun worker smoke: pass with `worker_output_count=4`.
- [ ] Build a retrieval trace export wrapper before running `Q090-Q091`.
- [ ] Build a metadata sidecar runner for `Q001-Q012`, `Q065`, `Q054`, `Q055`, and `Q076`.
- [ ] Build a selected-project scripted runner that binds one seed per run for `Q038-Q053`, `Q067`, `Q069-Q073`, and `Q077-Q089`.
- [ ] Before any 64-case answer execution, freeze an execution batch file that excludes blocked trace rows or labels them as trace-only blocked.
- [ ] Report future results by sublane: metadata sidecar, ordinary EDD, selected-project contract, selected-project technical, follow-up memory, unsupported boundary, contextual usefulness, business recommendation, and trace audit.
- [ ] Keep the first answer run raw; any fix after inspecting failures must be labeled targeted recheck, not fresh validation.

## 2026-07-07 L120 no-API metadata sidecar runner

- [x] Add `scripts/run_metadata_sidecar.py`.
- [x] Run metadata sidecar execution without API/model calls.
- [x] Generate `metadata_sidecar_results.json`.
- [x] Generate `metadata_sidecar_results.csv`.
- [x] Generate `metadata_sidecar_results.md`.
- [x] Generate `metadata_sidecar_strictness.svg`.
- [x] Generate per-case sidecar answer previews under `sidecar/answers/`.
- [x] Separate exact sidecar rows from candidate/taxonomy rows.
- [x] Fix the first-run `Q070` bookkeeping bug by resolving `preflight_answer_key_ref` instead of assuming `case_id == sidecar_key_id`.
- [x] Add `sidecar_key_id` and explicit `Q070 -> Q006` alias explanation.
- [x] Run `python -m py_compile scripts/run_metadata_sidecar.py`.
- [x] Collect two standard review contracts.
- [x] Run worker output smoke: pass with `worker_output_count=2`.
- [ ] Add optional row-level evidence review for candidate keyword rows before any semantic-accuracy claim.
- [ ] Build selected-project scripted runner next.
- [ ] Build trace wrapper for `Q090-Q091` later; do not let L120 sidecar success hide that blocker.

## 2026-07-07 L121 selected-project scripted batch

- [x] Add `scripts/build_selected_project_batch.py`.
- [x] Generate primary multiturn selected-project batch.
- [x] Generate resolved one-turn selected-project smoke batch.
- [x] Generate secondary diagnostic variants.
- [x] Add dynamic `S_INCHEON_JOB_ISP` seed for `Q073`.
- [x] Set `expect_abstention=true` for unsupported-boundary rows `Q075`, `Q077`, `Q079`, `Q080`, `Q081`.
- [x] Record call-count tradeoff: `71` multiturn calls vs `35` resolved-one-turn calls if executed.
- [x] Run full JSON parse checks on all generated batch files.
- [x] Run `python -m py_compile scripts/build_selected_project_batch.py`.
- [x] Collect contract, technical, and follow-up/persona review contracts.
- [x] Record technical-review capacity fallback and successful replacement worker.
- [x] Run worker output smoke: pass with `worker_output_count=3`.
- [x] Build sparse-field not-found/padding guard before scoring secondary technical variants.
- [ ] For the next cheap execution, run a small no-judge resolved-one-turn smoke, not the full 71-call multiturn batch.
- [ ] For any memory/follow-up claim, use the multiturn primary batch and preserve the raw first answer run.
- [ ] Keep secondary variants diagnostic-only and subtotaled separately.

## 2026-07-07 L122 sparse-field guard and new-question gap insight

- [x] Record the grouped insight that the new bank questions exposed evaluation/runner gaps, not only model-answer gaps.
- [x] Add `scripts/run_sparse_field_guard.py`.
- [x] Run the no-API sparse-field guard against the L121 secondary technical ADD variants.
- [x] Prefer raw HWP/PDF text over CSV-only text for sparse/not-found source visibility checks.
- [x] Record the source-basis reversal: CSV-only text showed `4` visible groups and `27` not-found groups, while raw text showed `31` visible groups and `0` not-found groups.
- [x] Preserve L122 outputs under `eval/parallel_runs/20260707_153900_L122-sparse-field-guard-and-new-question-gap-insight-recordi/analysis/sparse_field_guard/`.
- [x] Collect two proposal reviews and one local fallback review contract.
- [x] Run team output smoke: pass with `worker_output_count=3`.
- [x] Run JSON parse checks for ledger and sparse-field artifacts.
- [x] Add a scoreboard/aggregator guard that forces all `secondary_variant` rows to diagnostic-only even if their batch JSON has `ordinary_edd_candidate=true`.
- [x] Search for a truly sparse technical seed under raw source text before claiming a sparse-field not-found test.
- [ ] Do not report L122 as EDD or answer-quality improvement; it is a gate/readiness and source-basis correction loop.

## 2026-07-07 L123 secondary-variant scoreboard guard

- [x] Patch `scripts/aggregate_parallel_eval.py` so secondary variant question files are forced to `rank_scope=diagnostic_only`.
- [x] Detect secondary rows by filename markers such as `secondary_variants` and by payload markers such as `variant_claim`, secondary `diagnostic_label`, or `promotion_blocker`.
- [x] Build a synthetic no-API aggregate smoke row with complete metrics and `edd_score=99.99`.
- [x] Verify the synthetic secondary row produces `scoreboard_rows=0` and `diagnostic_only_rows=1`.
- [x] Verify the diagnostic reason is `quality_status=diagnostic_secondary_variant`.
- [x] Run `python -m py_compile scripts\aggregate_parallel_eval.py scripts\run_sparse_field_guard.py`.
- [x] Run worker output smoke for the L123 run: pass with `worker_output_count=2`.
- [x] Search for a truly sparse technical seed under raw source text before a sparse not-found answer run.
- [ ] If the next answer run uses L121 secondary variants, report them only as diagnostic stress rows.

## 2026-07-07 L124 raw-source sparse technical seed scan

- [x] Add `scripts/find_sparse_technical_seeds.py`.
- [x] Scan raw HWP/PDF text for technical sparse seed candidates.
- [x] Reframe the recommendation rule from "very few visible fields" to "many absent fields" after the first scan returned zero candidates.
- [x] Scan result: `97` technical candidate docs, `31` field groups, `5` recommended sparse seed candidates, all using `raw_file_text`.
- [x] Top candidate: `DOC073` ?щ떒踰뺤씤?꾩떆?꾨Ъ?꾩썝?뚯궗臾닿뎅 / ?곗쫰踰??ㅻⅤ湲곗쫰?ㅽ깂 湲고썑蹂?붾????ㅻ쭏??愿媛쒖떆?ㅽ뀥 援ъ텞?ъ뾽, visible `15`, absent `16`.
- [x] Second candidate: `DOC051` 湲곗큹怨쇳븰?곌뎄??/ 2025?꾨룄 以묒씠?④??띻린??洹뱀??⑥떆?ㅽ뀥 ?댁쟾 ?⑹뿭, visible `16`, absent `15`.
- [x] Third candidate: `DOC025` ?쒓뎅?섏옄?먭났??/ ?⑹씤 泥⑤떒 ?쒖뒪?쒕컲?꾩껜 援???곕떒 ?⑹닔怨듦툒?ъ뾽 ??뱀꽦議곗궗 諛?湲곕낯怨꾪쉷 ?섎┰ ?⑹뿭, visible `18`, absent `13`.
- [x] Run worker output smoke for L124: pass with `worker_output_count=2`.
- [x] Build a small frozen sparse diagnostic question file from the top 2-3 L124 candidates.
- [x] Preserve that first answer run raw and label it diagnostic-only unless it is preregistered as a new untouched validation.

## 2026-07-07 L125 frozen sparse diagnostic question set

- [x] Build `eval/parallel_runs/20260707_155335_L125-frozen-sparse-diagnostic-question-file/questions/questions_l125_sparse_field_diagnostic_frozen.json` (6 cases from `DOC073`, `DOC051`, `DOC025`).
- [x] Generate `questions_l125_sparse_field_diagnostic_frozen.csv`, `.md`, `.manifest.json`.
- [x] Keep all 6 cases diagnostic-only (`claim_use=diagnostic_only_sparse_field_not_found_probe`).
- [x] Execute a tiny no-judge diagnostic-only run on the frozen 6-case set and record:
  - mixed lane outcomes
  - padding_trap lane outcomes
  - hard boundary leakage by case
- [x] Execute scored diagnostic follow-up split into prompt lane (L126) and retrieval lane (L127); keep both diagnostic-only.
- [x] Fix aggregation gate so diagnostic-only question files are excluded from scoreboard even when registry metadata is missing.
- [x] Add `scripts/audit_sparse_answer_runs.py` for sparse-field answer-shape audit.
- [ ] Add field-level expectations for L125 sparse cases so present-field recovery and not-found correctness are scored directly rather than inferred from generic relevance.
- [ ] Revisit binary `is_abstention` for mixed sparse answers; partial answer plus explicit not-found caveat should not be counted as global abstention.
- [ ] If true padding leaks remain after field-level scoring, add hardening rule for unsupported-field fabrication in sparse questions and rerun 6-case diagnostics.

