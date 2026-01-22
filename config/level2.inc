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
