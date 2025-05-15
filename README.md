# DPS计算器 - 数据收集脚本合集

包括：

- Kengxxiao的游戏Blackboard数据：[ArknightsGameData](https://github.com/Kengxxiao/ArknightsGameData)
- 原计算器项目的resources/customdata数据，包括选项、手写参数和帧数数据
- 帧数提取脚本（node.js）。已适配[ArkUnpacker](https://github.com/isHarryh/Ark-Unpacker)
- 数据汇总程序：把以上所有数据都收集到按干员分的json里的处理程序

## 用法

## 数据汇总程序
```
python collect.py
```

### 输出数据格式

输出数据默认在output目录，每个干员一个json文件。包括:
```
{
    "char": { 清洗的character_table数据 },
    "equip": { 
        "battle": { 清洗的battle_equip_table数据 },
        清洗的uniequip_table数据
    },
    "custom": {
        "anim": 帧数数据,
        其他计算器手写参数(如抬手帧)
    },
    "skill": { 清洗的skill_table数据 }
}
```

包括了旧版计算器计算dps所需的所有数据。不包括写死在代码里的。

### collect.py 代码内参数设置：
- GAMEDATA_DIR：ArknightsGameData 的excel目录位置（游戏内的各种table.json），  
默认为 ./ArknightsGameData/zh_CN/gamedata/excel

- AKDATA_DIR：原计算器项目的resources/customdata位置（计算器的额外数据目录，需要用到dps_*.json)，包括2023年和以前的干员额外数据。  
默认为 ./customdata

- transform.json：设置了数据怎样变换。除此之外，还有一部分不需要的字段是在collect.py里直接去掉的，(参考代码）
- output：转换好的数据存放在这里

## 帧数提取程序 ak_skel

使用老版本node.js开发。使用步骤：

- 使用ArkUnpacker解包chararts和skinpack目录下的spine数据到`spine`目录下
```
.\ArkUnpacker-v4.0.2.exe -m ab --spine -i {游戏包路径}/skinpack -o spine
.\ArkUnpacker-v4.0.2.exe -m ab --spine -i {游戏包路径}/chararts -o spine
```
- 进入ak_skel目录
```
npm run test
```
- 会在当前目录下生成`dps_anim.json`，需要手动复制到customdata目录下。之后再改进自动化程度

- 如需修改js脚本，需要修改src目录的源码，然后使用babel处理一下
```
npm run prepublish
``` 
