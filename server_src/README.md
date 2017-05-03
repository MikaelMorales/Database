# Source code for the server

This is the source code for the server. <br/>
We are using php. <br/>
By simplicity, we use MAMP as local server. <br/>
You just have to copy paste the server source files to the root folder of your local server MAMP.

To allow CORS in your MAMP sever, you have to add the following lines at the end of the file **httpd.conf**, which is in **/Applications/MAMP/conf/apache/httpd.conf** :

```
<IfModule mod_headers.c>
    # Accept cross-domain requests
    Header always set Access-Control-Allow-Origin "*"
    Header always set Access-Control-Allow-Headers "Content-Type"
</IfModule>
```
