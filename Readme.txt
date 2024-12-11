
Passwords application Installation.

The Passwords application was downloaded from Github to C:\Workarea\Python\Passwords_2\Passwords and streamlined to elimiante test files and code not needed to create the Psswd.exe file. Another objective is to create a distribution file so the Psswd application can be installed anywhere.

Creation of the Psswd.exe file was attempted with PyInstaller. However an issue with the PyInstaller was found while executing relative paths in the code. Code to resolve this issue was added succesfully from recommendations found online.


### PyInstaller ###

With the command/app.PyInstaller create and exe file. with the following command

C:\Workarea\Python\Passwords_2\Passwords>pyinstaller --noconfirm --onedir --windowed --add-data "C:\Workarea\Python\Passwords_2\Passwords\information.json;." --add-data "C:\Workarea\Python\Passwords_2\Passwords\key.key;." --add-data "C:\Workarea\Python\Passwords_2\Passwords\passwords.enc;."  "C:\Workarea\Python\Passwords_2\Passwords\Psswd.py"

The build and dist folders were created with the dist folder containing the Psswd folder which in turn contains the _internal folder and Psswd.exe file.
Running the same command with the --onefile parameter will create a simple Psswd.exe file, however while executing this exe the file save function does not work due to an issue with the relative paths handling with PyInstaller. 


### auto-py-to-exe ###

Another way of doing it is with the command/app auto-py-to-exe to create an exe file.
C:\Workarea\Python\Passwords_2\Passwords> auto-py-to-exe
This opens the hi and then enter
Sript location:C:/Workarea/Python/Passwords_2/Passwords/Psswd.py
Onefile: One Directory
Console Window:Windows based (hide the console)
Icon: N/A
Additional Files:
C:/Workarea/Python/Passwords_2/Passwords/password.enc
C:/Workarea/Python/Passwords_2/Passwords/key.key
C:/Workarea/Python/Passwords_2/Passwords/information.json
Advanced:N/A
Settings:N/A

The output folders was created with th dist folder containing the Psswd folder which in turn contains the _internal folder and Psswd.exe file.
Running the same command with the --onefile parameter will create a simple Psswd.exe file, however while executing this exe the file save function does not work due to an issue with the relative paths handling with PyInstaller. 

This is the prefered method to create the Psswd.exe. This method uses the PyInstaller but also correct many issues with the PyInstaller plus there is a human interface to ease use of the PyInstaller commands.


### Inno ###

Downloaded the Inno application to create an installation of the Psswd.exe

Create a Psswd.exe with auto-py-to-exe or PyInstaller and copied it int the \Inno folder.

Ran the Inno setup compiler with the following settings.
Welcome: Create a new script file using the Script Wizard
Sript Wizard Welcome: Next
Application Information - Name: Passwords - then Next
Application Folder - Destination: Next
Application Files -Main exe..:C:\Workarea\Python\Passwords_2\Passwords\Inno\Psswd.exe
Application Files -Other applications N/A - Next
Application File Association N/A - Next
Application Shortcuts ... N/A - Next
Application Documentation ... N/A - Next
Setup Install Mode - Non Administrative Install Mode - Next
Application Registry Keys ... N/A - Next
Setup Languages ... N/A - Next
Compiler Settings 
- Custom Compiler output folder: C:\Workarea\Python\Passwords_2\Passwords\Inno
- Compiler output base file name: Passwords_setup.exe
Next
Inno Setup Preprocessor - Next
Finish - Next

Compile the new sript - Yes
Would you like to save script before compiling - Yes
Enter: Passwords_script - Save

Now go to the \Inno folder and run Passwords_setup.exe

Select destination Location - Accept C:\Users\Arturo\AppData\Local\Programs\Passwords
Additional tasks - Create a desktop shortcut
Ready to Install - Install
Finish.

The \Inno\Passwords_setup.exe can now be used to distribute it and install the Psswd.exe with supporting files for use.