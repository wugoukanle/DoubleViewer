rem ### ����spec�ļ� ###

rem # 1.�رտ���̨������debug #
rem pyi-makespec --noconsole --onedir --debug --name DCheck main.py
rem # 2.�رտ���̨���ر�debug #
rem pyi-makespec --noconsole --onedir --name DCheck main.py
rem # 3.�򿪿���̨���ر�debug #
rem pyi-makespec --onedir  --name DCheck main.py

rem # 4.������������ #
rem pyi-makespec --onedir --name DCheck main.py

rem # 5.���ͼ�꣬�޸�������� #
rem pyi-makespec --noconsole --onedir --debug  --icon  "./qss/logo-C.ico" --name DCheck main.py

rem pyi-makespec --noconsole --onefile --icon "./images/logo/logo.ico" --name DoubleViewer main.py
rem pyi-makespec --noconsole --onedir --icon "./qss/logo-C.ico" --name DCheck main.py

rem ### ʹ��spec�ļ����� ###
pyinstaller --clean --noconfirm main.spec
pyinstaller --onedir main.spec

pyinstaller --noconsole --onefile --icon "./images/logo/logo.ico" --noconfirm --uac-admin DoubleViewer.spec
pyinstaller --noconsole --onefile --icon "./images/logo/logo.ico" --noconfirm --uac-admin main.spec







