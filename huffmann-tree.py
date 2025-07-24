import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk

class HuffmanNode:
    
    colors = ["white", "red", "green", "light blue"]  # Liste der Farben
    
    def __init__(self, canvas, x, y, freq, letter=None, is_leaf=True):
        self.canvas = canvas
        self.freq = freq
        self.letter = letter
        self.edges = []
        self.is_connected = False
        self.is_leaf = is_leaf
        self.oval = canvas.create_oval(x-20, y-20, x+20, y+20, fill="white", tags="movable")
        self.text = canvas.create_text(x, y, text=f"{letter}:{freq}" if letter else str(freq))
        self.current_color_index = 0  # Index der aktuellen Farbe
        
    def change_color(self):
        """Wechselt die Farbe des Knotens zur nächsten in der Liste."""
        self.current_color_index = (self.current_color_index + 1) % len(HuffmanNode.colors)
        new_color = HuffmanNode.colors[self.current_color_index]
        self.canvas.itemconfig(self.oval, fill=new_color)

    def add_edge(self, other_node):
        x1, y1, x2, y2 = self.canvas.coords(self.oval)
        nx1, ny1, nx2, ny2 = self.canvas.coords(other_node.oval)
        line = self.canvas.create_line((x1 + x2) / 2, (y1 + y2) / 2, (nx1 + nx2) / 2, (ny1 + ny2) / 2, fill="black")
        self.edges.append({'other_node': other_node, 'line': line})
        other_node.edges.append({'other_node': self, 'line': line})

    def update_position(self, x, y):
        self.canvas.coords(self.oval, x-20, y-20, x+20, y+20)
        self.canvas.coords(self.text, x, y)
        for edge in self.edges:
            ox1, oy1, ox2, oy2 = self.canvas.coords(edge['other_node'].oval)
            self.canvas.coords(edge['line'], x, y, (ox1 + ox2) / 2, (oy1 + oy2) / 2)

        # Positionierung der Knoten mit Text über den Kanten
        self.raise_up()
    
    def raise_up(self):
        self.canvas.tag_raise(self.oval)
        self.canvas.tag_raise(self.text)

class HuffmanTreeApp:
    def __init__(self, root):
        self.root = root
        root.title("Huffman-Baum Erstellen")
        
        self.mode_var = tk.IntVar(value=1)  # Standardmodus ist 1 für den ersten Radiobutton
        self.create_widgets()
        self.nodes = {}
        self.selected_nodes = []
        self.leaf_x = 10
        self.added_texts = []


    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, bg="white", height=550, width=800)
        self.canvas.grid(row=0, columnspan=4)
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<ButtonPress-3>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<Button-2>", self.change_node_color)

        self.prepared_frequencies = ttk.Combobox(self.root, values=["E:4, M:1, W:1, C:1, H:1, U:1, N:3, I:2, T:2, _:3, S:3", "A:5, B:8, C:2, D:7, E:5, H:12, P:24", "E:15, F:6, G:3, P:3, Q:15", "H:10, I:4, J:1", "H:10, o:9, a:5, u:4, _:3, O:2, !:1"])
        self.prepared_frequencies.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.add_button = tk.Button(self.root, text="Hinzufügen", command=self.add_leaves)
        self.add_button.grid(row=1, column=2)

        self.reset_button = tk.Button(self.root, text="Zurücksetzen", command=self.reset_program)
        self.reset_button.grid(row=1, column=3)

        self.radio_button1 = tk.Radiobutton(self.root, text="Knoten verbinden/verschieben", variable=self.mode_var, value=1)
        self.radio_button1.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.radio_button2 = tk.Radiobutton(self.root, text="Kantenbeschriftungen einfügen", variable=self.mode_var, value=2)
        self.radio_button2.grid(row=2, column=2, columnspan=2, sticky="ew")


