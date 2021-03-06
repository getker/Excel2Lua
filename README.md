Excel2Lua 基于Python3.X使用
(将据xls、xlsx数据文件转化为lua脚本，作为游戏资源使用)

use [python xlrd2](https://pypi.python.org/pypi/xlrd2)

(使用python xlrd2模块)

(这个脚本是从 https://github.com/zfengzhen/xls2lua 和 https://github.com/luzexi/xls2lua 和 https://github.com/zerospace007/xls2lua-python 继承过来的，我改进了一些东西，使得更适合游戏项目使用。)

(如果你在使用Lua语言，将数据写进Lua文件是最方便的做法。这个脚本将帮助你将数据xls、xlsx文件转化为lua文件，这样你就可以更好的工作了。)

### Excute Example (举例执行命令)
python ./xls2lua.py

### NOTICE:(注意点)
> (sheet名以"OUT_"开头的才会被识别转换，否则将被忽略) <br />
> (第1行无用，是关键字名的介绍描述) <br />
> (第2行必须是关键字名) <br />
> (第3行必须为类型) <br />
> (类型有：none,int,float,string,boolean,intArr,floatArr,stringArr,booleanArr这几种) <br />
> (none表示该列不再导出,intArr表示int数组,floatArr表示float数组,stringArr表示string数组,booleanArr表示bool数组) <br />
> (第1列为int或者string类型的唯一关键字) <br />
> (string类型中"和'会自动用\"和\'替代)
> (空列将会被默认值代替，例如:0,"",false,{})

### Lua script (生成后的Lua文件示例)
```lua
-- this file is generated by program!
-- don't change it manaully.
-- source file: example_building.xls
-- created at: Thu Mar 26 02:53:52 2015

local data = {}

data[1] = { id = 1,  name = "house",  use_money = 1000,  use_food = 2.33,  is_init = true,  defense = 100,  aadd = {1,2,3},  aadddss = {1.23,2,3.23},  ddff = {"sdf","23e","s"},  ffdd = {true,false,true}}
data[2] = { id = 2,  name = "house2",  use_money = 123,  use_food = 336.2,  is_init = true,  defense = 0,  aadd = {1,2,3},  aadddss = {1,2.3445,3},  ddff = {"你好","你在哪"},  ffdd = {true,false}}
data[3] = { id = 3,  name = "",  use_money = 456,  use_food = 222.33665,  is_init = false,  defense = 130,  aadd = {3,2,5},  aadddss = {3,2,2.5},  ddff = {"我在这里啊","你在那","呢"},  ffdd = {false,true}}
data[4] = { id = 4,  name = "farm",  use_money = 100,  use_food = 220.0,  is_init = false,  defense = 200,  aadd = {2,3},  aadddss = {200.3,3,234.23},  ddff = {"df","ssd","dd","dd"},  ffdd = {}}
data[5] = { id = 5,  name = "house5",  use_money = 0,  use_food = 22.1,  is_init = false,  defense = 234,  aadd = {3,6,6,7},  aadddss = {3,6.3,6,7},  ddff = {"ss","d","d","d"},  ffdd = {true,true}}
data[6] = { id = 6,  name = "horse3",  use_money = 200,  use_food = 0,  is_init = false,  defense = 333,  aadd = {},  aadddss = {},  ddff = {"2e","w","e","we"},  ffdd = {false,false,false,false}}

return data

```

### How to use lua with data. (如何使用生成的lua数据)
```lua
local building = require "Building"

print(building[1].name)
```
The console will print "house"
