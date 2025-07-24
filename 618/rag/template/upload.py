import os
import engine
import config


# 上传接口
def upload_file(tenant_id, file_path):
    print(f"type of file: {type(file_path)}, value: {file_path}")
    filename = os.path.basename(file_path)
    print("上传文件：" + filename)
    file_write_dir = os.path.join(config.UPLOAD_DIR, tenant_id)
    os.makedirs(file_write_dir, exist_ok=True)
    file_write_path = os.path.join(file_write_dir, filename)
    if os.path.exists(file_write_path):
        print("文件已存在"+file_write_path)
        return

    print("文件写入路径：" + file_write_path)
    # 以二进制只读模式打开上传文件（路径由 gr.File(..., type="filepath") 返回
    with open(file_path, "rb") as src, open(file_write_path, "wb") as dst:
        dst.write(src.read())
    engine.build_index(tenant_id)
    print("✅ 文件上传并更新索引成功")


def get_paths(tenant_id: str):
    upload_path = os.path.join(config.UPLOAD_DIR, tenant_id)
    index_path = os.path.join(config.INDEX_DIR, tenant_id)
    os.makedirs(upload_path, exist_ok=True)
    os.makedirs(index_path, exist_ok=True)
    return upload_path, index_path

