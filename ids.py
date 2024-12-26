import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score
import tkinter as tk
from tkinter import filedialog, messagebox


def load_data(file_path):
    data = pd.read_csv(file_path)
    return data


def preprocess_data(data):
    
    
    data = pd.get_dummies(data)  

    X = data.iloc[:, :-1]  
    y = data.iloc[:, -1]   

    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(report)
    
    return accuracy, report


class IDSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Powered Intrusion Detection System")
        self.root.geometry("500x400")
        
        
        self.label = tk.Label(root, text="Intrusion Detection System", font=("Arial", 16))
        self.label.pack(pady=10)

        
        self.load_button = tk.Button(root, text="Load Network Data", command=self.load_data, width=25)
        self.load_button.pack(pady=20)

        self.run_button = tk.Button(root, text="Run IDS", command=self.run_ids, width=25)
        self.run_button.pack(pady=20)

        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=20)

        self.model = None
        self.data = None

    
    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data = load_data(file_path)
            messagebox.showinfo("Success", "Data Loaded Successfully!")
        else:
            messagebox.showerror("Error", "Failed to Load Data")

    
    def run_ids(self):
        if self.data is None:
            messagebox.showerror("Error", "Please load the data first!")
            return

        try:
            X_train, X_test, y_train, y_test = preprocess_data(self.data)
            self.model = train_model(X_train, y_train)
            accuracy, report = evaluate_model(self.model, X_test, y_test)
            self.result_label.config(text=f"Accuracy: {accuracy:.2f}\nCheck console for detailed report.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = IDSApp(root)
    root.mainloop()
