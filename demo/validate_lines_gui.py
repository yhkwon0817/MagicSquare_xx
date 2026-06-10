"""Minimal PyQt demo — 4×4 grid + validate_lines."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from validate_lines import validate_lines

VALID_GRID = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

LINE_LABELS = {
    "row:0": "R1",
    "row:1": "R2",
    "row:2": "R3",
    "row:3": "R4",
    "col:0": "C1",
    "col:1": "C2",
    "col:2": "C3",
    "col:3": "C4",
    "diag:main": "D1 (주대각)",
    "diag:anti": "D2 (반대각)",
}


class ValidateLinesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MagicSquare_xx — validate_lines 데모")
        self.setMinimumSize(420, 520)

        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)

        layout.addWidget(QLabel("4×4 격자 (빈칸=0, 1~16)"))

        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(6)
        self.cells: list[list[QLineEdit]] = []
        for row in range(4):
            row_cells: list[QLineEdit] = []
            for col in range(4):
                cell = QLineEdit()
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setMaxLength(2)
                cell.setPlaceholderText("0")
                cell.setFixedSize(56, 36)
                grid_layout.addWidget(cell, row, col)
                row_cells.append(cell)
            self.cells.append(row_cells)
        layout.addWidget(grid_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        buttons = QHBoxLayout()
        load_btn = QPushButton("정답 격자 불러오기")
        load_btn.clicked.connect(self._load_valid_grid)
        validate_btn = QPushButton("10선 검증")
        validate_btn.clicked.connect(self._on_validate)
        clear_btn = QPushButton("초기화")
        clear_btn.clicked.connect(self._clear_grid)
        buttons.addWidget(load_btn)
        buttons.addWidget(validate_btn)
        buttons.addWidget(clear_btn)
        layout.addLayout(buttons)

        self.status_label = QLabel("결과: —")
        self.status_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.status_label)

        self.detail = QTextEdit()
        self.detail.setReadOnly(True)
        self.detail.setPlaceholderText("틀린 줄 상세 (fail 시)")
        self.detail.setMaximumHeight(160)
        layout.addWidget(self.detail)

    def _clear_grid(self):
        for row in self.cells:
            for cell in row:
                cell.clear()
        self.status_label.setText("결과: —")
        self.detail.clear()

    def _load_valid_grid(self):
        for r in range(4):
            for c in range(4):
                self.cells[r][c].setText(str(VALID_GRID[r][c]))
        self.status_label.setText("결과: —")
        self.detail.clear()

    def _read_grid(self) -> list[list[int]] | None:
        grid: list[list[int]] = []
        for r in range(4):
            row: list[int] = []
            for c in range(4):
                text = self.cells[r][c].text().strip()
                if text == "":
                    row.append(0)
                    continue
                try:
                    value = int(text)
                except ValueError:
                    QMessageBox.warning(
                        self,
                        "입력 오류",
                        f"({r + 1}, {c + 1}) 칸에 숫자를 입력하세요.",
                    )
                    return None
                if value < 0 or value > 16:
                    QMessageBox.warning(
                        self,
                        "입력 오류",
                        f"({r + 1}, {c + 1}) 칸은 0~16만 허용됩니다.",
                    )
                    return None
                row.append(value)
            grid.append(row)
        return grid

    def _on_validate(self):
        grid = self._read_grid()
        if grid is None:
            return

        result = validate_lines(grid)
        status = result["status"]

        colors = {
            "pass": "#1b7f3d",
            "fail": "#c0392b",
            "incomplete": "#b8860b",
        }
        labels = {
            "pass": "PASS — 10선 합 34",
            "fail": "FAIL — 틀린 줄 있음",
            "incomplete": "INCOMPLETE — 빈칸(0) 포함",
        }
        self.status_label.setText(f"결과: {labels[status]}")
        self.status_label.setStyleSheet(
            f"font-weight: bold; font-size: 14px; color: {colors[status]};"
        )

        if status == "fail":
            lines = []
            for item in result["failed_lines"]:
                name = LINE_LABELS.get(item["id"], item["id"])
                lines.append(
                    f"{name} ({item['id']}): 합 {item['sum']} "
                    f"(기대 {item['expected']})"
                )
            self.detail.setPlainText("\n".join(lines))
        else:
            self.detail.clear()


def main():
    app = QApplication(sys.argv)
    window = ValidateLinesWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
