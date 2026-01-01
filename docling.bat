@echo off
TITLE Docling Server

:: --- Configuration ---
echo Setting Environment Variables...

:: Enable Code Enrichment
set DOCLING_ENABLE_CODE_ENRICHMENT=true

:: Enable Formula Enrichment
set DOCLING_ENABLE_FORMULA_ENRICHMENT=true

:: Force RapidOCR
set DOCLING_OCR_ENGINE=rapidocr

:: --- Run Server ---
echo Starting Docling Serve with UI enabled...
echo.

:: Run the command (I added --enable-ui since you wanted the interface)
docling-serve run --enable-ui

:: Keep window open if it crashes
pause