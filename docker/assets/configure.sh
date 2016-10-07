#!/bin/bash

#judgement
if [[ -a /etc/supervisor/conf.d/supervisord.conf ]]; then
  exit 0
fi

#supervisor
cat > /etc/supervisor/conf.d/supervisord.conf <<EOF
[supervisord]
nodaemon=true
[program:postfix]
command=/opt/postfix.sh
[program:courier]
command=/opt/courier.sh
[program:rsyslog]
command=/usr/sbin/rsyslogd -n -c3
EOF

############
#  postfix
############
cat >> /opt/postfix.sh <<EOF
#!/bin/bash
service postfix start
EOF
chmod +x /opt/postfix.sh
postconf -e "mydestination=localhost.localdomain, localhost"
postconf -e "home_mailbox = Maildir/"
postconf -e "mailbox_command = "

############
#  courier
############
cat >> /opt/courier.sh <<EOF
#!/bin/bash
service courier-imap start
service courier-authdaemon start
EOF
chmod +x /opt/courier.sh