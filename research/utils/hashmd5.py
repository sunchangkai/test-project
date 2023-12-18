import hashlib

def calculate_md5(file_path, salt):
    try:
        # 以二进制方式打开文件并读取内容
        with open(file_path, 'rb') as file:
            file_content = file.read()

        # 拼接Salt值
        data_to_hash = file_content + salt.encode('utf-8')

        # 计算MD5哈希值
        md5_hash = hashlib.md5(data_to_hash).hexdigest()

        return md5_hash

    except FileNotFoundError:
        return "文件未找到"
    except Exception as e:
        return f"发生错误：{e}"

# 指定文件路径和Salt值
file_path = '/Users/yuhanzhang/Desktop/ISO21434 Audit Evidence Summary_20231115.zip'
salt_value = 'ISO21434audit'

# 调用函数计算MD5哈希值
result = calculate_md5(file_path, salt_value)

# 输出结果
print("MD5哈希值:", result)




