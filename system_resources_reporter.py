import math

import rumps
import psutil


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
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = (size_bytes / p).__round__()
    return s


def get_current_system_report() -> str:
    memory_percentage = convert_size(psutil.virtual_memory().available)
    cpu_percentage = psutil.cpu_percent(interval=5).__round__()
    report = f"🧮{cpu_percentage}💾{memory_percentage}"
    return convert_to_subscript(report)


class SystemResourcesReported(rumps.App):

    def __init__(self):
        super(SystemResourcesReported, self).__init__("Loading...")

    @rumps.timer(5)
    def update_title(self, _):
        self.title = get_current_system_report()


if __name__ == "__main__":
    SystemResourcesReported().run()
