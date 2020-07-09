# CheckIP

## 1. Giới thiệu : 

Để thuận tiện cho việc kiểm tra Port từ 1 địa chỉ IP hoặc tra cứu thông tin của IP, domain. Mình đã phát triển 1 tool để thực hiện các thao tác tra cứu trực tiếp với bot trên telegram. 

Rất dễ dàng để có thể sử dụng, chỉ cần có 1 bot telegram và 1 server chạy CentOS 7, bạn có thể dựng cho mình 1 con bot để check info và sử dụng nó. 

## 2. Các tính năng

Tool có các chức năng khi thao tác trên telegram như : 

- [x] Chek port

- [x] Check CVE

- [x] Check Reverse IP 

- [x] Check Info IP & Domain

Một số chức năng đang được phát triển như  : 

- [ ] Ckeck hệ điều hành khi truyền vào địa chỉ IP 

## 3. Cài đặt 

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

## 4. Demo 

Để xem hướng dẫn sử dụng trước khi bắt đầu thao tác với bot, hãy nhập `/start`

![Imgur](https://i.imgur.com/P5fkAbM.png)

### Check Port
Khi truyền vào địa chỉ IP, lấy các port đang sử dụng của địa chỉ IP đó cùng với các service và các giao thức TCP hoặc UDP 

Ví dụ: Mình sẽ sử dụng lệnh sau để kiểm tra các port đang sử dụng trên IP `216.58.200.78`:

```
/port 216.58.200.78
```

![Imgur](https://i.imgur.com/pHb7J8M.png)

### Check CVE

Khi truyền vào địa chỉ IP, tool sẽ kiểm tra xem có CVE hay không.

Khi mình sử dụng lệnh `/cve 216.58.200.78`, nếu không tra ra CVE nào sẽ hiển thị 1 thông báo như sau: 

![Imgur](https://i.imgur.com/0vdKKH3.png)

Khi có CVE thì các CVE đó sẽ được gửi về telegram như sau :

![Imgur](https://i.imgur.com/ORfQP7F.png)

### Check Reverseip 

Khi truyền vào địa chỉ IP hiển thị những bản ghi `A record` đang trỏ đến địa chỉ IP đó. 

Mỗi ngày chỉ được truy xuất tối đa 20 lần

Ví dụ: Mình muốn hiển thị reverseip của địa chỉ `103.101.161.33`

```
/reverseip 103.101.161.33
```

![Imgur](https://i.imgur.com/13CcJAY.png)

### Check info

#### Info Domain

Truyền vào Domain sẽ hiển thị các thông tin của domain như : Nhà đăng ký, ngày khởi tạo, ngày hết hạn, name server, IPS. 

Ví dụ : 

```
/info hungnv99.com
```

![Imgur](https://i.imgur.com/XJVUtG2.png)

#### Info IP 

Truyền vào địa chỉ IP sẽ hiển thị được thông tin về người sở hữu và thông tin liên hệ của người sở hữu đó.

Ví dụ : 

```
/info 103.104.105.106
```

![Imgur](https://i.imgur.com/dM4KQjV.png)