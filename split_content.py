import copy
import re
def split_content(content, max_len):
    content_list = re.split(r"([，。？！；])",content)
    content_list.append("")
    content_list = ["".join(i) for i in zip(content_list[0::2], content_list[1::2])]
    new_content_list=[]
    new_content=""
    for i in range(len(content_list)):
        old_content = new_content
        new_content = new_content + content_list[i]
        if len(new_content) > max_len:
            new_content_t = copy.deepcopy(old_content)
            new_content_list.append(new_content_t)
            new_content = content_list[i]
    if len(new_content)>0:
        new_content_list.append(new_content)
    return new_content_list

if __name__ == "__main__":
    content = "嗯，这种设计思路听起来很吸引人。那对于高端定位的产品来说，老铺黄金是如何通过定价策略来塑造品牌形象的？嗯...老铺黄金采取了高价位策略，主力产品定价在1万至5万元之间，甚至有些达到25万元以上。这种定价不仅反映了产品本身价值，更重要的是通过价格传递出品牌定位信息——即作为奢侈品存在。采用“一口价”模式，减少对原材料成本波动敏感度，强调艺术性和收藏价值，进一步巩固了高端品牌形象。"
    content_list = split_content(content,80)
    print("--------------------")
    for i in content_list:
        print(len(i))
        print(i)