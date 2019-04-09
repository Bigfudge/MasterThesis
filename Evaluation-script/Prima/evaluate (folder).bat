@echo off
setlocal ENABLEDELAYEDEXPANSION


set counter=0


::
:: Loop through all files within the specified folder
::

FOR %%c in ("input\gt\*.txt") DO (
  IF !counter! == 0 (
  java -jar PrimaText.jar -gt-text "%%c" -gt-enc UTF-8 -res-text "input\res\%%~nc.txt" -res-enc UTF-8 -method BagOfWords,CharacterAccuracy,WordAccuracy -toLower ENGLISH -csv-headers -csv-addinp>output.csv
  ) ELSE (
  java -jar PrimaText.jar -gt-text "%%c" -gt-enc UTF-8 -res-text "input\res\%%~nc.txt" -res-enc UTF-8 -method BagOfWords,CharacterAccuracy,WordAccuracy -toLower ENGLISH -csv-addinp>>output.csv
  )
  set /A counter+=1
  echo !counter!
)

endlocal