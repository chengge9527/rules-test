import docker

client = docker.from_env()
image_name = "mihomo:latest"
output_path = "/tmp/mihomo_image.tar"

# 拉取镜像
print(f"Pulling image {image_name}...")
client.images.pull(image_name)

# 保存为 tar 文件
print(f"Saving image to {output_path}...")
image = client.images.get(image_name)
with open(output_path, "wb") as f:
    for chunk in image.save(named=True):
        f.write(chunk)

print("Done.")
