from src.models.notes_fields.notes_fields import Title, Text


class Note:
    def __init__(self, title, text=None):
        self.title = Title(title)
        self.text = Text(text)
        self.tags = []

    def __str__(self):
        if self.text:
            return f"Заголовок: {self.title.value}\nТекст: {self.text.value}"
        else:
            return f"Заголовок: {self.title.value}"

    def add_tags(self, tags):
        self.tags = [str(tag).strip() for tag in tags.split(',')]


class Notes:
    def __init__(self):
        self.notes = []

    def add_note(self, title, text=None, tags=None):
        note = Note(title, text)
        if tags:
            note.add_tags(tags)
        self.notes.append(note)

    def delete_note_by_title(self, title):
        for note in self.notes:
            if note.title.value == title:
                self.notes.remove(note)
                return f"Примітку '{title}' видалено."
        return f"Примітку '{title}' не знайдено."

    def find_note_by_title(self, title):
        for note in self.notes:
            if note.title.value == title:
                return str(note)
        return f"Примітку '{title}' не знайдено."

    def find_note_by_tag(self, tag):
        notes = []
        for note in self.notes:
            if tag in note.tags:
                text = note.text.value
                notes.append(text if text else note.title.value)
        if notes:
            return '\n'.join(notes)
        return f"Приміток за тегом: '{tag}' не знайдено."

    def update_note_by_title(self, title, new_title, new_text):
        for note in self.notes:
            if note.title.value == title:
                note.title.value = new_title
                note.text.value = new_text
                return f"Примітку '{title}' оновлено."
        return f"Примітку '{title}' не знайдено."

    def show_notes(self):
        notes = []
        for note in self.notes:
            tags = ','.join(note.tags)
            notes.append(f'Заголовок {note.title.value}: теги {tags}')
        if notes:
            return '\n'.join(notes)
        return f"Приміток не знайдено."
