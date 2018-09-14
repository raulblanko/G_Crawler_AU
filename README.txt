1. How to make query:
-----------------------
There are internal google search symbols:

Space and + means 'AND' operator
| means 'OR' operator
- means 'NOT' operator
"" means exact phrase
site:yourpreferedsite.com means results only from this site


Example:""mad dog mattis" | "john bolton"" -donald -trump
will find all links where exactly mad dog mattis or john bolton are present but without any donald and any trump.
Notice that the phrase "mad dog mattis" | "john bolton" is covered by " too because it is single logical statement like -donald and -trump.

So if we try to translate it to any program language - it will be:
((mad AND dog AND mattis) OR (john AND bolton)) AND (NOT donald) AND (NOT trump)

------------------------
Also you can sort search resuts by date (avaliable in google search only with date ranges)
(It is not google syntaxis, so you could use it in this program but not in usual browser)
You should place SORT:D after your query (by relevance is default option, no need to add anything to keep it)

Example:
something to find SORT:D

------------------------
Also you can tell Google not to guess alternative spellings or similar words
(It is not google syntaxis, so you could use it in this program but not in usual browser)
You should place VERBATIM:1 after your query

Example:
track VERBATIM:1
will find links with "track", not tracks, not tracking, e.t.c

------------------------
Also you can set date or time range for every query
(It is not google syntaxis, so you could use it in this program but not in usual browser)
You should place DTRANGE: after your query with such parameters

Examples:
your keywords and "phrases" DTRANGE:01.08.2018-10.09.2018
your keywords and "phrases" DTRANGE:last 30 sec
your keywords and "phrases" DTRANGE:last 10 min
your keywords and "phrases" DTRANGE:last 2 hour
your keywords and "phrases" DTRANGE:last 1 day
your keywords and "phrases" DTRANGE:last 4 week
your keywords and "phrases" DTRANGE:last 3 month
your keywords and "phrases" DTRANGE:last 7 year

It allows to type sec or seconds, min or mins or minutes, month or months or even monthes).
It doesn't matter because only two first letters are important.

-----------------------
If you want to use all abilities, place SORT:D first, VERBATIM:1 second, DTRANGE: third

Examples:
site:blabla.com "my query phrase" -trash SORT:D VERBATIM:1 DTRANGE:last 2 hour
"another query" -wrong SORT:D DTRANGE:01.02.2010-05.06.2012
and another | one -wrong DTRANGE:11.02.2010-05.09.2012

Notice that dates should be in dd.mm.yyyy format

Unfortunately it seams that there is no effect in sorting by dates without any date/time ranges
And even with them Google often gives very strange results (or no results)
It's sad, but it's their search engine behavior and i can not do anything with it(


2. You can run the program in silent mode without chromedrive browser popup.
Just change settings field "headless" to true

Should be:
  "headless": true,


3. You still can change country and language settings if need.
To do so - change "local" field to false (by default it's true, so only your local settings works)

You can find two-letter codes here:
https://developers.google.com/custom-search/docs/xml_results_appendices#interfaceLanguages


4. Also you should create new Gmail mailbox only for that program.
It will send letters from there to your normal mailbox.
Then you must allow less secure apps access to SMPT server.
It switches here:
https://myaccount.google.com/lesssecureapps
or here:
https://myaccount.google.com/u/2/lesssecureapps

Be careful and do this ONLY for new created Google user and his mail.

Then make changes in settings.txt to you new mailbox, login and password:
fields "from", "login" and "password"


Notice, that beliaev.pavlo is temporary box i created yesterday just for this program, but a.agency(the_dog)ukr.net is my regular address. You can write me any request or remark. I always work through Freelancer but i support all my programs if need even after the end of project.

Best regards,
Pavlo
