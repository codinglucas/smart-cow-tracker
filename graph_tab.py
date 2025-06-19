from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QLineEdit, QFrame, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class GraphTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
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
        title = QLabel("GRÁFICO")
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

        # Left column (graph and cow selector)
        left_column = QVBoxLayout()
        left_column.setSpacing(20)

        # ESCOLHER GADO label and combo
        gado_layout = QVBoxLayout()
        gado_label = QLabel("ESCOLHER GADO")
        gado_label.setFont(QFont("Montserrat Bold", 16))
        gado_label.setStyleSheet("color: #F2E8CF;")
        gado_layout.addWidget(gado_label)

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
        self.gado_combo.currentIndexChanged.connect(self.update_plot)
        gado_layout.addWidget(self.gado_combo)
        left_column.addLayout(gado_layout)

        # Graph
        graph_container = QFrame()
        graph_container.setStyleSheet("QFrame { background-color: #F2E8CF; border-radius: 20px; }")
        graph_container.setMinimumSize(600, 400)
        graph_layout = QVBoxLayout(graph_container)
        graph_layout.setContentsMargins(20, 20, 20, 20)

        # Create the matplotlib figure
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        graph_layout.addWidget(self.canvas)

        # Add labels
        self.ax.set_xlabel('pesagem', color='#386641')
        self.ax.set_ylabel('kg', color='#386641')
        self.figure.patch.set_facecolor('#F2E8CF')
        self.ax.set_facecolor('#F2E8CF')

        left_column.addWidget(graph_container)
        content_layout.addLayout(left_column)

        # Right column (statistics)
        right_column = QVBoxLayout()
        right_column.setSpacing(30)

        # Create statistics fields
        self.peso_medio = self.create_stat_field("PESO MÉDIO")
        self.gmd = self.create_stat_field("GMD")
        self.previsao = self.create_stat_field("PREVISÃO PESO MÉDIO\nDAQUI 90 DIAS")

        right_column.addLayout(self.peso_medio)
        right_column.addLayout(self.gmd)
        right_column.addLayout(self.previsao)
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

        # Initial plot update
        self.update_plot()

    def create_stat_field(self, label_text):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Label
        label = QLabel(label_text)
        label.setFont(QFont("Montserrat Bold", 16))
        label.setStyleSheet("color: #F2E8CF;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Value field
        value_field = QLineEdit()
        value_field.setFont(QFont("Montserrat Bold", 14))
        value_field.setStyleSheet("""
            QLineEdit {
                background-color: #F2E8CF;
                border-radius: 10px;
                padding: 8px;
                color: #386641;
            }
        """)
        value_field.setFixedHeight(40)
        value_field.setReadOnly(True)
        value_field.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_field)

        return layout

    def load_cow_ids(self):
        try:
            df = pd.read_excel("data/weights.xlsx")
            self.gado_combo.addItem("Todos")
            cow_ids = df.iloc[:, 0].unique()
            for cow_id in cow_ids:
                self.gado_combo.addItem(str(cow_id))
        except Exception as e:
            print(f"Error loading cow IDs: {e}")

    def calculate_statistics(self):
        try:
            df = pd.read_excel("data/weights.xlsx")
            selected = self.gado_combo.currentText()
            
            print(f"\nCalculating statistics for: {selected}")
            print("DataFrame head:")
            print(df.head())
            
            # Get timestamps from column headers (excluding the first column which is cow_id)
            weight_columns = [col for col in df.columns if col != 'cow_id']
            timestamps = pd.to_datetime(weight_columns)
            print("\nTimestamps:", timestamps)
            
            if selected == "Todos":
                # Get all valid weights for each timestamp
                all_current_weights = []  # For peso médio
                all_gmds = []  # For GMD
                
                for _, row in df.iterrows():
                    weights = row.iloc[1:].dropna()
                    if len(weights) > 0:
                        # Convert weights to float
                        weights = weights.astype(float)
                        print(f"\nProcessing cow weights: {weights.values}")
                        # Add last weight for current average
                        all_current_weights.append(weights.iloc[-1])
                        
                        if len(weights) >= 2:
                            # Get timestamps for this cow's measurements
                            # Get numeric positions of non-null values
                            weight_positions = weights.index.get_indexer(weights.index)
                            valid_timestamps = timestamps[weight_positions]
                            print(f"Valid timestamps: {valid_timestamps}")
                            
                            # Calculate GMD using the formula: (f(x) - f(x')) / (x - x')
                            days_diff = (valid_timestamps[-1] - valid_timestamps[0]).days
                            print(f"Days difference: {days_diff}")
                            
                            if days_diff > 0:  # Avoid division by zero
                                weight_diff = weights.iloc[-1] - weights.iloc[0]
                                gmd = weight_diff / days_diff
                                print(f"Weight diff: {weight_diff}, GMD: {gmd}")
                                all_gmds.append(gmd)
                
                print(f"\nAll current weights: {all_current_weights}")
                print(f"All GMDs: {all_gmds}")
                
                if all_current_weights:
                    # Calculate current average weight
                    current_avg = np.mean(all_current_weights)
                    print(f"Current average weight: {current_avg:.1f}")
                    self.peso_medio.itemAt(1).widget().setText(f"{current_avg:.1f} kg")
                    
                    if all_gmds:
                        # Calculate average GMD
                        avg_gmd = np.mean(all_gmds)
                        print(f"Average GMD: {avg_gmd:.2f}")
                        self.gmd.itemAt(1).widget().setText(f"{avg_gmd:.2f} kg/dia")
                        
                        # Calculate prediction using f(z+90) = (GMD * 90) + f(x)
                        predicted_weight = (avg_gmd * 90) + current_avg
                        print(f"Predicted weight: {predicted_weight:.1f}")
                        self.previsao.itemAt(1).widget().setText(f"{predicted_weight:.1f} kg")
                    else:
                        print("No GMDs calculated")
                        self.gmd.itemAt(1).widget().setText("N/A")
                        self.previsao.itemAt(1).widget().setText("N/A")
                else:
                    print("No current weights found")
                    self.peso_medio.itemAt(1).widget().setText("N/A")
                    self.gmd.itemAt(1).widget().setText("N/A")
                    self.previsao.itemAt(1).widget().setText("N/A")
            else:
                # Calculate for selected cow
                row = df[df.iloc[:, 0].astype(str) == selected].iloc[0]
                weights = row.iloc[1:].dropna()
                
                print(f"\nSelected cow weights: {weights}")
                
                if len(weights) > 0:
                    # Convert weights to float
                    weights = weights.astype(float)
                    # Calculate average weight
                    avg_weight = weights.mean()
                    print(f"Average weight: {avg_weight:.1f}")
                    self.peso_medio.itemAt(1).widget().setText(f"{avg_weight:.1f} kg")
                    
                    if len(weights) >= 2:
                        # Get timestamps for this cow's measurements
                        # Get numeric positions of non-null values
                        weight_positions = weights.index.get_indexer(weights.index)
                        valid_timestamps = timestamps[weight_positions]
                        print(f"Valid timestamps: {valid_timestamps}")
                        
                        # Calculate GMD using the formula: (f(x) - f(x')) / (x - x')
                        days_diff = (valid_timestamps[-1] - valid_timestamps[0]).days
                        print(f"Days difference: {days_diff}")
                        
                        if days_diff > 0:
                            weight_diff = weights.iloc[-1] - weights.iloc[0]
                            gmd = weight_diff / days_diff
                            print(f"Weight diff: {weight_diff}, GMD: {gmd:.2f}")
                            self.gmd.itemAt(1).widget().setText(f"{gmd:.2f} kg/dia")
                            
                            # Calculate prediction using f(z+90) = (GMD * 90) + f(x)
                            predicted_weight = (gmd * 90) + weights.iloc[-1]
                            print(f"Predicted weight: {predicted_weight:.1f}")
                            self.previsao.itemAt(1).widget().setText(f"{predicted_weight:.1f} kg")
                        else:
                            print("Zero days difference")
                            self.gmd.itemAt(1).widget().setText("N/A")
                            self.previsao.itemAt(1).widget().setText("N/A")
                    else:
                        print("Not enough measurements")
                        self.gmd.itemAt(1).widget().setText("N/A")
                        self.previsao.itemAt(1).widget().setText("N/A")
                else:
                    print("No weights found")
                    self.peso_medio.itemAt(1).widget().setText("N/A")
                    self.gmd.itemAt(1).widget().setText("N/A")
                    self.previsao.itemAt(1).widget().setText("N/A")
                
        except Exception as e:
            print(f"Error calculating statistics: {e}")
            import traceback
            print(traceback.format_exc())

    def update_plot(self):
        try:
            self.ax.clear()
            df = pd.read_excel("data/weights.xlsx")
            selected = self.gado_combo.currentText()

            if selected == "Todos":
                # Plot all cows
                for _, row in df.iterrows():
                    cow_id = int(row.iloc[0])  # Convert to integer to remove decimal
                    weights = row.iloc[1:].dropna().astype(float)
                    if len(weights) > 0:
                        x = range(1, len(weights) + 1)
                        self.ax.plot(x, weights, marker='o', label=f'Gado {cow_id}', linewidth=2)
                
                # Add legend with Montserrat Bold font at bottom right
                legend = self.ax.legend(prop={'family': 'Montserrat', 'weight': 'bold'}, 
                                      loc='lower right',
                                      bbox_to_anchor=(1, 0))
                legend.get_frame().set_facecolor('#F2E8CF')
                legend.get_frame().set_edgecolor('#386641')
                for text in legend.get_texts():
                    text.set_color('#386641')
                    text.set_fontfamily('Montserrat')
            else:
                # Plot selected cow
                row = df[df.iloc[:, 0].astype(str) == selected].iloc[0]
                weights = row.iloc[1:].dropna().astype(float)
                if len(weights) > 0:
                    x = range(1, len(weights) + 1)
                    self.ax.plot(x, weights, marker='o', color='#A7C957', linewidth=2)

            # Configure grid
            self.ax.grid(True, color='#386641', linestyle='-', linewidth=0.5, alpha=0.2)
            self.ax.set_axisbelow(True)

            # Set integer ticks on x-axis
            self.ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

            # Update tick colors and font
            self.ax.tick_params(colors='#386641')
            for label in self.ax.get_xticklabels() + self.ax.get_yticklabels():
                label.set_fontfamily('Montserrat Bold')
                label.set_fontweight('bold')
            
            # Configure spines
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.spines['bottom'].set_color('#386641')
            self.ax.spines['left'].set_color('#386641')

            # Update statistics
            self.calculate_statistics()

            # Adjust layout to prevent legend from being cut off
            self.figure.tight_layout()
            self.canvas.draw()

        except Exception as e:
            print(f"Error updating plot: {e}")

