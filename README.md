# music_analysis_batch_language

[中文](#music_analysis_batch_language中文版介绍) English

This is a language that I designed to allow you to quickly enter compositional analyses of key, chords, chord progressions, explanations of compositional techniques, etc.  
The chord progressions (usually roman numerals) are automatically aligned with the corresponding chords.  
You can specify which chord is currently being played. You can also set your own spacing (number of spaces) between adjacent chords.  
You can also set the character of the bar line, etc. Next I will explain the basic syntax of the language.  
First, the syntax for inputting the tonicity is
```
k.Tone
```
The tonality can be anything you want to write, such as A major, A major, etc., and the above syntax will be generated
```
key: tonality
```
In addition, you can also customize the beginning of the tonic with the syntax
```
k!The beginning of the tonality
```
This allows you to customize the content before the tonic, which defaults to ``key: ``

Then you can enter the chord progression and the corresponding chord progressions (usually roman numerals) for the composition analysis, with the syntax  
```
current bar number; chord 1; chord 2; chord 3; ... $ chord steps 1; chord steps 2; chord steps 3;... $ Other parameter customization
```
First, the first argument is the number of bars, which can be any number, integer, decimal, fraction (actually it can be any string)  
Then use `;` to separate it from the chord part, then every two chords are also separated by `;`, you can write as many as you want, and then use `$` as the ending  
After that you can write the content of the chord progression, again separated by `;` and then also ending with `$`, followed by other parameter configurations.  
If you want to display the chord you are currently playing, the syntax is to add `! `.  
For example, if you want to display the currently playing chord 2, then you can write
```
Current bar number; chord 1; ! chord2;chord3;... $ chord step 1; chord step 2; chord step 3;... $ other parameter customization
```
It's worth mentioning here that my language is designed in such a way that the last chord name with `! ` in front of the chord name as a display of the chord currently being played.  
So you can prefix multiple chords with `! `, you just need to make sure that the last `! ` is in front of the chord you want to display at the moment.


Possible parameter configurations.  
* c=textual description of the composition (you can add a textual description of the composition analysis of the chord of the current bar)

* i=spacing (you can set the number of spaces between each chord)

* b=whether to display the current bar number (if T, the current bar number is displayed (the first argument is displayed as the current bar number), if F, the current bar number is not displayed (the first argument is displayed as the first chord))

* s=bar line character (you can set the bar line character, the default is `|`)

* a=character of the chord currently being played (you can set the character of the chord currently being played, the default is `→`)

* ca=whether to show chord steps (if T, then show chord steps, if F, then don't show chord steps)

Next I'll demonstrate how this works.
```
1;Cmaj7;Dm11;G9sus;Cmaj9#11$IM7;ii11;V9sus;IM9#11
```
It is possible to generate
```
1
Cmaj7 | Dm11 | G9sus | Cmaj9#11
IM7     ii11   V9sus   IM9#11
```
Each chord and chord step is automatically aligned, saving you the trouble of laying out the chords yourself.  
If it is to show the chord currently being played, then you can write
```
1;Cmaj7;!D7;Fmaj7;Cmaj9(omit 3)$IM7;II7;IVM7;IM9
```
can generate
```
1
Cmaj7 | → D7 | Fmaj7 | Cmaj9(omit 3)
IM7       II7  IVM7    IM9
```
And there are various parameter configurations to customize the generated content yourself, for example, if you want to add a composition note, you can write
```
1;Cmaj7;!D7;Fmaj7;Cmaj9(omit 3)$IM7;II7;IVM7;IM9$c=2nd dominant seventh chord in C major borrowed from the parallel C lydian mode
```
can generate
```
1
Cmaj7 | → D7 | Fmaj7 | Cmaj9(omit 3)
IM7       II7  IVM7    IM9
2nd dominant seventh chord in C major borrowed from the parallel C lydian mode
````
If you want to enter a composition note with multiple lines, just type a line break `\n` at the time of the line break.  
If you do not want to display the content of the chord progressions of the compositional analysis, you can simply leave them out, the
```
1;Cmaj7;!D7;Fmaj7;Cmaj9(omit 3)
```
can generate
```
1
Cmaj7 | → D7 | Fmaj7 | Cmaj9(omit 3)
```
If you don't want to display the content of the chord steps of the composition analysis, but you need to configure the parameters, for example, you don't want to display the number of current bars.  
then you can write `. ` or `~` or just leave it blank.
```
Cmaj7;!D7;Fmaj7;Cmaj9(omit 3)$$b=F
```
can generate
```
Cmaj7 | → D7 | Fmaj7 | Cmaj9(omit 3)
```
Next I demonstrate the effect of some parameter configurations, such as changing the interval that
```
1;Cmaj7;!D7;Fmaj7;Cmaj9(omit 3)$IM7;II7;IVM7;IM9$i=2
```
can generate
```
1
Cmaj7 | → D7 | Fmaj7 | Cmaj9(omit 3)
IM7       II7  IVM7    IM9
```
The number of spaces to the bar line between each two chords is now 2.  
Showing the current tonicity of
```
k.A major
```
can generate
```
key: A major
```
which sets the current tonic preceding the
```
k!current tonality: 
```
and then write
```
k.A major
```
can generate
```
Current key: A major
```
Any number of lines can be left blank between the analysis of each composition in two different bars, and the result is generated with as many lines empty, e.g.
```
1;!Cmaj7;D7;Fmaj7;Cmaj9(omit 3)$IM7;II7;IVM7;IM9

2;Cmaj7;!D7;Fmaj7;Cmaj9(omit 3)$IM7;II7;IVM7;IM9
```
can generate
```
1
→ Cmaj7 | D7 | Fmaj7 | Cmaj9(omit 3)
  IM7     II7  IVM7    IM9

2
Cmaj7 | → D7 | Fmaj7 | Cmaj9(omit 3)
IM7       II7  IVM7    IM9
```
In addition, the current bar count can actually be written `+ the distance relative to the previous bar `, and the unit of this distance is also bars.  
For example, if the first current bar is 1, and then 1/2 bar later the next chord is played, then you can write `+1/2`.  
This syntax is actually directly parsable in the piano software I wrote, Ideal Piano, and I wrote the syntax parsing function logic specifically  
Ideal Piano supports both absolute and relative bar counts, and can directly read the above  
It is possible to read the composition analysis as generated above and display the composition analysis by bar in real time while playing the midi file in the software.

Batch syntax generation for a few chords:  
`[n*];chord name 1; chord name 2; chord name 3;... $ chord function 1; chord function 2; chord function 3;... `  
`[n1,n2,n3,...] ;chord name1;chord name2;chord name3;... $ chord function 1;chord function 2;chord function 3;... `  
The n\* in the brackets here sets all the bars of the current line to n. n can be both absolute and relative bars, and relative bars are usually used more often. You can also write n1,n2,n3 in parentheses to set the number of bars for each chord in the current line in turn.

I have written an editor specifically for this language, which writes code on the left and generates the corresponding composition content in real time on the right, as well as syntax highlighting and other functions.

# music_analysis_batch_language中文版介绍

中文 [English](#music_analysis_batch_language)

这是我设计的一门可以快速输入作曲分析内容的语言，可以对你输入的调性，和弦，和弦级数以及作曲手法的讲解等等  
进行批量排版，让你用很简洁的语法输入漂亮的作曲分析，和弦级数(一般为roman numerals)会自动与对应的和弦  
进行对齐，并且可以指定当前正在演奏的是哪一个和弦。也可以自己设定相邻和弦之间的间隔（空格的数量），  
也可以设置小节线的字符等等。接下来我讲解一下这门语言基本的语法。  
首先是输入调性，语法为：
```
k.调性
```
调性可以是任意的你想写的表示调性的内容，比如A大调，A major等等，以上的语法就会生成
```
key: 调性
```
此外，也可以自己定制调性的开头内容，语法为
```
k!调性开头的内容
```
这样就可以自己定制调性前的内容，默认为`key: `

然后是输入和弦进行以及对应的作曲分析的和弦级数(一般为roman numerals)，语法为  
```
当前小节数;和弦1;和弦2;和弦3;...$和弦级数1;和弦级数2;和弦级数3;...$其他的参数定制
```
首先，第一个参数是小节数，可以是任意的数字，整数，小数，分数都可以（实际上可以是任意的字符串）  
然后用`;`与和弦部分间隔开，然后每两个和弦之间也是使用`;`分隔，可以写任意多个，然后使用`$`作为结束，  
后面可以写和弦级数的内容，同样也是使用`;`分隔，然后也是以`$`作为结束，后面可以跟着其他的参数配置。  
如果要显示当前正在演奏的和弦，语法是在想要显示当前正在演奏的和弦名称前面加上`!`，  
比如想要显示当前正在演奏和弦2，那么可以写
```
当前小节数;和弦1;!和弦2;和弦3;...$和弦级数1;和弦级数2;和弦级数3;...$其他的参数定制
```
这里值得一提的是，我这个语言的设计是会把最后一个有`!`在前面的和弦名称作为显示当前正在演奏的和弦，  
因此你可以在多个和弦前面加上`!`，只需要保证最后一个`!`在你想要在当前显示的和弦前面就行了。


可以使用的参数配置：  
* c=作曲手法的文字说明  (可以加上当前小节的和弦的作曲手法分析的文字说明)

* i=间隔  (可以设定每两个和弦之间的空格数量)

* b=是否显示当前小节数  (如果为T,则显示当前小节数（把第一个参数作为当前小节数显示），如果为F，则不显示当前小节数（第一个参数作为第一个和弦）)

* s=小节线字符  (可以设定小节线的字符，默认为`|`)

* a=当前正在演奏的和弦的字符  (可以设定当前正在演奏的和弦的字符，默认为`→`)

* ca=是否显示和弦级数  (如果为T，则显示和弦级数，如果为F，则不显示和弦级数)

接下来我演示一下具体的实现效果，
```
1;Cmaj7;Dm11;G9sus;Cmaj9#11$IM7;ii11;V9sus;IM9#11
```
可以生成
```
1
Cmaj7 | Dm11 | G9sus | Cmaj9#11
IM7     ii11   V9sus   IM9#11
```
每一个和弦与和弦级数都会自动对齐，省去了自己排版的麻烦。  
如果是要显示当前正在演奏的和弦，那么可以写
```
1;Cmaj7;!D7;Fmaj7;Cmaj9(omit 3)$IM7;II7;IVM7;IM9
```
可以生成
```
1
Cmaj7 | → D7 | Fmaj7 | Cmaj9(omit 3)
IM7       II7  IVM7    IM9
```
而且还有各种参数配置可以自己定制生成的内容，比如想要加上作曲说明，可以写
```
1;Cmaj7;!D7;Fmaj7;Cmaj9(omit 3)$IM7;II7;IVM7;IM9$c=C大调中借用同主音C lydian调式的2级属七和弦
```
可以生成
```
1
Cmaj7 | → D7 | Fmaj7 | Cmaj9(omit 3)
IM7       II7  IVM7    IM9
C大调中借用同主音C lydian调式的2级属七和弦
```
如果想要输入多行的作曲说明，只需要在换行时打上一个换行符`\n`就行了。  
如果不想显示作曲分析的和弦级数的内容，可以直接不写，
```
1;Cmaj7;!D7;Fmaj7;Cmaj9(omit 3)
```
可以生成
```
1
Cmaj7 | → D7 | Fmaj7 | Cmaj9(omit 3)
```
如果不想显示作曲分析的和弦级数的内容，但是又需要参数配置，比如不想显示当前小节数，  
那么可以在写作曲分析的部分写`.`或者`~`或者直接留空，
```
Cmaj7;!D7;Fmaj7;Cmaj9(omit 3)$$b=F
```
可以生成
```
Cmaj7 | → D7 | Fmaj7 | Cmaj9(omit 3)
```
接下来我演示一些参数配置的效果，比如更改间隔，
```
1;Cmaj7;!D7;Fmaj7;Cmaj9(omit 3)$IM7;II7;IVM7;IM9$i=2
```
可以生成
```
1
Cmaj7  |  → D7  |  Fmaj7  |  Cmaj9(omit 3)
IM7         II7    IVM7      IM9
```
现在每两个和弦之间的到小节线的空格数量都是2了。  
显示当前的调性，
```
k.A大调
```
可以生成
```
key: A大调
```
设定当前的调性前面的内容，
```
k!当前调性: 
```
然后再写
```
k.A大调
```
可以生成
```
当前调性: A大调
```
每两个不同小节的作曲分析之间可以空任意多行，生成的结果也是空一样多的行，比如
```
1;!Cmaj7;D7;Fmaj7;Cmaj9(omit 3)$IM7;II7;IVM7;IM9

2;Cmaj7;!D7;Fmaj7;Cmaj9(omit 3)$IM7;II7;IVM7;IM9
```
可以生成
```
1
→ Cmaj7 | D7 | Fmaj7 | Cmaj9(omit 3)
  IM7     II7  IVM7    IM9

2
Cmaj7 | → D7 | Fmaj7 | Cmaj9(omit 3)
IM7       II7  IVM7    IM9
```
另外，当前小节数实际上可以写`+相对上一个小节的距离`，这个距离的单位也是小节，  
比如第一个当前小节数是1，然后过了1/2个小节开始演奏下一个和弦，那么可以写`+1/2`，  
这种语法实际上在我写的钢琴软件Ideal Piano里面是可以直接解析的，我专门写了语法解析的函数逻辑  
来进行小节数的推算。Ideal Piano同时支持绝对小节数和相对小节数，并且可以直接读取上面的  
生成的内容那样的作曲分析内容并且在软件里播放midi文件的时候按照小节实时显示作曲分析的内容。

批量生成一段几个和弦的语法:  
`[n*];和弦名称1;和弦名称2;和弦名称3;...$和弦功能1;和弦功能2;和弦功能3;...`  
`[n1,n2,n3,...];和弦名称1;和弦名称2;和弦名称3;...$和弦功能1;和弦功能2;和弦功能3;...`  
这里的中括号里的n\*可以把当前行的所有的和弦的小节都设置为n, n可以为绝对小节数和相对小节数，一般使用相对小节数的情况较多。中括号里也可以写n1,n2,n3的格式，对于当前行的每一个和弦的小节数依次进行设置。

我为这门语言专门写了一个编辑器，在左边写代码，右边会实时生成对应的作曲内容，还有语法高亮等功能。

