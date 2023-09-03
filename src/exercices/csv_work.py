import csv


class PhoneContact:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone


class Phone:
    def __init__(self):
        self.contacts = []

    def load_contacts_from_csv(self, file):
        with open(file, newline='') as csvfile:
            fieldnames = ['Name', 'Phone']
            reader = csv.DictReader(csvfile, fieldnames)
            for row in reader:
                self.contacts.append(PhoneContact(row['Name'], row['Phone']))

    def search_contacts(self, phrase):
        count = 0
        for contact in self.contacts:
            if phrase.lower() in contact.name.lower() \
                    or phrase in contact.phone:
                print('{0} ({1})'.format(contact.name, contact.phone))
                count += 1
        if count == 0:
            print("No contacts found")


phone = Phone()
phone.load_contacts_from_csv('resources/contacts.csv')
phrase = input("Search contacts: ")
phone.search_contacts(phrase)
