import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                           QWidget, QVBoxLayout, QHBoxLayout, QFrame, QGraphicsDropShadowEffect)
from PyQt5.QtGui import QFont, QPalette, QColor, QFontDatabase, QTransform, QPainter
from PyQt5.QtCore import Qt
from graph_tab import GraphTab
from simulation_tab import SimulationTab
from generate_pdf_report import generate_report_from_gui
from bluetooth_manager import BluetoothManager
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import matplotlib.font_manager as fm

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CATTLER")
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #6A994E;")

        # Load and register Montserrat fonts
        font_paths = {
            'Montserrat-Black': 'fonts/Montserrat-Black.ttf',
            'Montserrat-Bold': 'fonts/Montserrat-Bold.ttf'
        }
        
        for font_name, font_path in font_paths.items():
            # Add font for Qt
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id < 0:
                print(f"Error: Could not load {font_name} font for Qt")
            
            # Register font for matplotlib
            try:
                fm.fontManager.addfont(font_path)
            except Exception as e:
                print(f"Error registering {font_name} for matplotlib: {e}")

        # Set Montserrat as the default font family for matplotlib
        plt.rcParams['font.family'] = 'Montserrat'
        
        # Initialize Bluetooth manager
        self.bluetooth_manager = BluetoothManager()
        self.bluetooth_manager.connection_status.connect(self.update_connection_status)
        self.bluetooth_manager.error_message.connect(self.show_bluetooth_error)
        self.bluetooth_manager.start()

        self.initUI()

    def show_bluetooth_error(self, error_message):
        self.connection_status.setText(error_message)
        self.connection_status.setStyleSheet("""
            QLabel {
                color: #386641;
                background-color: #F2E8CF;
                padding: 15px 25px;
                border-radius: 20px;
            }
        """)
        self.pesar_btn.setEnabled(False)

    def update_connection_status(self, is_connected):
        if is_connected:
            self.connection_status.setText("Ready to use!")
            self.connection_status.setStyleSheet("""
                QLabel {
                    color: #386641;
                    background-color: #F2E8CF;
                    padding: 15px 25px;
                    border-radius: 20px;
                }
            """)
            self.pesar_btn.setEnabled(True)
        else:
            self.connection_status.setText("Por favor conecte ao aparelho")
            self.connection_status.setStyleSheet("""
                QLabel {
                    color: #386641;
                    background-color: #F2E8CF;
                    padding: 15px 25px;
                    border-radius: 20px;
                }
            """)
            self.pesar_btn.setEnabled(False)

    def closeEvent(self, event):
        self.bluetooth_manager.stop()
        event.accept()

    def add_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(4)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 80))
        widget.setGraphicsEffect(shadow)

    def create_sidebar_button(self, text, is_white=False):
        btn = QPushButton(text)
        btn.setFont(QFont("Montserrat Bold", 16))
        if text == "CATALOGAR":
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #A7C957;
                    color: #454851;
                    border-radius: 25px;
                    padding: 10px;
                    transition: background-color 0.3s;
                    cursor: pointer;
                }
                QPushButton:hover {
                    background-color: #96B84C;
                    cursor: pointer;
                }
                QPushButton:disabled {
                    color: #666666;
                    cursor: default;
                }
            """)
        elif is_white:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #F2E8CF;
                    color: #BC4749;
                    border-radius: 25px;
                    padding: 10px;
                    transition: background-color 0.3s;
                    cursor: pointer;
                }
                QPushButton:hover {
                    background-color: #E6DCC4;
                    cursor: pointer;
                }
                QPushButton:disabled {
                    color: #666666;
                    cursor: default;
                }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #A7C957;
                    color: #454851;
                    border-radius: 25px;
                    padding: 10px;
                    transition: background-color 0.3s;
                    cursor: pointer;
                }
                QPushButton:hover {
                    background-color: #96B84C;
                    cursor: pointer;
                }
            """)
        btn.setFixedSize(180, 50)
        btn.setCursor(Qt.PointingHandCursor)
        self.add_shadow(btn)
        return btn

    def create_vaccine_button(self, text):
        btn = QPushButton(text)
        btn.setFont(QFont("Montserrat Bold", 14))
        btn.setStyleSheet("""
            QPushButton {
                background-color: #BC4749;
                color: #F2E8CF;
                border-radius: 25px;
                padding: 10px;
                transition: background-color 0.3s;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #A63E40;
                cursor: pointer;
            }
        """)
        btn.setFixedSize(180, 50)
        btn.setCursor(Qt.PointingHandCursor)
        self.add_shadow(btn)
        return btn

    def show_graph_tab(self):
        self.graph_tab = GraphTab(self)
        self.setCentralWidget(self.graph_tab)

    def show_simulation_tab(self):
        self.simulation_tab = SimulationTab(self)
        self.setCentralWidget(self.simulation_tab)

    def generate_pdf(self):
        generate_report_from_gui()

    def initUI(self):
        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left sidebar with darker green background
        sidebar_widget = QWidget()
        sidebar_widget.setStyleSheet("background-color: #386641;")
        sidebar_widget.setFixedWidth(220)
        sidebar = QVBoxLayout(sidebar_widget)
        sidebar.setContentsMargins(20, 40, 20, 20)
        sidebar.setSpacing(20)

        # CATTLER title in sidebar
        title = QLabel("CATTLER")
        title.setFont(QFont("Montserrat Black", 32))
        title.setStyleSheet("color: #A7C957;")
        title.setAlignment(Qt.AlignLeft)
        sidebar.addWidget(title)

        sidebar.addSpacing(20)

        # Sidebar buttons
        self.pesar_btn = self.create_sidebar_button("PESAR", True)
        self.pesar_btn.setEnabled(False)
        ver_grafico_btn = self.create_sidebar_button("VER GRÁFICO")
        ver_grafico_btn.clicked.connect(self.show_graph_tab)
        gerar_pdf_btn = self.create_sidebar_button("GERAR PDF")
        gerar_pdf_btn.clicked.connect(self.generate_pdf)
        simulacao_btn = self.create_sidebar_button("SIMULAÇÃO")
        simulacao_btn.clicked.connect(self.show_simulation_tab)
        catalogar_btn = self.create_sidebar_button("CATALOGAR", True)
        catalogar_btn.setEnabled(False)

        sidebar.addWidget(self.pesar_btn)
        sidebar.addWidget(ver_grafico_btn)
        sidebar.addWidget(gerar_pdf_btn)
        sidebar.addWidget(simulacao_btn)
        sidebar.addWidget(catalogar_btn)
        sidebar.addStretch()

        # Custom widget to handle rotated text
        class RotatedLabel(QLabel):
            def paintEvent(self, event):
                painter = QPainter(self)
                painter.setRenderHint(QPainter.Antialiasing)
                painter.setFont(self.font())
                painter.setPen(QColor("#F2E8CF"))
                
                # Calculate position to center the rotated text
                rect = self.rect()
                painter.translate(rect.center())
                painter.rotate(-90)
                
                text_rect = painter.fontMetrics().boundingRect(self.text())
                painter.drawText(-text_rect.width()//2, text_rect.height()//4, self.text())

        # Central area
        central_area = QVBoxLayout()
        central_area.setContentsMargins(40, 20, 40, 20)
        central_area.setSpacing(30)
        
        # PESAR button and status container
        pesar_status_container = QHBoxLayout()
        pesar_status_container.setSpacing(20)

        # Large PESAR button
        central_pesar = QPushButton("PESAR")
        central_pesar.setFont(QFont("Montserrat Bold", 40))
        central_pesar.setStyleSheet("""
            QPushButton {
                background-color: #F2E8CF;
                color: #BC4749;
                border-radius: 60px;
                padding: 20px;
                transition: background-color 0.3s;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #E6DCC4;
                cursor: pointer;
            }
            QPushButton:disabled {
                color: #BC4749;
                cursor: default;
            }
        """)
        central_pesar.setFixedSize(450, 120)
        central_pesar.setCursor(Qt.PointingHandCursor)
        central_pesar.setEnabled(False)
        self.add_shadow(central_pesar)
        pesar_status_container.addWidget(central_pesar)

        # Connection status
        self.connection_status = QLabel("Por favor conecte ao aparelho")
        self.connection_status.setFont(QFont("Montserrat", 12))
        self.connection_status.setStyleSheet("""
            QLabel {
                color: #386641;
                background-color: #F2E8CF;
                padding: 15px 25px;
                border-radius: 20px;
            }
        """)
        self.connection_status.setAlignment(Qt.AlignCenter)
        pesar_status_container.addWidget(self.connection_status)
        
        central_area.addLayout(pesar_status_container)

        # Graph title
        graph_title = QLabel("GADO")
        graph_title.setFont(QFont("Montserrat", 20))
        graph_title.setStyleSheet("color: #F2E8CF;")
        graph_title.setAlignment(Qt.AlignCenter)
        central_area.addWidget(graph_title)

        # Graph container with labels
        graph_section = QVBoxLayout()
        graph_section.setSpacing(5)

        # Y-axis label and graph container
        graph_row = QHBoxLayout()
        graph_row.setSpacing(10)
        graph_row.setAlignment(Qt.AlignCenter)

        # Y-axis label
        y_label_rotated = RotatedLabel("kg")
        y_label_rotated.setFont(QFont("Montserrat", 12))
        y_label_rotated.setStyleSheet("color: #F2E8CF;")
        y_label_rotated.setFixedSize(20, 320)
        graph_row.addWidget(y_label_rotated)

        # Graph container
        graph_container = QFrame()
        graph_container.setStyleSheet("QFrame { background-color: #F2E8CF; border-radius: 20px; }")
        graph_container.setFixedSize(430, 320)
        graph_layout = QVBoxLayout(graph_container)
        graph_layout.setContentsMargins(10, 10, 10, 10)
        
        self.figure, self.ax = plt.subplots(figsize=(4.1, 2.9))
        self.figure.set_facecolor('#F2E8CF')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(410, 300)
        self.update_plot()
        graph_layout.addWidget(self.canvas, alignment=Qt.AlignCenter)
        
        graph_row.addWidget(graph_container)
        graph_section.addLayout(graph_row)

        # X-axis label
        x_label = QLabel("pesagem")
        x_label.setFont(QFont("Montserrat", 12))
        x_label.setStyleSheet("color: #F2E8CF;")
        x_label.setAlignment(Qt.AlignCenter)
        graph_section.addWidget(x_label, alignment=Qt.AlignCenter)

        central_area.addLayout(graph_section)

        # Right panel with reduced left margin
        right_panel = QVBoxLayout()
        right_panel.setContentsMargins(0, 20, 20, 20)  # No left margin
        right_panel.setSpacing(15)
        
        right_panel.addSpacing(100)  # Reduced from 200
        
        vacinacao_label = QLabel("VACINAR")
        vacinacao_label.setFont(QFont("Montserrat", 20))
        vacinacao_label.setStyleSheet("color: #F2E8CF;")
        vacinacao_label.setAlignment(Qt.AlignCenter)
        right_panel.addWidget(vacinacao_label)

        right_panel.addSpacing(20)

        # Add vaccine buttons
        for _ in range(5):
            vaccine_btn = self.create_vaccine_button("001 - 50 dias")
            right_panel.addWidget(vaccine_btn)
        
        right_panel.addStretch()

        # Add all sections to main layout
        central_widget = QWidget()
        central_widget.setLayout(central_area)
        
        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        right_widget.setFixedWidth(220)

        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(central_widget)
        main_layout.addWidget(right_widget)

    def update_plot(self):
        self.ax.clear()
        try:
            df = pd.read_excel("data/weights.xlsx")
            df.columns = df.columns.astype(str)

            for index, row in df.iterrows():
                # Get only the weight values (excluding the ID)
                weights = row.iloc[1:].values
                # Remove NaN values if any
                weights = weights[~pd.isna(weights)]
                if len(weights) > 0:
                    # Create x values starting from 1 regardless of when measurements started
                    x = range(1, len(weights) + 1)
                    self.ax.plot(x, weights, marker='o', color='#A7C957', linewidth=2, label=f"Cow {row.iloc[0]}")

            self.ax.set_facecolor('#F2E8CF')
            
            # Configure grid
            self.ax.grid(True, color='#386641', linestyle='-', linewidth=0.5, alpha=0.2)
            self.ax.set_axisbelow(True)  # Put grid behind the plot lines
            
            # Set integer ticks on x-axis
            self.ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
            
            # Remove all labels as they're handled by QLabels
            self.ax.set_xlabel("")
            self.ax.set_ylabel("")
            
            # Update tick fonts and colors
            for label in self.ax.get_xticklabels() + self.ax.get_yticklabels():
                label.set_fontsize(10)
                label.set_color('#386641')

            # Configure spines
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.spines['bottom'].set_color('#386641')
            self.ax.spines['left'].set_color('#386641')
            
            # Adjust layout to fill the figure
            self.figure.tight_layout(pad=0.2)
            self.canvas.draw()
        except Exception as e:
            print(f"Error updating plot: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())