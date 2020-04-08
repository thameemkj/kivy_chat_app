import socket
import threading


msg_queue=()

def client_reciever(client_fd,client_id,lock):
    global msg_queue
    while(True):
        try:
            #lock.acquire(blocking=False)
            msg=client_fd.recv(2**10).decode()
            if(len(msg)>0):
                msg_queue+=(msg,)
            #lock.release()
        except:
            #client_fd.close()
            break

def client_senter(client_fd,client_id,lock):
    global msg_queue
    send_msgs=0
    while(True):
        if(send_msgs==len(msg_queue)):
            continue
        try:
            #lock.acquire(blocking=False)
            client_fd.send(msg_queue[send_msgs].encode("ascii"))
            send_msgs+=1
            #lock.release()
        except:
            #client_fd.close()
            break

def display_msgqueue():
    global msg_queue
    l=0
    while(True):
        if(l==len(msg_queue)):
            continue
        print(msg_queue)
        l=len(msg_queue)

server=socket.socket()
ip_addr="127.0.0.1"
port=2022
server.bind(("0.0.0.0",port))
print("\n\n______SERVER______\n")
print("IP Address: ",ip_addr)
print("Port Num: ",port)
server.listen(3)
print("Waiting for client.\n")
clients_count=0
lock=threading.Lock()
threading.Thread(target=display_msgqueue,daemon=True).start()
while(True):
        client_fd,client_addr=server.accept()
        clients_count+=1
        print(clients_count," clients connected")
        threading.Thread(target=client_reciever,args=(client_fd,clients_count,lock,),daemon=True).start()
        threading.Thread(target=client_senter,args=(client_fd,clients_count,lock,),daemon=True).start()
        #threading.Thread(target=display_msgqueue).start()
        print("Client obj passed to thread function successfully")
