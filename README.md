# Cấu hình 

## Giới thiệu : 

Tool được viết với mục đích chính là check các thông số của 1 IP như port, người sở hữu, những bản ghi `A record` đang trỏ đến địa chỉ IP. 

## Mô tả: 

Tool có các chức năng khi thao tác trên telegram như : 

- [x] Truyền vào địa chỉ IP check port của địa chỉ IP đó 

    - Gửi về telegram thông tin về port, service chạy trên port đó và giao thức TCP hoặc UDP

- [x] Truyền vào địa chỉ IP kiểm tra nếu có CVE

    - Nếu có CVE sẽ gửi về telegram những CVE đó, nếu không có sẽ gửi về 1 tin nhắn báo trống

- [x] Truyền vào địa chỉ IP hiển thị những Domain đang được trỏ đến IP đó

    - Khi truyền vào địa chỉ IP trên tele, tool sẽ gửi về các bản ghi A record đang được trỏ đến địa chỉ IP đó. 

    - Mỗi ngày chỉ được truy xuất tối đa 20 lần. 

- [x] Truyền vào địa chỉ IP hoặc domain, hiển thị thông tin về IP hoặc Domain đó. 

    - Truyền vào IP sẽ hiển thị thông tin cơ bản như người sở hữu, và thông tin liên hệ của người sở hữu IP đó. 

    - Truyền vào Domain sẽ hiển thị thông tin như : Nhà đăng ký, ngày khởi tạo, ngày hết hạn, IPS. 

    - Một số Domain có thể sẽ không hiển thị đầy đủ các thông tin như trên, nhưng chắc chắn sẽ có tên đầy đủ của domain, IPS.

Một số chức năng đang được phát triển như  : 

- [ ] Truyền vào địa chỉ IP, hiển thị hệ điều hành đang chạy trên IP đó.


## Cài đặt 

Cài đặt trên hệ điều hành CentOS 7 

Thực hiện bằng user với quyền sudo hoặc người dùng root

### Bước 1: Cài đặt các gói cần thiết

Ta kiểm tra xem đã có version 3 của python được cài trong máy chưa. 

```
python3 --version
```

Thực hiện cài đặt python3 và các gói cần thiết.

```
yum groupinstall "Development Tools" -y
yum install python3-devel -y
yum install python3 -y
yum install python3-pip -y
pip3 install virtualenv
yum install -y git curl 
```

### Bước 2: Tải về source code

```
cd /opt
git clone https://github.com/hungviet99/CheckIP.git
cd CheckIP/
```

#### Chỉnh sửa file config.py

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

### Bước 3: Tạo venv 

#### Tạo môi trường ảo python 

```
cd /opt/CheckIP
virtualenv env -p python3.6
source env/bin/activate
```
#### Cài đặt requirement 

```
pip install -r requirements.txt
```

Chạy lệnh sau để nhập api hackertaget vào hệ thống. 

```
curl https://api.hackertarget.com/dnslookup/?q=hackertarget.com&apikey=plmoknijbuhvygvtrgedsfghhhhkjhkhfsk
```
Có thể sử dụng `Enter` để đẩy nhanh quá trình chạy.

### Bước 4: Tạo file service để chương trình chạy như 1 dịch vụ 

#### Tạo file service

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

#### Khởi động dich vụ checkip

```
systemctl daemon-reload
systemctl start checkip
systemctl status checkip
systemctl enable checkip
```
