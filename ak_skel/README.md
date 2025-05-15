DPS计算器使用的动画帧数提取代码

需要（很可能是）旧版（<14.16) nodejs运行

运行步骤：

1. 使用AssetStudio （不一定还能用，或用类似工具）提取游戏包 chararts和skinpack目录下，所有“.ab”文件里的".skel"文件为文本，输出到本项目的 TextAsset 文件夹下
（共有约3-4000个）

2. npm run test
结果会输出到dps_anim.json
默认扫描 TextAsset目录，修改扫描路径需要修改index.js的107行写死的路径
