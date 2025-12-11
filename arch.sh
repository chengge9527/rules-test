#!/bin/bash
set -e

DISK=/dev/sda   # ⚠️ 请确认这是你的U盘设备号

echo ">>> 分区磁盘"
parted -s $DISK mklabel gpt
parted -s $DISK mkpart primary fat32 1MiB 1025MiB   # sda1 EFI 1G
parted -s $DISK mkpart primary ext4 1025MiB 100%    # sda2 根分区

echo ">>> 格式化分区"
mkfs.fat -F32 ${DISK}1 -n EFI
mkfs.ext4 ${DISK}2 -L ROOT

echo ">>> 挂载分区"
mount ${DISK}2 /mnt
mkdir -p /mnt/boot/efi
mount ${DISK}1 /mnt/boot/efi

echo ">>> 安装基础系统"
pacstrap /mnt base linux linux-firmware vim nano networkmanager grub efibootmgr

echo ">>> 生成 fstab"
genfstab -U /mnt >> /mnt/etc/fstab

echo ">>> 进入 chroot 环境并配置系统"
arch-chroot /mnt /bin/bash <<EOF
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
hwclock --systohc --localtime

# 设置 locale
sed -i 's/^#en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen
sed -i 's/^#zh_CN.UTF-8 UTF-8/zh_CN.UTF-8 UTF-8/' /etc/locale.gen
locale-gen

echo "LANG=en_US.UTF-8" > /etc/locale.conf

echo "arclinux" > /etc/hostname

systemctl enable NetworkManager

echo ">>> 安装 GRUB"
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=GRUB --removable
grub-mkconfig -o /boot/grub/grub.cfg

echo ">>> 新建用户 monkey"
useradd -m -G wheel -s /bin/bash monkey

EOF

echo ">>> 安装完成！请 umount 并重启"
umount -R /mnt