#         self.prepared_frequencies = ttk.Combobox(self.root, values=["E:4, M:1, W:1, C:1, H:1, U:1, N:3, I:2, T:2, _:3, S:3","A:5, B:8, C:2, D:7, E:5, H:12, P:24", "E:15, F:6, G:3, P:3, Q:15", "H:10, I:4, J:1"])
#         self.prepared_frequencies.grid(row=0, column=0)
#         
#         self.add_button = tk.Button(self.root, text="Hinzufügen", command=self.add_leaves)
#         self.add_button.grid(row=1, column=0)
# 
#         self.reset_button = tk.Button(self.root, text="Zurücksetzen", command=self.reset_program)
#         self.reset_button.grid(row=1, column=1)
# 
#         self.canvas = tk.Canvas(self.root, bg="white", height=800, width=800)
#         self.canvas.grid(row=2, column=0, columnspan=2)
#         self.canvas.bind("<ButtonPress-1>", self.on_click)
#         self.canvas.bind("<ButtonPress-3>", self.on_click)
#         self.canvas.bind("<B1-Motion>", self.on_drag)
#         
#         self.canvas.bind("<Button-2>", self.change_node_color)  # Binden des Mausrad-Klicks
#         
#         # Radiobuttons für die Modus-Auswahl
#         self.radio_button1 = tk.Radiobutton(self.root, text="Knoten verbinden/verschieben", variable=self.mode_var, value=1)
#         self.radio_button1.grid(row=3, column=0, sticky="w")
#         
#         self.radio_button2 = tk.Radiobutton(self.root, text="Kantenbeschriftungen einfügen", variable=self.mode_var, value=2)
#         self.radio_button2.grid(row=4, column=0, sticky="w")
#  
    def change_node_color(self, event):
        """Ändert die Farbe des nächstgelegenen Knotens beim Mausrad-Klick."""
        item = self.canvas.find_closest(event.x, event.y)  # Finde das nächstgelegene Element
        if item:
            node = self.nodes.get(item[0])  # Überprüfe, ob das Element ein Knoten ist
            if node:
                node.change_color()  # Ändere die Farbe des Knotens

 

    def add_leaves(self):
        input_text = self.prepared_frequencies.get()
        if input_text:
            for part in input_text.split(','):
                letter, freq = part.strip().split(':')
                node = HuffmanNode(self.canvas, self.leaf_x+20, 520, int(freq), letter)
                self.nodes[node.oval] = node
                self.leaf_x += 50

    def on_click(self, event):
        
        if self.mode_var.get() == 1:
            self.connect_mode(event)
        
        elif self.mode_var.get() == 2:
            self.insert_label(event)
 

    def connect_mode(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if not items:
            return # Kein Element gefunden

        item = items[0]
        
        if item in self.nodes:
            node = self.nodes[item]
            if node.is_connected:
                messagebox.showinfo("Hinweis", "Der Knoten ist bereits verbunden.")
            if not node.is_connected:
                if node in self.selected_nodes:
                    self.canvas.itemconfig(node.oval, fill="white")
                    self.selected_nodes.remove(node)
                else:
                    if len(self.selected_nodes) < 2:
                        self.canvas.itemconfig(node.oval, fill="green")
                        self.selected_nodes.append(node)
                        if len(self.selected_nodes) == 2:
                            min_nodes = sorted([node for node in self.nodes.values() if not node.is_connected], key=lambda x: x.freq)[:2]
                            if (self.selected_nodes[0].freq == min_nodes[0].freq and self.selected_nodes[1].freq == min_nodes[1].freq) or \
                                (self.selected_nodes[1].freq == min_nodes[0].freq and self.selected_nodes[0].freq == min_nodes[1].freq):
                                self.combine_nodes()
                            else:
                                messagebox.showinfo("Hinweis", "Es gibt Knoten mit niedrigerer Häufigkeit.")
                                
                                
    def insert_label(self, event):
        """Fügt eine Beschriftung an der Position des Mausklicks ein."""
        label = "0" if event.num == 1 else "1" if event.num == 3 else ""
        if label:
            text_id = self.canvas.create_text(event.x, event.y, text=label, font=('Helvetica', '16'))
            self.added_texts.append(text_id)
             
    def on_drag(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        if item in self.nodes:
            node = self.nodes[item]
            node.update_position(event.x, event.y)
            if node in self.selected_nodes:
                self.canvas.itemconfig(node.oval, fill="white")
                self.selected_nodes.remove(node)

    def combine_nodes(self):
        if len(self.selected_nodes) == 2:
            node1, node2 = self.selected_nodes
            if not node1.is_connected and not node2.is_connected:
                x1, y1, x2, y2 = self.canvas.coords(node1.oval)
                x3, y3, x4, y4 = self.canvas.coords(node2.oval)
                new_x = (x1 + x3) / 2
                new_y = min(y1, y3) - 40
                
                # Erstelle den neuen Knoten
                new_node_freq = node1.freq + node2.freq
                new_node = HuffmanNode(self.canvas, new_x, new_y, new_node_freq, is_leaf=False)
                
                # Verbinden Sie den neuen Knoten mit den beiden ausgewählten Knoten
                new_node.add_edge(node1)
                new_node.add_edge(node2)
                
                new_node.raise_up()
                
                self.nodes[new_node.oval] = new_node
                node1.is_connected = True
                node2.is_connected = True
                for node in self.selected_nodes:
                    self.canvas.itemconfig(node.oval, fill="white")
                    node.raise_up()
                    
                    
                self.selected_nodes = []
                self.root.update()


                
    def reset_program(self):
        # Lösche alle Knoten und deren Text
        for node in list(self.nodes.values()):
            self.canvas.delete(node.oval)
            self.canvas.delete(node.text)
        
        # Lösche alle Kanten
        for node in list(self.nodes.values()):
            for edge in node.edges:
                self.canvas.delete(edge['line'])
        
        # Lösche alle eingefügten Beschriftungen (0 und 1)
        for text_id in self.added_texts:
            self.canvas.delete(text_id)
        self.added_texts.clear()  # Leere die Liste nach dem Löschen der Beschriftungen

        # Zurücksetzen der restlichen Variablen
        self.nodes = {}
        self.selected_nodes = []
        self.leaf_x = 10

        messagebox.showinfo("Programm zurücksetzen", "Das Programm wurde zurückgesetzt.")


root = tk.Tk()
app = HuffmanTreeApp(root)
root.mainloop()
