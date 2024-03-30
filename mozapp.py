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
user_pref("browser.newtabpage.activity-stream.feeds.telemetry", false);
user_pref("browser.newtabpage.activity-stream.feeds.snippets", false);
user_pref("browser.newtabpage.activity-stream.feeds.section.topstories", false);
user_pref("browser.newtabpage.activity-stream.feeds.topsites", false);
user_pref("browser.newtabpage.activity-stream.feeds.system.topsites", false);
user_pref("browser.newtabpage.activity-stream.feeds.recommendationprovider", false);
user_pref("browser.newtabpage.activity-stream.feeds.section.highlights", false);
user_pref("browser.newtabpage.activity-stream.feeds.discoverystreamfeed", false);
user_pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.addons", false);
user_pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.features", false);
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);
user_pref("dom.ipc.processCount", 1);  // Reduce content processes
user_pref("browser.tabs.drawInTitlebar", true);
user_pref("layers.acceleration.disabled", true);  // Disable hardware acceleration
user_pref("network.prefetch-next", false);  // Disable link prefetching
user_pref("network.dns.disablePrefetch", true);  // Disable DNS prefetching
user_pref("network.http.speculative-parallel-limit", 0);  // Disable speculative connections
user_pref("browser.cache.disk.enable", false);  // Disable disk cache
user_pref("browser.cache.memory.enable", true);  // Keep memory cache enabled
user_pref("browser.shell.checkDefaultBrowser", false);
"""

# used to remove the UI (inspired by: https://superuser.com/a/1269912 )
USER_CHROME = """
/*------------------------USAGE----------------------------
 * Remove "/*" at the begining of "@import" line to ENABLE.
 * Add "/*" at the begining of "@import" line to DISABLE.
 */

@import "WhiteSur/theme.css"; /**/

/*--------------Configure common theme features--------------*/

/* Hide Tabs */
#TabsToolbar {visibility: collapse !important;}

/* Hide the three-dot menu (more options), profile button, and extensions from the toolbar */
#PanelUI-button, #pageActionButton, #profile-button, .toolbarbutton-1 { display: none !important; }

/* Hide Bookmark Bar */
#PersonalToolbar {visibility: collapse !important;}

/* Hide Forward/Back Buttons - they are part of the nav-bar, so this might be redundant */
#back-button, #forward-button {display: none !important;}

/* Move tab close button to left. */
/*@import "WhiteSur/left-tab-close-button.css"; /**/

/* Hide the tab bar when only one tab is open (GNOMISH)
 * You should move the new tab button somewhere else for this to work, because by
 * default it is on the tab bar too. */
/*@import "WhiteSur/hide-single-tab.css"; /**/

/* Limit the URL bar's autocompletion popup's width to the URL bar's width (GNOMISH) 
 * This feature is included by default for Firefox 70+ */
/*@import "WhiteSur/matching-autocomplete-width.css"; /**/

/* Rounded window even when it gets maximized */
/*@import "WhiteSur/rounded-window-maximized.css"; /**/

/* Active tab high contrast */
/*@import "WhiteSur/active-tab-contrast.css"; /**/

/* Use system theme icons instead of Adwaita icons included by theme [BUGGED] */
/*@import "WhiteSur/system-icons.css"; /**/

/* Allow drag window from headerbar buttons (GNOMISH) [BUGGED] */
/* It can activate button action, with unpleasant behavior. */
/*@import "WhiteSur/drag-window-headerbar-buttons.css"; /**/

/* Make all tab icons look kinda like symbolic icons */
/*@import "WhiteSur/symbolic-tab-icons.css"; /**/

/* Hide window buttons (close/min/max) in maximized windows */
/*@import "WhiteSur/hide-window-buttons.css"; /**/

/* Import your custom stylesheet */
@import "customChrome.css"; /**/
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
