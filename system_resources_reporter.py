import math
import threading

import rumps
import psutil

UI_MODE = ["Emojis", "Text"]


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
        self.ui_mode = UI_MODE[self.get_last_saved_mode()]
        self.set_menu(self.get_last_saved_mode())

    @rumps.clicked(UI_MODE[0])
    def ui_mode_0(self, _):
        self.ui_mode = UI_MODE[0]
        self.set_menu(0)

    @rumps.clicked(UI_MODE[1])
    def ui_mode_1(self, _):
        self.ui_mode = UI_MODE[1]
        self.set_menu(1)

    def set_menu(self, index):
        self.set_last_saved_mode(index)
        self.menu.clear()
        icon = "tick.png"
        self.update_current_system_report(interval=0.1)

        item = rumps.MenuItem(UI_MODE[0], callback=self.ui_mode_0)
        if index == 0:
            item.icon = icon
        self.menu.add(item)

        item = rumps.MenuItem(UI_MODE[1], callback=self.ui_mode_1)
        if index == 1:
            item.icon = icon
        self.menu.add(item)

        item = rumps.MenuItem("Quit", callback=rumps.quit_application)
        self.menu.add(item)

    @rumps.timer(5)
    def update_title(self, _):
        t = threading.Thread(target=self.update_current_system_report, args=[4, ], daemon=True)
        t.start()

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

    @staticmethod
    def get_last_saved_mode() -> int:
        with open('db.txt', 'r') as file:
            try:
                return int(file.read())
            except ValueError:
                return 0

    @staticmethod
    def set_last_saved_mode(index: int) -> None:
        with open('db.txt', 'w') as file:
            file.write(str(index))


if __name__ == "__main__":
    SystemResourcesReported().run()
