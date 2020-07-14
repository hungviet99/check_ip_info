import shodan
import requests
import telebot
import re
import json
import config

bot = telebot.TeleBot(config.TOKEN)

api = shodan.Shodan(config.API_SHODAN) 

# Regex địa chỉ IP
regex_ip = re.compile("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")

# Hiển thị những port đang mở
def list_port(ipaddr):

    """
    Hàm trả về giá trị là thông tin của 1 Port khi truyền vào IP bằng cách sử dụng API của shodan
    để lấy dữ liệu về port, các giao thức và dịch vụ trên port đó.   

    :Param ipaddr: Là địa chỉ IP được truyền vào khi gọi hàm

    :Response: Nếu không có lỗi trả về kết quả là InfoPort, chứa các tham số như
    Port, các dịch vụ và các giao thức tương ứng. 
               Nếu có lỗi trả về kết quả là InfoPort, là 1 thông báo lỗi
    """

    ip_info = api.host(ipaddr)
    inf_data = ip_info['data']
    info_port = "**" + 'Port' + " : " + 'Service' + " : " + 'Protocol' + "**" + '\n'
    try: 
        for data in inf_data: 
            port = str(data['port'])
            service = str(data['_shodan']['module'])
            protocol = str(data['transport'])
            inf_output = "`" + port + " : " + service + " : " + protocol + "`"
            info_port = info_port + "\n" + inf_output + '\n' 
    except:
        info_port = "Lỗi Port"
    return info_port

def list_cve(ipaddr):
    """
    :Param ipaddr: Là địa chỉ IP được truyền vào khi gọi hàm

    :Response: Nếu có CVE sẽ trả về kết quả list các CVE 
               Nếu không có CVE sẽ trả về thông báo không có CVE
    """
    ip_info = api.host(ipaddr)
    list_cve=[]
    try:
        for item in ip_info['vulns']:
            CVE = item.replace('!','')
            list_cve.append(item)
    except:
        list_cve = "Không có CVE"
    return list_cve



def list_reverse_ip(ipaddr):

    """
    :Param ipaddr: Là địa chỉ IP được truyền vào khi gọi hàm
    Sử dụng API của hackertarget để lấy dữ liệu về A record đang trỏ đến địa chỉ IP đó
    """
    try : 
        check_site = requests.get("https://api.hackertarget.com/reverseiplookup/?q={}".format(ipaddr))
        site = check_site.text
    except: 
        site = "Hết lượt truy xuất !!"
    return site

# Lấy thông tin của IP
def info_ip(ipaddr):

    """
    Sử dụng API của rapidapi 
    
    :Param ipaddr: Là địa chỉ IP được truyền vào khi gọi hàm 

    :Response: Trả về kết quả là thông tin về người sở hữu địa chỉ IP đó
    """

    payload = {"format":"json","domain":"{}" .format(ipaddr)}
    response1 = requests.request("GET", config.url, params=payload, headers=config.headers)
    inf_ip = response1.json()
    try:
        contact_name = inf_ip['contacts']['admin'][0]['name']
        contact_addr = inf_ip['contacts']['admin'][0]['address']
        contact_phone = inf_ip['contacts']['admin'][0]['phone']
        INFO_IP = 'Người sở hữu: ' + contact_name + '\n\n' 
        INFO_IP = INFO_IP + 'Địa Chỉ : ' + contact_addr + '\n\n' 
        INFO_IP = INFO_IP + 'Số điện thoại: ' + contact_phone
    except:
        INFO_IP = "Không có thông tin về người sở hữu IP này"
    return INFO_IP

# Lấy thông tin về domain
def info_domain(domain):

    """
    Sử dụng API của rapidapi
    
    :Param domain: Là domain được truyền vào khi gọi hàm

    :Response: Trả về thông tin cơ bản của domain, IPS và Domain luôn có dữ liệu 
    """
    payload = {"format":"json","domain":"{}" .format(domain)}
    response2 = requests.request("GET", config.url, params=payload, headers=config.headers)
    inf_domain = response2.json()
    IPS = inf_domain['ips']
    domain = inf_domain['name']
    try: 
        DNS = inf_domain['nameserver']
        create = inf_domain['created']
        expires = inf_domain['expires']
        registrar = inf_domain['registrar']['name']
    except:
        DNS = ' '
        create = ' '
        expires = ' '
        registrar = ' '
    INFO_DOMAIN ='Domain: ' + domain + '\n\n' 
    INFO_DOMAIN = INFO_DOMAIN + 'IPS: ' + IPS + '\n\n' 
    INFO_DOMAIN = INFO_DOMAIN + 'Name Server: ' + str(DNS) + '\n\n' 
    INFO_DOMAIN = INFO_DOMAIN + 'Nhà đăng ký: ' + registrar + '\n\n' 
    INFO_DOMAIN = INFO_DOMAIN + 'Ngày tạo: ' + create + '\n\n' 
    INFO_DOMAIN = INFO_DOMAIN + 'Ngày hết hạn: ' + expires 
    return INFO_DOMAIN

