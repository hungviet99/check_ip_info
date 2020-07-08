# Cấu hình 

## Mô tả : 
Tool có các chức năng như : 

- Truyền vào địa chỉ IP check port và service chạy trên port đó 

- Truyền vào địa chỉ IP kiểm tra nếu có CVE

- Truyền vào địa chỉ IP hiển thị những Domain đang được trỏ đến IP đó. ( 1 Ngày tối đa 20 lần)

- Truyền vào địa chỉ IP hoặc domain, hiển thị thông tin về IP hoặc Domain đó. 

Sử dụng trên hệ điều hành CentOS 7 

Thực hiện bằng user với quyền sudo hoặc người dùng root

## Kiểm tra version Python trên máy

Ta kiểm tra xem đã có version 3 của python được cài trong máy chưa. 
```
python3 --version
```

Nếu chưa có phiên bản python 3 trong máy, thực hiện cài đặt python3 

**Đối với CentOS:** 

Cài đặt các gói cần thiết 

```
yum groupinstall "Development Tools" -y
yum install python3-devel -y
yum install python3 -y
yum install python3-pip -y
pip3 install virtualenv
yum install -y git curl 
```

Để sử dụng được chương trình này chạy như 1 tiến trình của hệ thống, ta làm như sau : 

## Bước 1: Tải về source code

```
cd /opt
git clone https://github.com/hungviet99/CheckIP.git
cd CheckIP/
```

### Chỉnh sửa file config.py

- Thay token bot telegram

```
sed -i 's/TOKEN =/TOKEN = "918364925:AAGbl5y7463f8DFFx4RhkeB3_eRhUUNfHHw"/' /opt/CheckIP/config.py
```

Thay `918364925:AAGbl5y7463f8DFFx4RhkeB3_eRhUUNfHHw` bằng token bot của bạn 

- Lấy API của shodan  

Nếu bạn không có API của shodan, có thể đăng nhập vào shodan theo đường link sau : [Shodan login](https://account.shodan.io/login). Sau khi đăng nhập, truy cập vào [API shodan](https://account.shodan.io/) để lấy API key của shodan. 

Hoặc bạn có thể sử dụng api sau: `1iyY8S7elAIY9P4i9ISZKUOV4DSBdQpl`

- Thêm API của shodan vào file config. 

```
sed -i 's/ApiKeyShodan =/ApiKeyShodan = "1iyY8S7elAIY9P4i9ISZKUOV4DSBdQpl"/' /opt/CheckIP/config.py
```

Nếu bạn có API khác thì hãy thay `1iyY8S7elAIY9P4i9ISZKUOV4DSBdQpl` bằng API của bạn.

## Tạo venv 

### Tạo môi trường ảo python 

```
cd /opt/CheckIP
virtualenv env -p python3.6
source env/bin/activate
```
### Cài đặt requirement 

```
pip install -r requirements.txt
```

Chạy lệnh sau để nhập api hackertaget vào hệ thống. 

```
curl https://api.hackertarget.com/dnslookup/?q=hackertarget.com&apikey=plmoknijbuhvygvtrgedsfghhhhkjhkhfsk
```

### Tạo file service 

```
vi /etc/systemd/system/checkip.service
```

và ghi vào file nội dung như sau : 

```
[Unit]
Description= Check info IP or Domain
After=network.target

[Service]
PermissionsStartOnly=True
User=root
Group=root
ExecStart=/opt/CheckIP/env/bin/python3 /opt/CheckIP/messagebot.py --serve-in-foreground

[Install]
WantedBy=multi-user.target
```

### Khởi động dich vụ sshalert 

```
systemctl daemon-reload
systemctl start checkip
systemctl status checkip
systemctl enable checkip
```
