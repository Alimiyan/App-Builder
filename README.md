mozapp
======

Do you prefer Firefox to Chrome? Me too! But ever since Firefox dropped support
for standalone web applications, I've resorted to using Chrome for those.
Better than installing a bloated Electron app, but not ideal.

This is my best attempt at fixing the situation. Tested only using Firefox 96
and Gnome 3 on both Wayland and X11. It's a 100 line commented and
straightforward Python script.

Usage
-----

```bash
(venv) [user@linux]$ python3 mozapp.py
Usage: python3 mozapp.py Example https://example.com optional-icon-name

List of installed apps (and also the commands to de-install them):
rm -r /home/user/.local/share/webapp/WhatsApp /home/user/.local/share/applications/webapp-WhatsApp.desktop
rm -r /home/user/.local/share/webapp/Agenda /home/user/.local/share/applications/webapp-Agenda.desktop
```

```bash
(venv) [user@linux]$ python3 mozapp.py Spotify https://web.Spotify.com/ call-start
Success! Try searching for 'Spotify'.

List of installed apps (and also the commands to de-install them):
rm -r /home/user/.local/share/webapp/WhatsApp /home/user/.local/share/applications/webapp-WhatsApp.desktop
rm -r /home/user/.local/share/webapp/Agenda /home/user/.local/share/applications/webapp-Agenda.desktop
rm -r /home/user/.local/share/webapp/Spotify /home/user/.local/share/applications/webapp-Spotify.desktop
(venv) [user@linux]$ rm -r /home/user/.local/share/webapp/Spotify /home/user/.local/share/applications/webapp-Spotify.desktop
(venv) [user@linux]$
```

