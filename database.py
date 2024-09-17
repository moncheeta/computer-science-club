from models import Project
import sqlite3
import pickle


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(
            "database.db", check_same_thread=False
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS projects (
            name text NOT NULL,
            description text,
            authors text NOT NULL,
            source text
        )"""
        )
        self.write()
        self.read()

    def __del__(self):
        self.connection.close()

    def read(self):
        self.projects = []
        self.cursor.execute("SELECT * FROM projects")
        for data in self.cursor.fetchall():
            name = data[0]
            description = data[1]
            authors = pickle.loads(data[2])
            source = data[3]
            project = Project(name, description, authors, source)
            self.projects.append(project)
        return self.projects

    def write(self):
        self.connection.commit()

    def add(self, project):
        self.projects.append(project)
        data = (
            project.name,
            project.description,
            pickle.dumps(project.authors),
            project.source,
        )
        self.cursor.execute("INSERT INTO projects VALUES (?, ?, ?, ?)", data)
        self.write()


database = Database()
