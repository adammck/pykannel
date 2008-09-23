This is a lightweight interface to [Kannel](http://kannel.org) (also available via your local apt-get repository) to make sending and receiving SMS messages in Python a little more friendly, at the cost of a little abstraction. It's very bare right now; you may consider that an invitation for pataches.


### Sending an SMS
    sender = SmsSender("kuser", "kpass")
    sender.send("1234567890", "Hello")
    sender.send("0987654321", "Goodbye")


### Receiving SMS
    class TestReceiver():
        def iGotAnSMS(self, caller, msg):
            print "SMS from %s: %s" % (caller, msg)
    
    tr = TestReceiver()
    print "Waiting for SMS..."
    SmsReceiver(tr.iGotAnSMS).run()

