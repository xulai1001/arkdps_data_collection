# DPS������ - �����ռ��ű��ϼ�

������

- Kengxxiao����ϷBlackboard���ݣ�[ArknightsGameData](https://github.com/Kengxxiao/ArknightsGameData)
- ԭ��������Ŀ��resources/customdata���ݣ�����ѡ���д������֡������
- ֡����ȡ�ű���node.js����������[ArkUnpacker](https://github.com/isHarryh/Ark-Unpacker)
- ���ݻ��ܳ��򣺰������������ݶ��ռ�������Ա�ֵ�json��Ĵ������

## �÷�

## ���ݻ��ܳ���
```
python collect.py
```

### ������ݸ�ʽ

�������Ĭ����outputĿ¼��ÿ����Աһ��json�ļ�������:
```
{
    "char": { ��ϴ��character_table���� },
    "equip": { 
        "battle": { ��ϴ��battle_equip_table���� },
        ��ϴ��uniequip_table����
    },
    "custom": {
        "anim": ֡������,
        ������������д����(��̧��֡)
    },
    "skill": { ��ϴ��skill_table���� }
}
```

�����˾ɰ����������dps������������ݡ�������д���ڴ�����ġ�

### collect.py �����ڲ������ã�
- GAMEDATA_DIR��ArknightsGameData ��excelĿ¼λ�ã���Ϸ�ڵĸ���table.json����  
Ĭ��Ϊ ./ArknightsGameData/zh_CN/gamedata/excel

- AKDATA_DIR��ԭ��������Ŀ��resources/customdataλ�ã��������Ķ�������Ŀ¼����Ҫ�õ�dps_*.json)������2023�����ǰ�ĸ�Ա�������ݡ�  
Ĭ��Ϊ ./customdata

- transform.json�����������������任������֮�⣬����һ���ֲ���Ҫ���ֶ�����collect.py��ֱ��ȥ���ģ�(�ο����룩
- output��ת���õ����ݴ��������

## ֡����ȡ���� ak_skel

ʹ���ϰ汾node.js������ʹ�ò��裺

- ʹ��ArkUnpacker���chararts��skinpackĿ¼�µ�spine���ݵ�`spine`Ŀ¼��
```
.\ArkUnpacker-v4.0.2.exe -m ab --spine -i {��Ϸ��·��}/skinpack -o spine
.\ArkUnpacker-v4.0.2.exe -m ab --spine -i {��Ϸ��·��}/chararts -o spine
```
- ����ak_skelĿ¼
```
npm run test
```
- ���ڵ�ǰĿ¼������`dps_anim.json`����Ҫ�ֶ����Ƶ�customdataĿ¼�¡�֮���ٸĽ��Զ����̶�

- �����޸�js�ű�����Ҫ�޸�srcĿ¼��Դ�룬Ȼ��ʹ��babel����һ��
```
npm run prepublish
``` 
