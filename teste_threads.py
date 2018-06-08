import threading

response = None
def user_input():
    global response
    response = raw_input("Do you wish to reconnect? ")

user = threading.Thread(target=user_input)
user.daemon = True
user.start()
user.join(2)
if response is None:
    print
    response = raw_input("another thing ")
else:
    print 'As you wish'
