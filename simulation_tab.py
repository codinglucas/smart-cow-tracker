from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QLineEdit, QFrame, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase
import pandas as pd
from datetime import datetime, timedelta

class SimulationTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("background-color: #6A994E;")
        
        # Load Montserrat Black and Bold fonts
        QFontDatabase.addApplicationFont("fonts/Montserrat-Black.ttf")
        QFontDatabase.addApplicationFont("fonts/Montserrat-Bold.ttf")
        
        self.initUI()

    def go_back(self):
        self.main_window.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        # Top sidebar with dark green background
        top_bar = QWidget()
        top_bar.setFixedHeight(150)
        top_bar.setStyleSheet("background-color: #386641;")
        top_bar_layout = QVBoxLayout()
        top_bar_layout.setContentsMargins(40, 20, 40, 20)

        # Title in top bar
        title = QLabel("SIMULAÇÃO")
        title.setFont(QFont("Montserrat Black", 32))
        title.setStyleSheet("color: #A7C957;")
        title.setAlignment(Qt.AlignCenter)
        top_bar_layout.addWidget(title)
        top_bar.setLayout(top_bar_layout)
        main_layout.addWidget(top_bar)

        # Content area
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #6A994E;")
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(40)
        content_widget.setLayout(content_layout)

        # Left column (inputs)
        left_column = QVBoxLayout()
        left_column.setSpacing(20)

        # GADO input (dropdown)
        gado_layout = self.create_input_group("GADO", is_combo=True)
        left_column.addLayout(gado_layout)

        # PESO DESEJADO input
        peso_layout = self.create_input_group("PESO DESEJADO")
        left_column.addLayout(peso_layout)

        # VALOR DO ARROBA input
        valor_layout = self.create_input_group("VALOR DO ARROBA")
        left_column.addLayout(valor_layout)

        left_column.addStretch()
        content_layout.addLayout(left_column)

        # Middle column (SIMULAR button)
        middle_column = QVBoxLayout()
        middle_column.addStretch()
        self.simular_btn = QPushButton("SIMULAR")
        self.simular_btn.setFont(QFont("Montserrat Bold", 16))
        self.simular_btn.setStyleSheet("""
            QPushButton {
                background-color: #A7C957;
                color: #386641;
                border-radius: 25px;
                padding: 15px 40px;
            }
            QPushButton:hover {
                background-color: #96B84C;
            }
        """)
        self.simular_btn.clicked.connect(self.calculate_simulation)
        middle_column.addWidget(self.simular_btn)
        middle_column.addStretch()
        content_layout.addLayout(middle_column)

        # Right column (results)
        right_column = QVBoxLayout()
        right_column.setSpacing(20)

        # DATA ESTIMADA with result
        data_layout = QHBoxLayout()
        data_layout.setSpacing(20)
        data_label = QLabel("DATA ESTIMADA")
        data_label.setFont(QFont("Montserrat Bold", 16))
        data_label.setStyleSheet("color: #F2E8CF;")
        data_label.setFixedWidth(200)
        data_layout.addWidget(data_label)

        self.data_input = QLineEdit()
        self.data_input.setFont(QFont("Montserrat Bold", 14))
        self.data_input.setStyleSheet("""
            QLineEdit {
                background-color: #F2E8CF;
                border-radius: 10px;
                padding: 8px;
                color: #386641;
                min-width: 120px;
            }
        """)
        self.data_input.setFixedHeight(40)
        self.data_input.setReadOnly(True)
        data_layout.addWidget(self.data_input)

        self.result_label = QLabel("= <span style='color: #BC4749; font-family: \"Montserrat Black\";'>X</span> reais")
        self.result_label.setFont(QFont("Montserrat Bold", 16))
        self.result_label.setStyleSheet("color: #A7C957;")
        self.result_label.setTextFormat(Qt.RichText)
        data_layout.addWidget(self.result_label)
        right_column.addLayout(data_layout)

        # "Daqui a X dias" label
        self.days_label = QLabel("Daqui a <span style='color: #BC4749; font-family: \"Montserrat Black\";'>X</span> dias")
        self.days_label.setFont(QFont("Montserrat Bold", 14))
        self.days_label.setStyleSheet("color: #A7C957;")
        self.days_label.setAlignment(Qt.AlignRight)
        self.days_label.setTextFormat(Qt.RichText)
        right_column.addWidget(self.days_label)

        # GMD (Ganho Médio Diário)
        gmd_layout = QHBoxLayout()
        gmd_layout.setSpacing(20)
        gmd_label = QLabel("GMD")
        gmd_label.setFont(QFont("Montserrat Bold", 16))
        gmd_label.setStyleSheet("color: #F2E8CF;")
        gmd_label.setFixedWidth(200)
        gmd_layout.addWidget(gmd_label)

        self.gmd_input = QLineEdit()
        self.gmd_input.setFont(QFont("Montserrat Bold", 14))
        self.gmd_input.setStyleSheet("""
            QLineEdit {
                background-color: #F2E8CF;
                border-radius: 10px;
                padding: 8px;
                color: #386641;
            }
        """)
        self.gmd_input.setFixedHeight(40)
        self.gmd_input.setReadOnly(True)
        gmd_layout.addWidget(self.gmd_input)
        right_column.addLayout(gmd_layout)

        right_column.addStretch()
        content_layout.addLayout(right_column)

        main_layout.addWidget(content_widget)

        # Back button
        back_button = QPushButton("← Voltar")
        back_button.setFont(QFont("Montserrat Bold", 14))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #A7C957;
                color: #454851;
                border-radius: 20px;
                padding: 10px;
            }
        """)
        back_button.setFixedWidth(150)
        back_button.clicked.connect(self.go_back)
        top_bar_layout.insertWidget(0, back_button, alignment=Qt.AlignLeft)

    def create_input_group(self, label_text, is_combo=False):
        layout = QHBoxLayout()
        layout.setSpacing(20)

        # Label
        label = QLabel(label_text)
        label.setFont(QFont("Montserrat Bold", 16))
        label.setStyleSheet("color: #F2E8CF;")
        label.setFixedWidth(250)
        layout.addWidget(label)

        if is_combo:
            # ComboBox for GADO
            self.gado_combo = QComboBox()
            self.gado_combo.setFont(QFont("Montserrat Bold", 14))
            self.gado_combo.setStyleSheet("""
                QComboBox {
                    background-color: #F2E8CF;
                    border-radius: 10px;
                    padding: 8px;
                    color: #386641;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox::down-arrow {
                    image: none;
                    border-width: 0px;
                }
            """)
            self.gado_combo.setFixedHeight(40)
            self.load_cow_ids()
            self.gado_combo.currentIndexChanged.connect(self.update_current_weight)
            layout.addWidget(self.gado_combo)
        else:
            # Input field
            input_field = QLineEdit()
            input_field.setFont(QFont("Montserrat Bold", 14))
            input_field.setStyleSheet("""
                QLineEdit {
                    background-color: #F2E8CF;
                    border-radius: 10px;
                    padding: 8px;
                    color: #386641;
                }
            """)
            input_field.setFixedHeight(40)
            if label_text == "PESO DESEJADO":
                self.peso_input = input_field
            elif label_text == "VALOR DO ARROBA":
                self.valor_input = input_field
            layout.addWidget(input_field)

        return layout

    def load_cow_ids(self):
        try:
            df = pd.read_excel("data/weights.xlsx")
            # Add default option first
            self.gado_combo.addItem("Escolha um gado")
            cow_ids = df.iloc[:, 0].unique()  # Get unique cow IDs from first column
            for cow_id in cow_ids:
                self.gado_combo.addItem(str(cow_id))
            # Trigger the currentIndexChanged signal to update the current weight
            self.gado_combo.setCurrentIndex(0)
        except Exception as e:
            print(f"Error loading cow IDs: {e}")

    def get_current_weight(self, cow_id):
        try:
            df = pd.read_excel("data/weights.xlsx")
            # Convert cow_id to string for comparison
            cow_id = str(cow_id)
            # Get the row for this cow
            row = df[df['cow_id'].astype(str) == cow_id]
            if not row.empty:
                # Get all columns except 'cow_id'
                weight_columns = [col for col in df.columns if col != 'cow_id']
                # Get timestamps from column headers
                timestamps = pd.to_datetime(weight_columns)
                # Get all weights for this cow
                weights = row[weight_columns].iloc[0]
                weights = weights.dropna()
                
                if not weights.empty:
                    last_weight = float(weights.iloc[-1])
                    
                    # Calculate GMD if we have at least 2 weights
                    gmd = None
                    if len(weights) >= 2:
                        # Get timestamps for this cow's measurements
                        weight_positions = weights.index.get_indexer(weights.index)
                        valid_timestamps = timestamps[weight_positions]
                        
                        # Calculate GMD using all available data points
                        days_diff = (valid_timestamps[-1] - valid_timestamps[0]).days
                        if days_diff > 0:
                            weight_diff = weights.iloc[-1] - weights.iloc[0]
                            gmd = weight_diff / days_diff
                    
                    print(f"Found last weight for cow {cow_id}: {last_weight}, GMD: {gmd}")
                    return last_weight, gmd
                    
            print(f"No weights found for cow {cow_id}")
        except Exception as e:
            print(f"Error getting current weight: {e}")
        return None, None

    def update_current_weight(self):
        cow_id = self.gado_combo.currentText()
        if cow_id and cow_id != "Escolha um gado":
            current_weight, gmd = self.get_current_weight(cow_id)
            if current_weight is not None:
                self.current_weight = current_weight
                self.current_gmd = gmd
                if gmd is not None:
                    self.gmd_input.setText(f"{gmd:.2f} kg/dia")
                else:
                    self.gmd_input.setText("N/A")
                print(f"Updated current weight to: {self.current_weight}, GMD: {gmd}")
            else:
                self.current_weight = None
                self.current_gmd = None
                self.gmd_input.setText("N/A")
                print("Could not update current weight - no data found")
        else:
            self.current_weight = None
            self.current_gmd = None
            self.gmd_input.setText("N/A")

    def calculate_simulation(self):
        try:
            # Get input values
            if not hasattr(self, 'current_weight') or self.current_weight is None:
                print("No current weight available")
                return
            
            print(f"Starting calculation with current weight: {self.current_weight}")
            
            target_weight = float(self.peso_input.text())
            print(f"Target weight: {target_weight}")
            
            arroba_value = float(self.valor_input.text())
            print(f"Arroba value: {arroba_value}")
            
            # Calculate weight difference
            weight_diff = target_weight - self.current_weight
            print(f"Weight difference: {weight_diff}")
            
            # Use the actual GMD if available, otherwise use default
            if hasattr(self, 'current_gmd') and self.current_gmd is not None and self.current_gmd > 0:
                gmd = self.current_gmd
                print(f"Using actual GMD: {gmd}")
            else:
                gmd = 0.8  # Default value if no historical data
                print(f"Using default GMD: {gmd}")
            
            # Calculate days needed based on the cow's GMD
            days_needed = max(1, int(weight_diff / gmd))  # Ensure at least 1 day
            print(f"Days needed: {days_needed}")
            
            # Calculate estimated date
            target_date = datetime.now() + timedelta(days=days_needed)
            formatted_date = target_date.strftime('%d/%m/%Y')
            print(f"Target date: {formatted_date}")
            
            self.data_input.setText(formatted_date)
            
            # Update days label with red number
            days_text = f"Daqui a <span style='color: #BC4749; font-family: \"Montserrat Black\";'>{days_needed}</span> dias"
            self.days_label.setText(days_text)
            self.days_label.setTextFormat(Qt.RichText)
            
            # Keep showing the cow's actual GMD
            gmd_text = f"{gmd:.2f} kg/dia"
            print(f"Cow's GMD: {gmd_text}")
            self.gmd_input.setText(gmd_text)
            
            # Calculate final value (1 arroba = 15kg)
            arrobas = target_weight / 15
            final_value = arrobas * arroba_value
            # Update the X in red color with Montserrat Black
            value_text = f"= <span style='color: #BC4749; font-family: \"Montserrat Black\";'>{final_value:.2f}</span> reais"
            self.result_label.setText(value_text)
            self.result_label.setTextFormat(Qt.RichText)
            
        except ValueError as ve:
            print(f"Value error in calculation: {ve}")
        except Exception as e:
            print(f"Error in simulation: {e}") 