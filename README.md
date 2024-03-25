# Py-Anti-Extractor
![BwE](https://i.imgur.com/Xuams7P.png)

Made for a CTF that I designed and distributed. Solved by Lindsay :)

Reads Python applications compiled with Pyinstaller and edits them in a manner that corrupts them enough to be unextractable by Pyinstxtractor and other Python decompilers.

The extraction is stopped by corrupting the table of contents, thus when using a decompiler like Pyinstxtractor for example it will throw a 'ValueError: embedded null character' error.

This is not a fool proof method in any way shape or form, but it is an interesting concept to annoy Pyinstaller users/abusers.

