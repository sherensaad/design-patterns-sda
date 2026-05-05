"""
Software Design & Architecture - Final Project
Design Patterns Implementation in Python
Patterns: Singleton, Prototype, Factory Method
"""


class DatabaseConnection:
    """
    Singleton Pattern: Ensures only one database connection
    instance exists throughout the application lifecycle.
    """
    _instance = None

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connected = True
        self.query_log = []

    @classmethod
    def get_instance(cls, db_name: str = "AppDatabase"):
        if cls._instance is None:
            cls._instance = cls(db_name)
            print(f"[Singleton] New DB connection created: {db_name}")
        else:
            print(f"[Singleton] Reusing existing DB connection: {cls._instance.db_name}")
        return cls._instance

    def execute_query(self, query: str):
        self.query_log.append(query)
        print(f"[DB] Executing: {query}")

    def get_log(self):
        return self.query_log



import copy

class Document:
    """Base prototype class for documents."""

    def __init__(self, title: str, content: str, metadata: dict):
        self.title = title
        self.content = content
        self.metadata = metadata  

    def clone(self):
        """Deep copy to ensure full independence of the clone."""
        return copy.deepcopy(self)

    def display(self):
        print(f"[Document] Title: {self.title}")
        print(f"           Content: {self.content}")
        print(f"           Metadata: {self.metadata}")


class ReportDocument(Document):
    def __init__(self, title, content, metadata, report_type):
        super().__init__(title, content, metadata)
        self.report_type = report_type

    def clone(self):
        return copy.deepcopy(self)

    def display(self):
        super().display()
        print(f"           Report Type: {self.report_type}")


class InvoiceDocument(Document):
    def __init__(self, title, content, metadata, amount):
        super().__init__(title, content, metadata)
        self.amount = amount

    def clone(self):
        return copy.deepcopy(self)

    def display(self):
        super().display()
        print(f"           Amount: ${self.amount}")


from abc import ABC, abstractmethod

class Notification(ABC):
    """Product interface."""

    @abstractmethod
    def send(self, message: str):
        pass

    @abstractmethod
    def get_channel(self) -> str:
        pass


class EmailNotification(Notification):
    def __init__(self, recipient: str):
        self.recipient = recipient

    def send(self, message: str):
        print(f"[Email] Sending to {self.recipient}: {message}")

    def get_channel(self) -> str:
        return "Email"


class SMSNotification(Notification):
    def __init__(self, phone: str):
        self.phone = phone

    def send(self, message: str):
        print(f"[SMS] Sending to {self.phone}: {message}")

    def get_channel(self) -> str:
        return "SMS"


class PushNotification(Notification):
    def __init__(self, device_id: str):
        self.device_id = device_id

    def send(self, message: str):
        print(f"[Push] Sending to device {self.device_id}: {message}")

    def get_channel(self) -> str:
        return "Push"


class NotificationFactory(ABC):
    """Creator — declares the factory method."""

    @abstractmethod
    def create_notification(self, target: str) -> Notification:
        pass

    def notify(self, target: str, message: str):
        notif = self.create_notification(target)
        print(f"[Factory] Created {notif.get_channel()} notification")
        notif.send(message)


class EmailFactory(NotificationFactory):
    def create_notification(self, target: str) -> Notification:
        return EmailNotification(target)


class SMSFactory(NotificationFactory):
    def create_notification(self, target: str) -> Notification:
        return SMSNotification(target)


class PushFactory(NotificationFactory):
    def create_notification(self, target: str) -> Notification:
        return PushNotification(target)


def run_demo():
    print("=" * 55)
    print("       SOFTWARE DESIGN & ARCHITECTURE — DEMO")
    print("=" * 55)

    # --- Singleton ---
    print("\n--- Pattern 1: Singleton (Database Connection) ---")
    db1 = DatabaseConnection.get_instance("MainDB")
    db2 = DatabaseConnection.get_instance("OtherDB")
    db1.execute_query("SELECT * FROM users")
    db2.execute_query("INSERT INTO logs VALUES ('login')")
    print(f"Same instance? {db1 is db2}")
    print(f"Query log: {db1.get_log()}")

    # --- Prototype ---
    print("\n--- Pattern 2: Prototype (Document Cloning) ---")
    original_report = ReportDocument(
        title="Q1 Sales Report",
        content="Sales data for Q1...",
        metadata={"author": "Alice", "year": 2025},
        report_type="Financial"
    )
    cloned_report = original_report.clone()
    cloned_report.title = "Q2 Sales Report"
    cloned_report.metadata["author"] = "Bob"

    print("Original:")
    original_report.display()
    print("Clone (modified independently):")
    cloned_report.display()

    original_invoice = InvoiceDocument(
        title="Invoice #001",
        content="Services rendered.",
        metadata={"client": "XYZ Corp"},
        amount=4500
    )
    cloned_invoice = original_invoice.clone()
    cloned_invoice.title = "Invoice #002"
    cloned_invoice.amount = 7200
    print("Original Invoice:")
    original_invoice.display()
    print("Cloned Invoice:")
    cloned_invoice.display()

    # --- Factory ---
    print("\n--- Pattern 3: Factory Method (Notification System) ---")
    factories = [
        (EmailFactory(), "user@example.com"),
        (SMSFactory(),   "+201001234567"),
        (PushFactory(),  "device-abc-999"),
    ]
    for factory, target in factories:
        factory.notify(target, "Your order has been shipped!")

    print("\n" + "=" * 55)
    print("             DEMO COMPLETE")
    print("=" * 55)


if __name__ == "__main__":
    run_demo()
