import math
import os
import sys
import threading
import rumps
import psutil

UI_MODE = ["Emojis", "Text"]
INTERVAL = 5


def get_last_saved_mode() -> int:
    try:
        with open(resource_path('db.txt'), 'r') as file:
            try:
                return int(file.read())
            except ValueError:
                return 0
    except FileNotFoundError:
        open(resource_path("db.txt"), "x")
        return 0


def set_last_saved_mode(index: int) -> None:
    with open(resource_path('db.txt'), 'w') as file:
        file.write(str(index))


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def convert_to_subscript(text):
    """Converts a string containing numbers into subscript characters. """
    subscript_map = {
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅',
        '6': '₆', '7': '₇', '8': '₈', '9': '₉'
    }
    return ''.join(subscript_map.get(char, char) for char in text)


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 1)
    return "%s %s" % (s, size_name[i])


def convert_size_light(size_bytes):
    if size_bytes == 0:
        return "0B"
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = (size_bytes / p).__round__()
    return s


class SystemResourcesReported(rumps.App):
    def __init__(self):
        super(SystemResourcesReported, self).__init__("Loading...", quit_button=None)
        last_saved_mode = get_last_saved_mode()
        self.ui_mode = UI_MODE[last_saved_mode]
        self.t = None
        self.is_active = True
        self.set_menu(last_saved_mode)
        threading.Thread(target=self.update_title_loop, args=[INTERVAL, ], daemon=True).start()

    @rumps.clicked(UI_MODE[0])
    def ui_mode_0(self, _):
        self.ui_mode = UI_MODE[0]
        self.set_menu(0)

    @rumps.clicked(UI_MODE[1])
    def ui_mode_1(self, _):
        self.ui_mode = UI_MODE[1]
        self.set_menu(1)

    def set_menu(self, index):
        set_last_saved_mode(index)
        self.menu.clear()
        icon = resource_path("tick.png")
        self.update_current_system_report(interval=0.1)

        item = rumps.MenuItem(UI_MODE[0], callback=self.ui_mode_0)
        if index == 0:
            item.icon = icon
        self.menu.add(item)

        item = rumps.MenuItem(UI_MODE[1], callback=self.ui_mode_1)
        if index == 1:
            item.icon = icon
        self.menu.add(item)

        item = rumps.MenuItem("Quit", callback=self.close)
        self.menu.add(item)

    def close(self, _):
        self.is_active = False
        rumps.quit_application()

    def update_title_loop(self, _):
        while self.is_active:
            self.update_current_system_report(INTERVAL)

    def update_current_system_report(self, interval) -> None:
        report = ""
        cpu_percentage = psutil.cpu_percent(interval=interval)

        if self.ui_mode == UI_MODE[0]:
            memory_percentage = convert_size_light(psutil.virtual_memory().available)
            cpu_percentage = cpu_percentage.__round__()
            report = f"🧮{cpu_percentage}💾{memory_percentage}"
            report = convert_to_subscript(report)
        elif self.ui_mode == UI_MODE[1]:
            memory_available = convert_size(psutil.virtual_memory().available)
            report = f"CPU: {cpu_percentage}% RAM: {memory_available}"

        self.title = report


if __name__ == "__main__":
    SystemResourcesReported().run()
