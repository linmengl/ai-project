from PIL import Image
import os

def process_id_photo(input_path, output_path, target_size=(150, 200), max_size_kb=1024):
    # 打开原始图片
    img = Image.open(input_path)

    # 转换成RGB（避免PNG带透明通道问题）
    img = img.convert("RGB")

    # 裁剪成目标比例（3:4）
    target_ratio = target_size[0] / target_size[1]
    width, height = img.size
    current_ratio = width / height

    if current_ratio > target_ratio:
        # 图片过宽，按高度裁剪
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        img = img.crop((left, 0, left + new_width, height))
    else:
        # 图片过高，按宽度裁剪
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        img = img.crop((0, top, width, top + new_height))

    # 调整到目标尺寸
    img = img.resize(target_size, Image.LANCZOS)

    # 保存 JPG 并控制大小
    quality = 95
    while quality > 20:  # 降低质量直到小于1MB
        img.save(output_path, "JPEG", quality=quality)
        if os.path.getsize(output_path) <= max_size_kb * 1024:
            break
        quality -= 5

    print(f"处理完成：{output_path}, 大小 {os.path.getsize(output_path)/1024:.2f} KB")


if __name__ == "__main__":
    # 输入文件路径（替换成你的照片路径）
    process_id_photo("input.jpg", "output.jpg")