
htpasswd 用法

htpasswd [-cmdpsD] passwordfile username
htpasswd -b[cmdpsD] passwordfile username password
htpasswd -n[mdps] username
htpasswd -nb[mdps] username password

-c  创建一个加密文件
-n  不更新加密文件，只将apache htpasswd命令加密后的用户名密码显示在屏幕上
-m  默认apache htpassswd命令采用MD5算法对密码进行加密
-d  apache htpassswd命令采用CRYPT算法对密码进行加密
-p  apache htpassswd命令不对密码进行进行加密，即明文密码
-s  apache htpassswd命令采用SHA算法对密码进行加密
-b  在apache htpassswd命令行中一并输入用户名和密码而不是根据提示输入密码
-D  删除指定的用户