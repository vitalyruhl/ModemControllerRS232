"""Minimal editor for user profile notes; command edits remain model-driven."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from modem_controller.catalog.models import CommandCatalog


class CatalogEditor(QWidget):
    """Edits user-owned notes without transmitting, connecting, or launching tools."""

    notes_saved = Signal(str, str)

    def __init__(self, catalog: CommandCatalog, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._catalog = catalog
        self.profile_selector = QComboBox(self)
        self.notes = QPlainTextEdit(self)
        self.save_button = QPushButton("Notizen speichern", self)
        for profile in catalog.profiles:
            self.profile_selector.addItem(profile.name, profile.id)
        self.profile_selector.currentIndexChanged.connect(self._load_notes)
        self.save_button.clicked.connect(self._save)
        form = QFormLayout()
        form.addRow("Profil", self.profile_selector)
        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(self.notes)
        layout.addWidget(self.save_button)
        self._load_notes()

    def _load_notes(self) -> None:
        self.notes.setPlainText(
            self._catalog.profile(self.profile_selector.currentData()).user_notes
        )

    def _save(self) -> None:
        self.notes_saved.emit(
            self.profile_selector.currentData(), self.notes.toPlainText()
        )