# Reply hướng dẫn
@bot.message_handler(commands=["start"])
def send_welcome(message):
    """
    Hàm mô tả các hướng dẫn để thao tác với bot trên telegram
    """
    bot.reply_to(message, "Nhập vào /port <IP> để xem port. VD: /port 8.8.8.8"+ '\n\n' +
        "Nhập vào /reverseip <IP> để xem những tên miền đang trỏ đến IP. VD: /reverseip 8.8.8.8" + '\n\n' +
        "Nhập vào /info <IP> để xem thông tin người sở hữu. VD: /info 8.8.8.8" + '\n\n' +
        "Nhập vào /info <domain> để xem thông tin của domain. VD: /info hungnv99.com" + '\n\n' +
        "Nhập vào /cve <IP> để kiểm tra xem có CVE hay không. VD: /cve 8.8.8.8", parse_mode='Markdown')

if __name__ == "__main__":

    # Tạo lệnh check port 
    @bot.message_handler(commands=["port"])
    def check_port(message):

        """
        Hàm sẽ lấy ra địa chỉ IP được nhập vào, sau đó sẽ gọi lại hàm list_port 
        và truyền địa chỉ IP vào đó. Hàm trả về kết quả sẽ lấy kết quả và gửi về telegram
        """
        IP = message.text[6:]
        same_ip = regex_ip.match(IP)
        if same_ip :
            port = list_port(IP)
            string_port  = str(port)
            send_message = bot.reply_to(message, string_port, parse_mode='Markdown')
        else:
            send_message = bot.reply_to(message, "Không Phải địa chỉ IP", parse_mode='Markdown')
    
    @bot.message_handler(commands=["cve"])
    def check_port(message):
        """
        Hàm sẽ lấy ra địa chỉ IP được nhập vào, sau đó sẽ gọi lại hàm list_cve
        và truyền địa chỉ IP vào đó. Hàm trả về kết quả sẽ lấy kết quả và gửi về telegram
        """
        IP = message.text[5:]
        same_ip = regex_ip.match(IP)
        if same_ip :
            cve = list_cve(IP)
            string_cve  = str(cve)
            send_message = bot.reply_to(message, string_cve, parse_mode='Markdown')
        else:
            send_message = bot.reply_to(message, "Không Phải địa chỉ IP", parse_mode='Markdown')

    @bot.message_handler(commands=["reverseip"])
    def check_revip(message):
        """
        Hàm sẽ lấy ra địa chỉ IP được nhập vào, sau đó sẽ gọi lại hàm list_reverse
        và truyền địa chỉ IP vào đó. Hàm trả về kết quả sẽ lấy kết quả và gửi về telegram

        Nếu messae trả về có len > 4096 ký tự (độ dài message cho phép khi sử dụng bot telegram),
        message sẽ được chia ra gửi thành nhiều phần.
        """
        IP = message.text[11:]
        same_ip = regex_ip.match(IP)
        if same_ip :
            revip = list_reverse_ip(IP)
            string_revip = str(revip)
            if len(string_revip) > 4096: 
                for x in range(0, len(string_revip), 4096):
                    send_message = bot.reply_to(message, string_revip[x:x+4096], parse_mode='Markdown')
            else:
                send_message = bot.reply_to(message, string_revip, parse_mode='Markdown')
        else:
            send_message = bot.reply_to(message, "Không Phải địa chỉ IP", parse_mode='Markdown')

    @bot.message_handler(commands=["info"])
    def check_info(message):
        """
        Hàm kiểm tra xem dữ liệu nhật vào có phải IP hay không. Nếu là IP sẽ gửi thông tin về IP, 
        Nếu không phải IP sẽ gửi thông tin về Domain. 
        """
        ip_domain = message.text[6:]
        same_ip = regex_ip.match(ip_domain)
        if same_ip: 
            mess = info_ip(ip_domain)
            string_infip = str(mess)
            send_message = bot.reply_to(message, string_infip, parse_mode='Markdown')
        else: 
            mess = info_domain(ip_domain)
            string_infdomain = str(mess)
            send_message = bot.reply_to(message, string_infdomain, parse_mode='Markdown')
    bot.polling()
