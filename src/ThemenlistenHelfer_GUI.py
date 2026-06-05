"""Kompatibilitäts-Entrypoint.

Historischer Startpunkt bleibt erhalten und delegiert an `gui.main()`.
"""

from gui import main


if __name__ == "__main__":
    main()
