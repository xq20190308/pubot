import yaml

with open("D:\\Documents\\qqbot\\nonebot\\littlebot\\littlebot\\plugins\\pu\\config.yaml", "r") as f:
    data = yaml.load(f, yaml.FullLoader)

def get_config(text):
    if "event" in text:
        return data["url"][text]
    else:
        return data[text]