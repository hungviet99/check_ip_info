FROM centos:7

LABEL maintainer="hungvietnguyen6241@gmail.com"
RUN yum groupinstall "Development Tools" -y
RUN yum install python3-devel python3 python3-pip -y
RUN pip3 install virtualenv
RUN yum install -y git curl
RUN python3 -m pip install --upgrade pip setuptools wheel

COPY ./src /opt/check_ip_info
WORKDIR /opt/check_ip_info/

RUN pip3 install -r requirements.txt
RUN sed -i 's/TOKEN =/TOKEN = "1126478322:AAFsn68ebrizoL50DKYtFQIlvUel6DpTmTc"/' /opt/check_ip_info/config.py
RUN sed -i 's/API_SHODAN =/API_SHODAN = "uwy2MOj0yGpigf30zAcEABtl4SFcSe7M"/' /opt/check_ip_info/config.py
RUN curl https://api.hackertarget.com/dnslookup/?q=hackertarget.com&apikey=plmoknijbuhvygvtrgedsfghhhhkjhkhfsk 

RUN mv /opt/check_ip_info/ipinfo.service /etc/systemd/system/ipinfo.service
RUN systemctl daemon-reload && systemctl enable ipinfo --now