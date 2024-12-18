class Notifier:
    def notify(self, count):
        pass

class ConsoleNotifier(Notifier):
    def notify(self, count):
        print(f"Scraping completed. {count} products updated in the database.")
