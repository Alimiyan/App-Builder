import sys
import pathlib
import urllib.request
import os
import shutil


# used to disable distracting stuff & make editing the UI possible
PREFS = """
user_pref("browser.startup.homepage", "{url}");
user_pref("browser.startup.firstrunSkipsHomepage", false);
user_pref("browser.startup.homepage_override.mstone", "ignore");
user_pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.addons", false);
user_pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.features", false);
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);
"""

# used to remove the UI (inspired by: https://superuser.com/a/1269912 )
USER_CHROME = """
@namespace url("http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul");

/* Hide the tab strip but keep the window controls */
#TabsToolbar .tabbrowser-tabs {visibility: collapse;}
#TabsToolbar-customization-target { visibility: collapse !important; } 

/* Hide the navigation bar and bookmarks bar */
#nav-bar {visibility: collapse;}
#PersonalToolbar {visibility: collapse;}
"""


# used to create a desktop menu item
DESKTOP = """[Desktop Entry]
Version=1.0
Name={name}
Exec=firefox --profile {profile} --no-remote --name={name} --class={name}
Icon={icon_name}
Terminal=false
Type=Application
StartupWMClass={name}
"""

LOCAL_SHARE = pathlib.Path.home() / ".local/share"

WEBAPP = LOCAL_SHARE / "webapp"
WEBAPP.mkdir(exist_ok=True)


def custom_copytree(src, dst, symlinks=False, ignore=None):
    """Custom copy function that excludes certain files like 'lock'."""
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            # Exclude 'lock' file and other non-essential files as needed
            if item not in ["lock", "parent.lock", ".parentlock"]:
                shutil.copy2(s, d)


def create_profile(profile, url):
    """Create a new Firefox profile by copying a template profile."""
    if not os.path.exists(profile):
        os.makedirs(profile)
    template_profile_path = "/home/ali/.mozilla/firefox/rsz4ggkk.default-release"
    # Use the custom copy function
    custom_copytree(template_profile_path, profile)

    # Add DRM enabling preference and title bar preference
    drm_prefs = 'user_pref("media.eme.enabled", true);\n'
    title_bar_prefs = 'user_pref("browser.tabs.drawInTitlebar", true);\n'

    # Write preferences
    with open(profile / "user.js", "w") as file:
        file.write(PREFS.format(url=url) + drm_prefs + title_bar_prefs)

    # Set up the userChrome.css
    chrome = profile / "chrome"
    chrome.mkdir(exist_ok=True)
    (chrome / "userChrome.css").write_text(USER_CHROME)


def create_desktop_file(name, profile, icon_name):
    """Create a menu shortcut for our new app"""

    contents = DESKTOP.format(name=name, profile=profile, icon_name=icon_name)
    desktop_file_path(name).write_text(contents)


def desktop_file_path(name):
    return LOCAL_SHARE / "applications" / f"webapp-{name}.desktop"


def create_app(name, url, icon_name):
    # create a minimal Firefox profile
    profile = WEBAPP / name
    create_profile(profile, url)

    # download icon - if necessary
    if not icon_name:
        # png icon from this directory
        icon_name = "spotify.png"

    # create .desktop launcher file
    create_desktop_file(name, profile, icon_name)
    # ... and make sure it's detected by the system
    os.system(f"update-desktop-database {LOCAL_SHARE}/applications/")


def main():
    try:
        # default icon_name to None
        name, url, icon_name, *_ = sys.argv[1:] + [None]
    except ValueError:
        print("Usage: python3 mozapp.py Example https://example.com optional-icon-name")
    else:
        # create a webapp
        create_app(name, url, icon_name)
        print(f"Success! Try searching for '{name}'.")
    print()
    print("List of installed apps (and also the commands to de-install them):")
    for app in WEBAPP.iterdir():
        print("rm -r", app, desktop_file_path(app.name))


if __name__ == "__main__":
    main()
