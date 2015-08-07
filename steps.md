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
  <li>specify twitter list</li>
  <li>define timeframe over which engagement tbd, allowing again for external input</li>
    <ul>
      <li><s>max tweets??</s></li>
        <ul>
          <li>pull/store tweets from streaming api in real time to avoid limits</li>
          <li>friday discovery: there is no (apparent) limit</li>
        </ul>
      <li>from list members, pull all tweets with time/date of today ... is that embedded in tweet?</li>
      <li>should i try first without user selection bits, perhaps using argv to determine list/timeframe in command line?</li>
    </ul>
  <li>define number of tweets to be returned (?)</li>
  <li>return tweets</li>
</ul>  