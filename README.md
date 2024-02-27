# Py-Anti-Extractor
![BwE](https://i.imgur.com/Xuams7P.png)

Reads Python applications compiled with Pyinstaller and edits them in a manner that corrupts them enough to be unextractable by Pyinstxtractor and other Python decompilers.

The extraction is stopped by corrupting the table of contents, thus when using a decompiler like Pyinstxtractor for example it will throw a 'ValueError: embedded null character' error.

This is not a fool proof method of protecting your PYC file, but will be sufficient enough to stop most novice users. 

