from pattern.web import URL, Twitter

#Licence from twitter
riddlerbotKey = (
    "",
    "", (
    "",
    ""))

#This function sends tweets from our twitter account: theRiddlerBot
#@param tweet: is a string with the message to be sent
#@returns: true if the message was successfully been sent
def sendTweet(tweet):
    url = URL("https://api.twitter.com/1.1/statuses/update.json", method="post", query={"status": tweet})
    twitter = Twitter(license=riddlerbotKey)
    url = twitter._authenticate(url)
    
    try:
        # Send the post request.
        url.open()
        print "Message successfully sent: " + tweet
    
    except Exception as e:
        print e
        print e.src
        print e.src.read()
        #NEW
        twitter.id=-1
        
    #NEW        
    return twitter
