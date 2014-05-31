#PtServer
PTSERVER_HOME=D:\PtServer

D:\usr\bin;D:\usr\local\memcached;D:\usr\local\mongodb;D:\usr\local\mysql;D:\usr\local\nodejs;D:\usr\local\php\55;D:\usr\local\php\phing-2.6.1\bin


#phing
PHING_HOME=D:\PtServer\php\phing-2.6.1
PHP_CLASSPATH=D:\PtServer\php\phing-2.6.1\classes
PHP_COMMAND=D:\PtServer\php\55\php.exe
PATH=%PHING_HOME%\bin




http://pear.php.net/go-pear.phar

pear clear-cache
pear channel-discover pear.phpunit.de
pear install –a -f phpunit/PHPUnit

Installing PHPUnit On Windows
Posted on August 21st, 2012 by Alex Mills
I wanted to start contributing to the WordPress unit tests so I needed to install PHPUnit. Turned out it was harder than it might seem (I had a tough time getting it all working) so I thought I’d blog what finally ended up working for me to help save some people some time.

Assuming you already have PHP and MySQL installed, here’s the steps you need to take:

Install PEAR, a dependency for PHPUnit:
Visit http://pear.php.net/go-pear.phar in your browser and save the file into your PHP directory. This is the folder where you can find php.exe.
Open an administrator command prompt. On Vista or Windows 7, hit your Windows key, type “cmd”, right-click the resulting “cmd.exe” search result, and select “Run as administrator”. Navigate to the folder where you have PHP installed, the same folder where you saved the file in the previous step.
Type the following command to execute the file you just downloaded: php go-pear.phar
After a moment, you should start being prompted for some things. The installer is pretty self-explanatory and I think you want a system installation rather than a local one.
Open the folder where PHP is installed and double-click the PEAR_ENV.reg file that has been created. This allows you to run the pear command from any folder.
Verify PEAR is working by running the command pear version
Install PHPUnit:
Turn on auto_discover in PEAR by typing the following command at the command line: pear config-set auto_discover 1
Download and install PHPUnit by running the following command: pear install pear.phpunit.de/PHPUnit
In order to be able to run the phpunit command from any folder, you need to add it to your Windows Path value. Right-click My Computer → Properties → Advanced system settings → Environmental Variables → select “Path” under “System Variables” → Edit → Add a semi-colon (;) and then the full path to your PHP folder onto the end of the value, for example like this: ;D:\Webserver\php
Verify PHPUnit is working by running the command phpunit --version
Set up the WordPress unit tests by following the rest of the steps on the WordPress Core Contributor Handbook now that you have PHPUnit installed.