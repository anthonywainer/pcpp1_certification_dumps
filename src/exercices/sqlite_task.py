import sqlite3


class Todo:
    def __init__(self):
        self.conn = sqlite3.connect('resources/todo.db')
        self.c = self.conn.cursor()
        self.create_tasks_table()

    def create_tasks_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                     id INTEGER PRIMARY KEY,
                     name TEXT NOT NULL,
                     priority INTEGER NOT NULL
                     );''')

    def add_task(self):
        name = input('Enter task name: ')
        priority = int(input('Enter priority: '))

        if len(name) == 0 or priority < 1:
            return

        if self.find_task(name) is not None:
            return

        self.c.execute(
            'INSERT INTO tasks (name, priority) VALUES (?,?)',
            (name, priority))
        self.conn.commit()

    def find_task(self, name):
        self.c.execute('SELECT * FROM tasks WHERE name = ?', (name,))
        return self.c.fetchone()

    def show_tasks(self):
        for row in self.c.execute('SELECT * FROM tasks'):
            print(row)

    def change_priority(self):
        task_id = int(input('Enter task id: '))
        new_priority = int(input('Enter new priority: '))

        if new_priority < 1:
            return

        self.c.execute(
            'UPDATE tasks SET priority = ? WHERE id = ?',
            (new_priority, task_id))
        self.conn.commit()

    def delete_task(self):
        task_id = int(input('Enter task id: '))

        self.c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()


class Menu:
    def __init__(self):
        self.app = Todo()

    def open(self):
        self.open = True
        while self.open:
            self.draw()
            option = int(input('Choose an option [1-5]: '))

            if option == 1:
                self.app.show_tasks()
            elif option == 2:
                self.app.add_task()
            elif option == 3:
                self.app.change_priority()
            elif option == 4:
                self.app.delete_task()
            elif option == 5:
                self.close()
            else:
                input('Option not found. Please choose an option again...')

    def draw(self):
        print('1. Show Tasks')
        print('2. Add Task')
        print('3. Change Priority')
        print('4. Delete Task')
        print('5. Exit')

    def close(self):
        self.open = False


menu = Menu()
menu.open()
