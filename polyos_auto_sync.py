import os
import sublime
import sublime_plugin

PACKAGE_NAME = "PolyOS-Edi-for-Sublime-Text"
PROFILE_DIR = "Packages/" + PACKAGE_NAME + "/profile/"
MANIFEST_NAME = "manifest.json"
MARKER_NAME = ".polyos-sync.json"
DEFAULT_INTERVAL_SECONDS = 4 * 60 * 60  # align with Package Control's default check
STARTUP_DELAY_MS = 15000

# Keys of Package Control.sublime-settings that this plugin is allowed to
# change. Everything else (bootstrapped, in_process_packages, last_*, ...) is
# owned by Package Control and left untouched.
_AUTHORED_KEYS = ("repositories", "installed_packages")

# Syntax resource paths from older PolyOS layouts that no longer exist. Views
# restored from a stale session carry one of these and make Sublime log
# "Error loading syntax file ... Unable to stat" on every startup. The plugin
# rewrites them to the current path (see _repair_stale_syntax_references).
_CURRENT_SYNTAX = "Packages/" + PACKAGE_NAME + "/polymark.sublime-syntax"
_STALE_SYNTAX_PATHS = (
    "Packages/User/polymark.sublime-syntax",       # "first try" layout (a641bb7)
    "Packages/PolyMark/polymark.sublime-syntax",   # custom-packages layout (4c54317..v3.2.x)
)


def _user_path(name):
    return os.path.join(sublime.packages_path(), "User", name)


def _load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return sublime.decode_value(f.read())
    except (OSError, ValueError):
        return None


def _write_json(path, data):
    try:
        directory = os.path.dirname(path)
        if not os.path.isdir(directory):
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(sublime.encode_value(data, pretty=True))
    except OSError:
        return False
    return True


def _merge_package_control(profile):
    existing = _load_json(_user_path("Package Control.sublime-settings")) or {}

    merged = dict(existing)
    for key in _AUTHORED_KEYS:
        additions = profile.get(key, [])
        current = list(existing.get(key, []))
        if not current and additions:
            # Package Control clears installed_packages during its startup
            # bootstrap; restore the baseline so managed packages stay
            # installed and upgradeable.
            current = list(additions)
        else:
            for item in additions:
                if item not in current:
                    current.append(item)
        merged[key] = current
    return merged


def _ensure_package_control_baseline():
    try:
        content = sublime.load_resource(
            PROFILE_DIR + "Package Control.sublime-settings")
    except OSError:
        return
    _apply_profile_file("Package Control.sublime-settings", content)


def _merge_user_preferences(profile):
    # User/Preferences.sublime-settings wins over every package Preferences,
    # so the profile's shared keys must be layered into the existing file.
    # Unrelated user settings are preserved; profile keys win on version bump
    # so a fresh install/upgrade lands the PolyOS look on first sync.
    existing = _load_json(_user_path("Preferences.sublime-settings")) or {}
    merged = dict(existing)
    merged.update(profile)
    return merged


def _apply_profile_file(name, content):
    if name == "Package Control.sublime-settings":
        try:
            profile = sublime.decode_value(content)
        except ValueError:
            print("[PolyOS] profile: invalid Package Control.sublime-settings, skipped")
            return False
        path = _user_path(name)
        existing = _load_json(path) or {}
        merged = _merge_package_control(profile)
        if merged == existing:
            return True
        ok = _write_json(path, merged)
        if ok:
            print("[PolyOS] profile: Package Control baseline ensured")
        return ok
    elif name == "Preferences.sublime-settings":
        try:
            profile = sublime.decode_value(content)
        except ValueError:
            print("[PolyOS] profile: invalid Preferences.sublime-settings, skipped")
            return False
        merged = _merge_user_preferences(profile)
        ok = _write_json(_user_path(name), merged)
    else:
        ok = _write_json(_user_path(name), sublime.decode_value(content))
    return ok


def apply_profile(force=False):
    # Always keep the Package Control baseline in place. Package Control can
    # wipe installed_packages during its startup bootstrap, so re-assert on
    # every check (the union merge is idempotent and only writes on change).
    _ensure_package_control_baseline()

    try:
        manifest = sublime.decode_value(
            sublime.load_resource(PROFILE_DIR + MANIFEST_NAME))
    except ValueError:
        print("[PolyOS] profile: manifest missing or invalid, skipping sync")
        return

    version = str(manifest.get("version", ""))
    if not version:
        print("[PolyOS] profile: manifest has no version, skipping sync")
        return

    marker_path = _user_path(MARKER_NAME)
    if not force and _load_json(marker_path) == {"version": version}:
        return

    applied = []
    failed = []
    for name in manifest.get("files", []):
        if name == "Package Control.sublime-settings":
            continue
        try:
            content = sublime.load_resource(PROFILE_DIR + name)
        except OSError:
            failed.append(name)
            continue
        if _apply_profile_file(name, content):
            applied.append(name)
        else:
            failed.append(name)

    if failed:
        print("[PolyOS] profile: failed to apply: %s" % ", ".join(failed))
        return

    _write_json(marker_path, {"version": version})
    msg = "PolyOS profile synced to v%s" % version
    print("[PolyOS] " + msg)
    sublime.status_message(msg)


def _repair_stale_syntax_references():
    # Views restored from a pre-bundle session may still point at syntax paths
    # that no longer exist, making Sublime log "Error loading syntax file ...
    # Unable to stat" on every startup. Rewrite them to the current path; the
    # corrected setting is saved back into the session on exit.
    for window in sublime.windows():
        for view in window.views():
            syntax = view.settings().get("syntax")
            if syntax in _STALE_SYNTAX_PATHS:
                view.set_syntax_file(_CURRENT_SYNTAX)
                print("[PolyOS] repaired stale syntax: %s -> %s" % (syntax, _CURRENT_SYNTAX))


def _schedule_next_check(interval):
    sublime.set_timeout(lambda: _periodic_check(interval), interval * 1000)


def _periodic_check(interval):
    try:
        apply_profile()
        _repair_stale_syntax_references()
    finally:
        _schedule_next_check(interval)


def plugin_loaded():
    _repair_stale_syntax_references()
    sublime.set_timeout(
        lambda: _periodic_check(DEFAULT_INTERVAL_SECONDS),
        STARTUP_DELAY_MS)


class PolyosSyncProfileCommand(sublime_plugin.WindowCommand):
    """Forces the profile to re-apply even if the version is unchanged."""

    def run(self):
        apply_profile(force=True)
