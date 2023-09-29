import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QComboBox, QPushButton, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt


class StatisticalTestRecommender(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Statistical Test Recommender')
        self.setWindowIcon(QIcon('stat.ico'))
        # Center the window on the screen
        self.setGeometry(0, 0, 600, 400)
        screen_center = QApplication.desktop().screenGeometry().center()
        window_center = self.geometry().center()
        self.move(screen_center - window_center)
        # Create a QLabel for the email link
        self.email_label = QLabel('<a href="mailto:mahsatorabi515@gmail.com">mahsatorabi515@gmail.com</a>')
        self.email_label.setOpenExternalLinks(True)
        self.email_label.setAlignment(Qt.AlignCenter)


        # Create input fields and labels
        font = QFont('Cascadia Code Light', 14)

        self.sample_size_label = QLabel('Sample Size:')
        self.sample_size_label.setFont(font)
        self.sample_size_input = QLineEdit(self)
        self.sample_size_input.setFont(font)

        self.num_groups_label = QLabel('Number of Groups:')
        self.num_groups_label.setFont(font)
        self.num_groups_input = QLineEdit(self)
        self.num_groups_input.setFont(font)

        self.num_variables_label = QLabel('Number of Variables:')
        self.num_variables_label.setFont(font)
        self.num_variables_input = QLineEdit(self)
        self.num_variables_input.setFont(font)

        # Create the 'Data Type' dropdown
        self.data_type_label = QLabel('Data Type:')
        self.data_type_label.setFont(font)
        self.data_type_combo = QComboBox(self)
        self.data_type_combo.setFont(font)
        self.data_type_combo.addItem('Parametric')
        self.data_type_combo.addItem('Non-parametric')
        self.data_type_combo.addItem('Binomial')

        # Create the 'Independence of Groups' dropdown
        self.independence_label = QLabel('Groups Independence:')
        self.independence_label.setFont(font)
        self.independence_combo = QComboBox(self)
        self.independence_combo.setFont(font)
        self.independence_combo.addItem('Independent')
        self.independence_combo.addItem('Dependent')

        # Create the 'Recommend Test' button
        self.recommend_button = QPushButton('Recommend Test', self)
        self.recommend_button.setFont(font)
        self.recommend_button.clicked.connect(self.recommend_test)

        # Create the output text box (fixed-size box)
        self.output_box = QTextEdit(self)
        self.output_box.setFont(font)
        self.output_box.setFixedSize(600, 100)

        # Create a vertical layout
        layout = QVBoxLayout()
        layout.addWidget(self.sample_size_label)
        layout.addWidget(self.sample_size_input)
        layout.addWidget(self.num_groups_label)
        layout.addWidget(self.num_groups_input)
        layout.addWidget(self.num_variables_label)
        layout.addWidget(self.num_variables_input)
        layout.addWidget(self.data_type_label)
        layout.addWidget(self.data_type_combo)
        layout.addWidget(self.independence_label)
        layout.addWidget(self.independence_combo)
        layout.addWidget(self.recommend_button)
        layout.addWidget(self.output_box)
        layout.addWidget(self.email_label) 

        self.setLayout(layout)

        # Apply stylesheets for customized appearance
        app.setStyleSheet('''
            QWidget {
                background-color: lightblue;
            }

            QLineEdit {
                background-color: lightpink;
            }

            QComboBox {
                background-color: lightpink;
            }

            QPushButton {
                background-color: shinyblue;
                border-style: outset;
                border-width: 2px;
                border-radius: 10px;
                border-color: shinyblue;
                padding: 4px;
                color: white;
            }

            QPushButton:hover {
                background-color: #3daee9;
            }

            QPushButton:pressed {
                background-color: #005cbf;
            }
            QTextEdit {
                background-color: white;
            }
        ''')

    def recommend_test(self):
        try:
            sample_size = int(self.sample_size_input.text())
            num_groups = int(self.num_groups_input.text())
            num_variables = int(self.num_variables_input.text())

            data_type = self.data_type_combo.currentText()
            is_parametric = True if data_type == 'Parametric' else False
            is_binomial = True if data_type == 'Binomial' else False
            is_independent = True if self.independence_combo.currentText() == 'Independent' else False

            # Check conditions and recommend a test based on the user input
            if is_binomial:
                test_name = "Binomial test"
            elif is_independent:
                if num_groups == 2 and num_variables == 1:
                    if is_parametric:
                        test_name = "Independent t-test"
                    else:
                        test_name = "Mann-Whitney U test"
                elif num_groups > 2 and num_variables == 1:
                    if is_parametric:
                        test_name = "One-way ANOVA"
                    else:
                        test_name = "Kruskal-Wallis test"
                elif num_groups == 2 and num_variables == 2:
                    if is_parametric:
                        test_name = "Paired t-test"
                    else:
                        test_name = "Wilcoxon signed-rank test"
                elif num_groups > 2 and num_variables == 2:
                    test_name = "Two-way ANOVA"
                elif num_variables == 2:
                    test_name = "Correlation"
                else:
                    test_name = "Other statistical test"
            else:
                if num_variables == 1:
                    if is_parametric:
                        test_name = "One-sample t-test"
                    else:
                        test_name = "Wilcoxon signed-rank test"
                elif num_variables == 2:
                    test_name = "KS test"
                else:
                    test_name = "Other statistical test"

            self.output_box.setText(f"Based on the provided information, it is recommended to use the {test_name}.")
        
        # Clear the input fields
            self.sample_size_input.clear()
            self.num_groups_input.clear()
            self.num_variables_input.clear()
                    
        except ValueError:
            self.output_box.setPlainText("Please enter valid numeric values for all inputs.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        /* Empty stylesheet to prevent inheritance from OS styles */
    ''')
    window = StatisticalTestRecommender()
    window.show()
    sys.exit(app.exec_())
