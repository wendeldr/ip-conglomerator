## ip-conglomerator

change db path in libserver.py to where ever you want it.

# To run server

```./server.py <ip> <port> <passphrase>```
eg
```./server.py 127.0.0.1 65432 thisismypassword```


# To run client
to add to "db"

```./client.py <ip> <port> <passphrase>```
eg
```./client.py 127.0.0.1 65432 thisismypassword```

retreive db

```./client.py <ip> <port> <passphrase> list```
eg
```./client.py 127.0.0.1 65432 thisismypassword list```
