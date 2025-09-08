@echo off
echo.
echo *** ULTIMATE GGUF EXTRACTOR ***
echo *** Made By @CuppaTeaCuppa ***
echo ================================
echo.
echo Choose your interface:
echo.
echo 1. GUI Version (Easiest - Recommended!)
echo 2. Command Line Interface
echo 3. View README
echo 4. Run Example Analysis
echo 5. Cleanup Virtual Mounts
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Starting GGUF Editor GUI...
    python gguf_gui.py
    goto end
)

if "%choice%"=="2" (
    echo.
    echo GGUF CLI Help:
    echo.
    python gguf_cli.py --help
    echo.
    echo Example commands:
    echo python gguf_cli.py analyze model.gguf -v
    echo python gguf_cli.py mount model.gguf /virtual/model
    echo python gguf_cli.py fix-tokenizer /virtual/model
    echo python gguf_cli.py save /virtual/model fixed_model.gguf
    goto end
)

if "%choice%"=="3" (
    echo.
    echo Opening README...
    start README.md
    goto end
)

if "%choice%"=="4" (
    echo.
    echo Running example analysis...
    echo Please place a GGUF file in this directory and modify the script
    echo.
    rem python gguf_cli.py analyze your_model.gguf -v
    echo Example: python gguf_cli.py analyze your_model.gguf -v
    goto end
)

if "%choice%"=="5" (
    echo.
    echo Cleaning up virtual mounts...
    python gguf_cli.py cleanup
    echo Cleanup complete!
    goto end
)

echo.
echo Invalid choice. Please run the script again.

:end
echo.
echo Thanks for using ULTIMATE GGUF EXTRACTOR!
echo Perfect for professional AI model enhancement!
pause
