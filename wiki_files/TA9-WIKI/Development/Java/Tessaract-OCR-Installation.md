[[_TOC_]]

#Installation
##Windows
Install Tessaract on the server machine (where TextAnalytics resides) (I've downloaded it from here: https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.1.0.20190314.exe)
or
\\\10.100.102.13\Share\Installs\tesseract-ocr
##Linux (Centos) 
run the following:

```
sudo yum-config-manager --add-repo https://download.opensuse.org/repositories/home:/Alexander_Pozdnyakov/CentOS_7/
sudo rpm --import https://build.opensuse.org/projects/home:Alexander_Pozdnyakov/public_key
sudo yum update
sudo yum install tesseract 
```

# Configuration
Configure the following configurations:

SELECT * FROM sqlite_metadata.system_config;

1. OCR_ENGINE - should be TESSARCT
2. TIKA_EXTRACT_OCR_FROM_PDF - Config TIKA whether to try to extract text in images contained in PDF files. Possible values: true/false
3. TESSARACT_OCR_FILES - path for tesseract language files (when OCR configured to TESSARCT). Possible value for Windows OS : D:\\Program Files\\Tesseract-OCR\\tessdata\\ or Linux: /usr/share/tesseract/4/tessdata
4. TESSARACT_OCR_EXE_FOLDER - path for tesseract installation folder (when OCR configured to TESSARCT). Possible value for Windows OS: D:\Program Files\Tesseract-OCR\ or Linux: /usr/bin/tesseract
