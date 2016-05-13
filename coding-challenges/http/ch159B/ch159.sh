# install LAMP
# sudo apt-get install mysql-server
# sudo apt-get install apache2
# sudo apt-get install php5 php5-mysql
# sudo /etc/init.d/apache2 -k restart
# sudo chmod 777 /var/www/html

echo get crackstation-hashdb from <https://github.com/defuse/crackstation-hashdb>
echo please read its document first.
curwd=$(pwd)
cd ~
git clone https://github.com/defuse/crackstation-hashdb.git
cd crackstation-hashdb
make
mkdir data

echo generate the crack dict
python ${curwd}/ch159-gen-dict.py > data/ch159-dict.txt

echo create sha1 index
php createidx.php sha1 data/ch159-dict.txt data/ch159-dict-sha1.idx

echo sort the index
$./sortidx -r 1024 data/ch159-dict-sha1.idx

echo copy 'ch159-crack.php' to apache server directory
cp ${curwd}/ch159-crack.php /var/www/html/

echo start challenging
python ch159.py
