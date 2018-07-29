# rubiks-cube-NxNxN-solver

## Overview
This is a rubiks cube solver that can solve any size cube, I have tested
up to 17x17x17.  The following table shows the reduction in move counts
as the solver has evolved. This table starts in July 2018, the earlier
releases of the solver had drastically higher move counts, I think it was
over 400 moves the first time I solved a 5x5x5.

| Date | Commit | 4x4x4 | 5x5x5 | 6x6x6 | 7x7x7 | 8x8x8 | 9x9x9 | 10x10x10 |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| 07/16/2018 | [456ddd1](https://github.com/dwalton76/rubiks-cube-NxNxN-solver/commit/456ddd18f761590294b0b28ac1574a2494514917)  | **51** | 105 | **172** | 247 | **376** | 520 | **725** |
| 07/12/2018 | [c9484d9](https://github.com/dwalton76/rubiks-cube-NxNxN-solver/commit/c9484d93cd55ae50bffb658165e2f843ac5c5fe1)  | 60 | 105 | **176** | 247 | 386 | 520 | 743 |
| 07/12/2018 | [5cda2c8](https://github.com/dwalton76/rubiks-cube-NxNxN-solver/commit/5cda2c8e94deba9cecc6b9e87f265b401b3d97a4)  | 60 | 105 | 181 | **247** | **386** | **520** | 743 |
| 07/08/2018 | [9c13b16](https://github.com/dwalton76/rubiks-cube-NxNxN-solver/commit/9c13b16dbea8abd0581dfaa0abeb4960c54010a4)  | 60 | 105 | 181 | **257** | **403** | **531** | **743** |
| 07/07/2018 | [e876493](https://github.com/dwalton76/rubiks-cube-NxNxN-solver/commit/e87649306139adebdc86ba1880b1e0c0e9265c5a)  | 60 | 105 | **181** | **272** | 408 | 556 | 768 |
| 07/04/2018 |   | 60 | 105 | 200 | 278 | 408 | 556 | 768 |

Solving a 2x2x2 takes around 9 moves while solving a 3x3x3 takes around 20 moves but
I am not working on those solvers so I did not include them in the table above.

I am working on bringing this down but these are the memory requirements for running the solver

| Size | Memory | --min-memory Memory |
| ------ | ------ | ------ |
| 4x4x4 | 415M | 300M |
| 5x5x5 | 450M | 150M |
| 6x6x6 | 2.7G | 1.2G |
| 7x7x7 | 3.8G | 4.0G |
| NxNxN | 4.2G | 4.2G |


## Install

### Install 3x3x3 solver
The kociemba solver is required to solve the larger cubes that have been
reduced to 3x3x3.

```
$ git clone https://github.com/dwalton76/kociemba.git
$ cd ~/kociemba/kociemba/ckociemba/
$ make
$ sudo make install
```

### Install the rubikscubennnsolver python module
```
$ sudo pip3 install pyhashxx
$ cd
$ git clone https://github.com/dwalton76/rubiks-cube-NxNxN-solver.git
$ cd rubiks-cube-NxNxN-solver
$ python3 setup.py build
$ sudo python3 setup.py install
```

## Usage
Run rubiks-cube-solver.py where --state is your cube state in kociemba
order (URFDLB). You must run rubiks-cube-solver.py from the directory that
holds your lookup-table\*.txt files

Example:
```
$ cd ~/rubiks-cube-NxNxN-solver
$ ./usr/bin/rubiks-cube-solver.py --state LFBDUFLDBUBBFDFBLDLFRDFRRURFDFDLULUDLBLUUDRDUDUBBFFRBDFRRRRRRRLFBLLRDLDFBUBLFBLRLURUUBLBDUFUUFBD
```

## History
One of my hobbies is building Lego Mindstorms robots that can solve rubiks cubes. I was able to find solvers for 2x2x2, 3x3x3, 4x4x4 and 5x5x5 but I couldn't find a solver for anything larger than that :(  The solvers that I did find for 4x4x4 and 5x5x5 took quite a bit of RAM (several gigs) but I wanted to be able to run the solver on a Lego Mindstorms EV3 which is 300Mhz and 64M of RAM. So I decided to write my own solver and here we are :)

Here is the thread on speedsolving.com where I first posted looking for solvers. I ended up posting updates to this thread as my solver evolved:
https://www.speedsolving.com/forum/threads/5x5x5-6x6x6-7x7x7-or-nxnxn-solvers.63592/


## Examples
```
2x2x2
=====
reset; ./usr/bin/rubiks-cube-solver.py --state DLRRFULLDUBFDURDBFBRBLFU


3x3x3
=====
reset; ./usr/bin/rubiks-cube-solver.py --state RRBBUFBFBRLRRRFRDDURUBFBBRFLUDUDFLLFFLLLLDFBDDDUUBDLUU


4x4x4
=====
reset; ./usr/bin/rubiks-cube-solver.py --state DRFDFRUFDURDDLLUFLDLLBLULFBUUFRBLBFLLUDDUFRBURBBRBDLLDURFFBBRUFUFDRFURBUDLDBDUFFBUDRRLDRBLFBRRLB


5x5x5
=====
reset; ./usr/bin/rubiks-cube-solver.py --state RFFFUDUDURBFULULFDBLRLDUFDBLUBBBDDURLRDRFRUDDBFUFLFURRLDFRRRUBFUUDUFLLBLBBULDDRRUFUUUBUDFFDRFLRBBLRFDLLUUBBRFRFRLLBFRLBRRFRBDLLDDFBLRDLFBBBLBLBDUUFDDD


6x6x6
=====
reset; ./usr/bin/rubiks-cube-solver.py --state FBDDDFFUDRFBBLFLLURLDLLUFBLRFDUFLBLLFBFLRRBBFDRRDUBUFRBUBRDLUBFDRLBBRLRUFLBRBDUDFFFDBLUDBBLRDFUUDLBBBRRDRUDLBLDFRUDLLFFUUBFBUUFDLRUDUDBRRBBUFFDRRRDBULRRURULFDBRRULDDRUUULBLLFDFRRFDURFFLDUUBRUFDRFUBLDFULFBFDDUDLBLLRBL


7x7x7
=====
reset; ./usr/bin/rubiks-cube-solver.py --state DBDBDDFBDDLUBDLFRFRBRLLDUFFDUFRBRDFDRUFDFDRDBDBULDBDBDBUFBUFFFULLFLDURRBBRRBRLFUUUDUURBRDUUURFFFLRFLRLDLBUFRLDLDFLLFBDFUFRFFUUUFURDRFULBRFURRBUDDRBDLLRLDLLDLUURFRFBUBURBRUDBDDLRBULBULUBDBBUDRBLFFBLRBURRUFULBRLFDUFDDBULBRLBUFULUDDLLDFRDRDBBFBUBBFLFFRRUFFRLRRDRULLLFRLFULBLLBBBLDFDBRBFDULLULRFDBR


8x8x8
=====
reset; ./usr/bin/rubiks-cube-solver.py --state DRRRURBDDBFBRBDDBRRDUFLLURFBFLFURLFLFRBRFUBDRFDFUUBLFFFUULBBFDBDFBUBBFRFLRDLFDRBBLLFRLDFDRBURULDDRFFBFUUBLLFBRUUFDUBRDBBRDFLURUUFFUDLBRRFDUBFLRUUFFRLBFRFLRULUDFRUBBDBFFLBBDFDFLDBFRRRDDLFLBRBFBBRULDDUUBLBBURULLDDLDRUDRBUDRLUULDURLRDFLFULUFLFULRDDDUBBULRBRDFBBLFURRLULUBDDULRFBRFURBRLBRUBULBDDFBUFFBBRLRUUUFRULLBFFRFDDFFDULLDLBUDLLLLUUBBLDLLBBULULBDUDDFUBFLLDLDLFRDUDDBRRFRURRFRRLDDDDRD


9x9x9
=====
reset; ./usr/bin/rubiks-cube-solver.py --state RFBLRUFLLFFLRRBDUDDBBBDUDFRUDUFFFBBFRBRDURBULFUDDFLLLDLFLRDLDBBBUUBRDBBBDFUFRUURULURBURDLFDUBFFDRDFRUBDUBRFLRRLUDLRLFBLBRRLLRDRBRBLURBLLRFRLDDFFFRBFUFURDFRRUDUFDDRRRLFLLUBBLBFDRRDLBRLUUBRDBBUBFLUUFBLLDBFFFBUFBFDBRDDDFLRFFBFFFLFRRDUUDDBUBLUUDURRBDBFFLFURDDLUBULUULULBFBRUBLLDDFLRBDBRFDUUDFURLLUBUFBLULLURDLLLBLFFRLLBLUDRLRDBLDDBRBUDRBLLRDUUUBRRFBFBBULUDUDLDRFUDDDFULRFRBDUDULBRRDBDFFRUUFRRFBDBLFBBDFURLRFDUUFRLUBURFURDDFLDFUBDFRRURRDLUDRBRBDLBFLBBRDLRDBFDUBDFFUBLFLUULLBUDLLLURDBLFFFDFLF


10x10x10
========
reset; ./usr/bin/rubiks-cube-solver.py --state ULBDLDBUFRBBBBBLBFFFDFRFBBDDFDFRFFLDLDLURRBUDRRBFLUDFRLBDURULRUUDBBBUBRURRRLDLRFFUFFFURRFBLLRRFLFUDBDRRDFULLLURFBFUUBDBBDBFLFDFUUFDUBRLUFDBLRFLUDUFBFDULDFRUBLBBBUBRRDBDDDDFURFLRDBRRLLRFUFLRDFDUULRRDULFDUDRFLBFRLDUDBDFLDBDUFULULLLBUUFDFFDBBBRBRLFLUFLFUFFRLLLFLBUDRRFDDUDLFLBRDULFLBLLULFLDLUULBUDRDFLUDDLLRBLUBBRFRRLDRDUUFLDDFUFLBDBBLBURBBRRRFUBLBRBRUBFFDBBBBLBUFBLURBLDRFLFBUDDFFRFFRLBDBDUURBUFBDFFFLFBDLDUFFBRDLBRLRLBFRUUUULRRBDBRRFDLLRRUUBDBDBFDLRDDBRUUUUUBLLURBDFUFLLRDBLRRBBLBDDBBFUDUDLDLUFDDDUURBFUFRRBLLURDDRURRURLBLDRFRUFBDRULUFFDUDLBBUURFDUDBLRRUDFRLLDULFUBFDLURFBFULFLRRRRRFDDDLFDDRUFRRLBLUBU


11x11x11
========
reset; ./usr/bin/rubiks-cube-solver.py --state URBDLBURUBUFDDRBUFDDUBFRDBLRFUUBLDRLBBUBLUFBLRBFFDDLLLDRULRBUDBBRLULBUUUFFRUBLUFUUBRLBLUUDRLDUBLUFDLBLFDBLFRLFLRUDFLLLDFULDRFDFLLFLLRDUUDRFRFFFFBFRBFRFUUBBUULURLULBBLLDDLBUFRURBLFFBRFFRRURFUFLLRUFDBDDDBLRDUBLBRBLRLBUBULLBBFRBFRBLFUDDULLFBRLDUFBBLDBBFBDBDUFFRRDBUUULDDBRFRDBDDRDRFUDBBFULDLUDBLRRFDBLDBLRFFBDLRBUBLDLUDFUFBDDRUDRDFUBLFFRBDFDDDBULBDRBUDBBDRLUFUFFFFDRBDLRLRDRRBFRLUBFFURFRLRLRRLDBLFLFULBURULDURURBLUFUULFBFULULUDLFLLUFLRFLRLFFDRBLLFRDDDBFBFFBLULDLRUDUURLRUFDRFRDURDUFFFULRRUURUDFURBDLBLLDFBBRDRLUBULFRDLRUFUFDBBDLRRURFULBBBBDBRUDUUULFFBUDLRUBRDDRBFDDBURRLURRDDRRRUURURFUBRRBFRFFFBLBLLDURBDRDFDFRRDRDDLDUFUFFLBDLBBDFLLLFDULDBLDRUUFDURBDLUBBLBDDFFDUURBLDRBRLDBLUDRLRFBFDUFUUBFBRDRFFFFUDDDRFFLDFLRRBLDRRDRFBFBLUDBFBBB


14x14x14
========
reset; ./usr/bin/rubiks-cube-solver.py --state FBDRLBLRRURRLDRBDLBURDFDDDRBLBBFBRDLLFDUBLFRLDFUUBFRDBFBBBULFRLBUFLBDDDLLDRBFLLBBLFBFFDFBFDDFRRRBDRRBRBDUFDRLRUDLDFDDURFLBUBBUUDLBRRDUDRDBBBLDBRBBBUFLBLRUURBDDLDRLUFFBLFRLDFBRFLDLBULFFBRLDBDDFLLRFLUBFDFBRLRLFDBLBURLBLFRFBLLDULUDURLBUUULLRRLUBDDLURLLRFURFRFRBDDUBLDFBLUDRLRDRRBLFUFRDUFFRULBLRBBRUFDBUBBBBLDBRBLDDRRFDDBFFUUBRBLFUBBRFUURBFDRLURLRBFUUFUBRUDRBDFBBFURFLFFDRDFUFFULFLUBDFUFFDLRRFRUDUDLBBBDLLLDUFUDRFDBLRRFFLRUFDRFURDLRRDRDLFBRLRLULRFBDLFDRLFRDDFLLDBFBUBBRLLDLFURFRFULUBLUBFLFFBFDFBDUUBURUUUBFUBDLLFLUUUFDUDLUUULDLLUDDBUFRDRULRLLULRULFBLUDFURFLFUBDLLFLFUBUUBBUFLUDUBRDBLFFUUUFDRLRULUDDRLRBLRUUFBRRRRULBDLFBFLDLRDFUBLUBRDDFUULFLDLUBFURRURUBDFFFDLRFFLBRFRDRUDUULURULLDFRBUDRDLFUFULDBLUBFRFBURDLLUUFDURLRDBLFFRFDBFURLFUBLUUUFFRULUBURRURFDDBFUFRBURBBDRFUDDFDLRUURFBBDBDRLUBRRBFDFRDFDLRDUFFUBRRBDBBLDLFDUDDRLFRRRBUUUBRFUFBUFFBRRDRDDBBDRUULDRFRFBUFLFFBLRBFLLLRUDFDRUDLDRLFRLUFLUBRDUFDDLLUDDRBUBBBDRDBBFRBDDRRLRRUUBBUDUDBLDBDFLFRFUBFLFDBBLRLULDBRFBRRLUUURDFFFDBLDUDBRFDDFFUBLUUURBBULFUFUDFBRDLLFURBULULBUDLUFFBDRBRRDBUUULFDURRDFDDLUDBDRBFBUFLULURUFDRFRFBBFBBBDRLBLUDLDRDLLDRRLLDLFBRBRLDUFBDDUDBLDFRFBBBDRDRDDLDRULFFLLFLBLDFLURLBUDFBDLRBLFDFLUDDFUBUBLURBBBLFRLFLBDDBURFFBFRRL


15x15x15
========
reset; ./usr/bin/rubiks-cube-solver.py --state RLURLURBDDULFUUURFLRBLURUBFDBULFLUBBFLDUFBDRFRBRUDFULFRUFLUDFRLFDFLLFDBULURRLBFBUURDULFDFBLRRRLFULLFFFDUULRRRUUUUFDBLDDFFLRDLLUURUBBULUFFURBRRLBBUUBBFDRRBRBRLUDLUDRBFBFULLRRBBFBFRDDDLDDDFRFUFLURUFLBDLUBRLDFRRDBDBFLFUDFLDFFURLFULLDDRURRDLRFLDFLULUUDDRFDRBLRBRBFUFDBDUUDBRRBDFBLBLRBBLBFLLDUBFFFFBDDRLBBBRFDFFUBBDURFLUUDDDRDDLDBRLBULLFLFBRBRBLUDDLRDRDUDFLFRUFLDLBLURDDDRUFDLBRDRLFBDBLDRFBFFBURULUDRRBRDFRFFLULLUBRDRRRDUFRBLFULUBBUFFBRBBFRLFDRRDBLDFRDRDDRLRUULBDURDURFDDLFDUUDBFLBDUFBULFRRDUDUBFBUDBBFUDFUUDLUDDRFDDDFRRRBUDRBFBBULLUFBLRLFLLBRRRRUBDRFLFDFDBLRFLURULULFFBUUUUFDBBLDLUBBRUBBBRBFLULLBLUUULLUBFFDULDFFBFFFUFFDUDRFBUFLDDLURFLRFLRFBUUBLRFDDRULUUUFFRDDBLRDULFURUDDBDLBBUUBFURFRFBRLBUULBLDDDBUBRFFULLUDFFDLDFUBLLBLDFFDDLBDUFUFFLBBBUBULDDFBRRFFLDUDDFRBLRRDDUDLBDBLURBUDBRRLUBBDRFBUFRDRDRBBDULBUFFDRBBDFBUULFFRLLDURRRDFFUUFULDULURLDLUUUDLBBUDLDRFBDBBDLUFBRRFDFLLDLFDBRBBRFUDDDBURDRBUBRUBDUBLDLLDLURLDFDBRUBDLDFRRRBRLULFRFLDRLBUBRUBLFBFDFFLFRFDFLBRULLRBLDRBBFURRRDUUULLULLDLBLBBDFBUUUBRRUFFBRUDBFRDFDLFLFFRFFFFRULDFFDFRUBBBRURBUFLBDFBBBBBRRRLFLFBDRRUFLURDDLRRBRLLFURRURBRFLLLFFURBFULFRFFBLDUUUUBDDUFFDRBRLDDFRBULDDDFFRURUFLDRFLDFBLRUFFUBBDFFDBLLDBDUBDLDLUDFBFLRULRRBDBLRBLDLUURRLLRULDBLBLLRRFDDRBBRBUBDDULDRFBFBBFLUFBLUULDDFDBRLLUBUBBDFBBLBBUBLULDRUDBLRULDUDLUFRRDLLUDDBUFLFLBUFUURFDRDLBURLLRRRULRBFFRRBRFBUBRBUUFRLRDRDLBBRFLLLDDBRFUFRBULFLFDRDDRRDBF
```
