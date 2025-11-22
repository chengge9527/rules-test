import docker

client = docker.from_env()

image_name = "ghostchu/peerbanhelper:latest"  # 替换为你需要的镜像名
output_file = "peerbanhelper.tar"

print(f"Pulling image: {image_name}")
image = client.images.pull(image_name)

print(f"Saving image to {output_file}")
with open(output_file, "wb") as f:
    for chunk in image.save(named=True):
        f.write(chunk)

print("Done.")
