from datetime import datetime

from Data.DataHelper import DataHelper

class InstalledPatchesRepository:
    def __init__(self):
        self.db = DataHelper()

        # Build the table if it doesn't exist
        self.build()

    def select(self, id: str) -> tuple:
        return self.db.selectFirstWithParams('''
            SELECT * FROM InstalledPatches WHERE PatchID = %s;
        ''', (id,))

    def insert(self, id: str, patchDate: datetime) -> None:
        self.db.execute('''
            INSERT INTO InstalledPatches (PatchID, PatchDate) VALUES (%s, %s);
        ''', (id, patchDate))

    def build(self) -> None:
        try:
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS InstalledPatches (
                    PatchID TEXT PRIMARY KEY,
                    PatchDate TIMESTAMP NOT NULL
                );
            ''', ())
        except:
            pass