Follow these steps  
In VM  
first clean up mininet to clean state  
```
    sudo mn -c
```
Execute simple script to create single switch topology with 3 hosts  
set ip for h1, h2, h3 to 10.0.0.1, 10.0.0.2, 10.0.0.3 respectively
```
    sudo python init.py
```

After this above line, it goes into mininet CLI

Open server in h1, make sure it runs in background
```
    h1 python server.py &
```
Open renderer in h3, make sure it runs in background
``` 
    h3 python renderer.py &
```
### WARNING
Order matters. Make sure server.py runs first, then renderer.py second. 

Commands you can send:  
1: request list of available files to stream   
2: play file. -f filename should be provided. Otherwise, default file is sample.txt   
3: stop streaming   
4: resume streaming   
5: start from beginning   

Format for command:
```
    h2 python controller.py -c <command> [-f filename]
```
Below are examples of commands you can send using controller


```
    h2 python controller.py -c 1
```
```
    h2 python controller.py -c 2 -f alice_in_wonderland.txt
```
