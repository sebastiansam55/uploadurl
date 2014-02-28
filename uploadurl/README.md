uploadurl
==

Allows users of a mediagoblin site to upload files via GET url variables (allows for cool browser extensions)

It works best in browser because it uses the browser authentication right now.

Example for http://i.imgur.com/KWl6pqT.jpg

`HOSTNAME/upload?url=http%3A%2F%2Fi.imgur.com%2FKWl6pqT.jpg&title=heavybreathingcat`

Which should return some json

`{"status":"200", "permalink":"<URLGOESHERE>"}`


License
----

GNU GPLv3