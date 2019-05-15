First you have to install postfix to use the sendmail operator.
On SuSe 42.2 it is installed by default. You can use Yast if this is not the case. 





Use "sudo apt install postfix" to install it on Ubuntu.
During the installation, a prompt will appear asking for your General type of mail configuration.
Select Internet Site. Then enter the fully qualified name of your domain,



You have to make sure that the bash is your standard shell.
On Ubuntu you have to change the standard from dash to bash.

Use the command :

sudo dpkg-reconfigure dash 

and then choose the "No" Option.


Then you have to modify two files 
/etc/postfix/main.cf  and /etc/postfix/sasl_passwd.

If the latter one does not exist, you need to create it.



In the sasl_passwd you have to edit (default port 25):

[smtp.isp.example]:25  username:password


Now create the hash db file for postfix by running:

sudo postmap /etc/postfix/sasl_passwd






In the main.cf you have to adapt the entries to your purposes (smtp Server without tls).

Either you have to change existing entries or you have to create them.


#specify SMTP relay host 
relayhost = [smtp.isp.example]:25 

# enable SASL authentication 
smtp_sasl_auth_enable = yes

# disallow methods that allow anonymous authentication. 
smtp_sasl_security_options = noanonymous

# where to find sasl_passwd
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd

# Enable STARTTLS encryption 
smtp_use_tls = no



Example for a smtp server with tls:


In the sasl_passwd you have to edit:

[smtp.isp.example]:587  username:password


In the main.cf you have to edit:

# specify SMTP relay host 
relayhost = [smtp.isp.example]:587 


# enable SASL authentication 
smtp_sasl_auth_enable = yes

# disallow methods that allow anonymous authentication. 
smtp_sasl_security_options = noanonymous

# where to find sasl_passwd
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd

# Enable STARTTLS encryption 
smtp_use_tls = yes

# where to find CA certificates
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt





Make sure for the sasl_passwd.db und the sasl_passwd that only root is able to read or write 
those files.

You can do it with:

sudo chown root:root /etc/postfix/sasl_passwd /etc/postfix/sasl_passwd.db
sudo chmod 0600 /etc/postfix/sasl_passwd /etc/postfix/sasl_passwd.db




As a last step you have to restart the postfix service:

sudo service postfix restart
