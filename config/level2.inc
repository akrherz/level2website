  ServerName mesonet-nexrad.agron.iastate.edu
  ServerAlias level2.local
  ServerAdmin akrherz@iastate.edu
  DocumentRoot "/opt/level2website/htdocs"
  <Directory "/opt/level2website/htdocs">
    Options Indexes
    AllowOverride None
    Order allow,deny
    Allow from all
  </Directory>

  #Redirect /level2/raw/KJAX https://tgftp.nws.noaa.gov/data/radar/nexrad_level2/KJAX
  RewriteEngine On
  RewriteCond %{HTTP_USER_AGENT} ^GRLevelX/2\.0$
  #RewriteRule ^/level2/raw/(.*)$ https://tgftp.nws.noaa.gov/data/radar/nexrad_level2/$1 [R=302,L]
  RewriteRule ^/level2/raw/(.*)$ https://nomads.ncep.noaa.gov/pub/data/nccf/radar/nexrad_level2/$1 [R=302,L]

  Alias "/level2" "/mnt/level2"
  <Directory "/mnt/level2">
    Options Indexes FollowSymLinks
    AllowOverride None
    Order allow,deny
    Allow from all
  </Directory>

  Alias "/archive" "/mnt/l2archive"
  <Directory "/mnt/l2archive">
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
  </Directory>
