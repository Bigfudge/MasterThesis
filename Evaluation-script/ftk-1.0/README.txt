README file for the ISRI OCR Frontiers Toolkit distribution
October, 1999


Please send questions, comments and bug reports to:

 isri-ftk@isri.unlv.edu



This is the data and binary distribution for the ISRI OCR Frontiers
Toolkit.  This CD contains all ground truth data for each snippet page
from "OPTICAL CHARACTER RECOGNITION: An Illustrated Guide to the Frontier,"
published by Klewer Academic Publishers (ISBN 0-7923-8492-X).


The distribution consists of four components:

1. The OCR-Frontiers test data

Included are TIFF Group IV image files for the pages corresponding to
the snippets from the OCR-Frontiers book.  Also included are text zone
definition files, text snippet definition files, and ground truth text
files for each text zone on each page.


2. The OCR-Frontiers test tools (described in more detail below).

The CD contains distribution directories containing binary executables
for Solaris 2.6, Irix 6.3, Debian GNU/Linux 2.1, and Win32.  The tools
have been compiled under the respective OS versions, but should
function without modification on other versions (i.e. Redhat Linux,
Solaris 2.7, etc).  The are only guaranteed to run under the listed
operating systems, however.  Also included is a PDF manual, and UNIX
man pages for all of the tools.


3. Sample output from three contemporary OCR systems.

All of the included test data has been run through three modern OCR
devices.  The text output from each device has been included on the CD
for example purposes.  The devices have been labeled "ocr1", "ocr2",
and "ocr3" to maintain anonymity.


4. Sample character and word accuracy reports for each OCR system.

For illustration and verification purposes, we have also included
sample accuracy reports for each page and each OCR device.  This
allows a researcher to view the sample reports, and verify that the
tools are working properly.



Directories:
------------

/bin	 This directory contains the binary distribution directories
	 for all supported platforms.

/data	 Contains directories corresponding to each section of the
	 book.  Each section directory contains TIFF, zone definition,
	 and ground truth text files for each snippet page from the
	 section.

/doc	 Contains the PDF manual for the toolkit.

/man	 Has UNIX man pages for all of the tools included on the CD.

/samples This dirctory contains subdirectories corresponding to three
	 contemporary commercial OCR packages.  The OCR devices are
	 intentionally anonymous.  Each of these OCR directories
	 contains summary word and character accuracy reports, and
	 section subdirectories which, in turn, contain sample OCR
	 output as well as character and word accuracy reports for
	 each snippet page.


Executables are included for the following tools:

Executable	 Function
----------	 --------
accci		 Compute 95% confidence interval for character accuracy.
accdist		 Generate distribution of character accuracies.
accsum		 Sum multiple character accuracy reports.
accuracy	 Compute character accuracy from GT and OCR text.
groupacc	 Compute accuracy by character class.
ngram		 Compute n-gram statistics for one or more text files.
nonstopacc	 Generate accuracy report for non-stopwords.
synctext	 Synchronize two or more strings of text.
wordacc		 Generate word accuracy report.
wordaccci	 Compute 95% confidence interval for word accuracy.
wordaccdist	 Generate distribution of word accuracies.
wordaccsum	 Sum multiple word accuracy reports.
wordfreq	 Compute frequecies of word occurance in text files.


File Naming Conventions:
------------------------

In the following descriptions, the "?" characters refer to any numeric
character.  So, for example, "??_3.tif" would match "01_3.tif", but not
"AB_3.tif".

??_3.tif    a 300dpi TIFF Group 4 image.
??_3.zon    a zone definition file.
??_3.sdf    a snippet definition file.
??.z??	    the ground truth text file for a specific text zone.
??.txt	    the ground truth text file for the entire page.
??.acc	    a character accuracy report.
??.wac	    a word accuracy report.
??.ocr	    OCR generated text for a page image.


For example, all of the data files corresponding to snippet 01 in
section 3.1, page 62 of the book would be:

Path		     Description
----		     -----------
/data/3.1/01.txt     Correct text for entire page.
/data/3.1/01.z01     Correct text for zone 1.
/data/3.1/01.z02     Correct text for zone 2.
/data/3.1/01.z03     Correct text for zone 3.
/data/3.1/01_3.tif   300dpi TIFF file for page.
/data/3.1/01_3.zon   Zone definitions file.
/data/3.1/01_3.sdf   Coordinates file for snippet on page.

and

Path			    Description
----			    -----------
/samples/ocr1/3.1/01_3.acc  Character accuracy report for ocr device 1.
/samples/ocr1/3.1/01_3.ocr  Text recognised by OCR device 1.
/samples/ocr1/3.1/01_3.wac  Word accuracy report for ocr device 1.
/samples/ocr2/3.1/01_3.acc  Character accuracy report for ocr device 2.
/samples/ocr2/3.1/01_3.ocr  Text recognised by OCR device 2.
/samples/ocr2/3.1/01_3.wac  Word accuracy report for ocr device 2.
/samples/ocr3/3.1/01_3.acc  Character accuracy report for ocr device 3.
/samples/ocr3/3.1/01_3.ocr  Text recognised by OCR device 3.
/samples/ocr3/3.1/01_3.wac  Word accuracy report for ocr device 3.








