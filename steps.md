<h1>steps to highlight top tweets over x period of time from y list</h1>
<ul>
  <li>choose twitter library for python</li>
    <ul>
      <li>https://github.com/tweepy/tweepy</li>
      <li>https://github.com/ryanmcgrath/twython</li>
    </ul>
  <li>import library</li>
  <li>create twitter app for key/secret</li>
  <li>authorize script</li>
  <li>define/weight engagement (replies, retweets, favorites)<li>
    <ul>
      <li>likely in above order</li>
    </ul>
  <li>pull user lists</li>
    <ul>
      <li>print lists (own and subscribe)</li>
      <li>list = int(raw_input("Which list? "))</li>
    </ul>
  <li>define timeframe over which engagement tbd, allowing again for external input</li>
    <ul>
      <li><s>max tweets??</s></li>
        <ul>
          <li>pull/store tweets from streaming api in real time to avoid limits</li>
          <li>friday discovery: there is no (apparent) limit</li>
        </ul>
      <li>from list members, pull all tweets with time/date of today ... is that embedded in tweet?</li>
        <ul>
          <li>for member in list:<br>
          \tif date == today:<br>
          \t\tprint status</li>
        <ul>
    </ul>
  <li>define number of tweets to be returned (?)</li>
    <ul>
      <li>.items(xxx) in for-loop pulling tweets</li>
    </ul>
  <li>return tweets</li>
    <ul>
      <li>receiving <a href="https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning">insecure platform warning</a> when running tweepy_test.py, what do i need to know about using ssl/urllib3?</li>
      <li>and while we're on the subject, what are the common python libraries i should know about?</li>
</ul>  
