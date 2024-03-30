forgeon
======

Bring Back Standalone Web Apps to Firefox (For Now!)

Firefox fans, rejoice! This Python script (tested with Firefox 96-124 and Gnome 3,4 on Wayland/X11) aims to restore the functionality of standalone web apps, a feature dearly missed by many.

Fed up with Electron apps? Us too. This lightweight script offers a streamlined alternative to bloated Electron frameworks.

Here's what you get:

Standalone web app experience: Launch your favorite web apps as independent windows, replicating the pre-deprecation behavior.
Simple setup: Easy-to-understand Python code with clear comments makes customization a breeze.
Cross-environment compatibility (work in progress): Tested successfully on both Wayland and X11 for broader usability.
Current Limitations (Let's collaborate!):

This is a work in progress. Your contributions and ideas are invaluable in making it better!
Let's revive the standalone web app experience in Firefox!

Usage
-----

Clone this repository: git clone https://github.com/Alimiyan/App-Builder.git
Navigate to the project directory: cd App-Builder
Run the script: python forgeon.py
Feel free to report issues, suggest improvements, or contribute code!

![Screenshot of Github made into a borderless WebApp](forgeon.png)

```bash
(venv) [user@linux forgeon]$ python3 forgeon.py Skype https://web.skype.com/ call-start
Success! Try searching for 'Skype'.

List of installed apps (and also the commands to de-install them):
rm -r /home/user/.local/share/webapp/WhatsApp /home/user/.local/share/applications/webapp-WhatsApp.desktop
rm -r /home/user/.local/share/webapp/Agenda /home/user/.local/share/applications/webapp-Agenda.desktop
rm -r /home/user/.local/share/webapp/Skype /home/user/.local/share/applications/webapp-Skype.desktop
(venv) [user@linux forgeon]$ rm -r /home/user/.local/share/webapp/Skype /home/user/.local/share/applications/webapp-Skype.desktop
(venv) [user@linux forgeon]$
```

Icon Options:

There are two ways to set the icon for the generated .desktop file:

Provide an Icon Name:

Pass the desired icon name as the third argument to forgeon.
This name will be used directly in the .desktop file.
Example: forgeon https://example.com "My Web App" my_app.desktop
Automatic Download (Requires favicon package):

If you don't specify an icon name, forgeon will attempt to download the largest icon offered by the web application.
To enable this feature, you need to have the favicon Python package installed (pip install favicon).
Note: This approach requires internet access and might not always work due to website restrictions.
Choosing the Right Method:

If you have a specific icon in mind, providing the name directly offers more control.
If you prefer automatic download and have favicon installed, it's a convenient option, but keep in mind its limitations.
