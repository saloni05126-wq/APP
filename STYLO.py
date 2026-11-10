import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

BG, PINK, DARK, GOLD, WHITE = "#F8F0EB", "#E8C4CC", "#593C43", "#B58A62", "#FFFCFA"
services = [{"name": n, "price": p} for n, p in [
    ("Haircut", 500), ("Facial", 1200), ("Manicure", 600),
    ("Hair Spa", 1500), ("Makeup", 2000)]]
appointments, next_id = [], 1


def money(n):
    return f"Rs. {n:,.2f}"


def label(parent, text, size=11, color=DARK, bold=False):
    return tk.Label(parent, text=text, bg=parent.cget("bg"), fg=color,
                    font=("Segoe UI", size, "bold" if bold else "normal"))


def btn(parent, text, command, color=DARK):
    return tk.Button(parent, text=text, command=command, bg=color, fg="white",
                     activebackground=GOLD, relief="flat", cursor="hand2",
                     font=("Segoe UI", 10, "bold"), padx=10, pady=6)


def tree(parent, cols, heads):
    t = ttk.Treeview(parent, columns=cols, show="headings", height=9)
    for c, h in zip(cols, heads):
        t.heading(c, text=h)
        t.column(c, width=105, anchor="center")
    t.pack(fill="both", expand=True, pady=9)
    return t


class Stylo:
    def __init__(self, root):
        self.root = root
        root.title("STYLO | Salon Management")
        root.geometry("1050x700")
        root.minsize(900, 580)
        root.configure(bg=BG)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=WHITE, fieldbackground=WHITE,
                        foreground=DARK, rowheight=27)
        style.configure("Treeview.Heading", background=DARK, foreground="white")
        self.login_page()

    def clear(self, parent):
        for w in parent.winfo_children():
            w.destroy()

    def login_page(self):
        self.clear(self.root)
        box = tk.Frame(self.root, bg=WHITE, padx=45, pady=35)
        box.place(relx=.5, rely=.5, anchor="center")
        tk.Label(box, text="STYLO", bg=WHITE, fg=DARK,
                 font=("Georgia", 28, "bold")).pack(pady=8)
        label(box, "Where Beauty Meets Precision.", 10, GOLD, True).pack()
        label(box, "Username", 11, DARK, True).pack(anchor="w", pady=(20, 3))
        self.user = tk.Entry(box, font=("Segoe UI", 12), width=27)
        self.user.pack(ipady=5)
        label(box, "Password", 11, DARK, True).pack(anchor="w", pady=(12, 3))
        self.pw = tk.Entry(box, font=("Segoe UI", 12), width=27, show="*")
        self.pw.pack(ipady=5)
        self.pw.bind("<Return>", lambda e: self.login())
        btn(box, "LOGIN", self.login, GOLD).pack(fill="x", pady=18)
        self.err = label(box, "", 10, "#B33A50")
        self.err.pack()
        self.user.focus_set()

    def login(self):
        if self.user.get().strip().upper() == "SALONI" and self.pw.get() == "5126":
            self.main_layout()
        else:
            self.err.config(text="Incorrect username or password.")
            self.pw.delete(0, tk.END)

    def main_layout(self):
        self.clear(self.root)
        side = tk.Frame(self.root, bg=DARK, width=195)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)
        tk.Label(side, text="STYLO", bg=DARK, fg=PINK,
                 font=("Georgia", 21, "bold")).pack(pady=(28, 5))
        label(side, "SALON MANAGEMENT", 9, WHITE).pack(pady=(0, 25))
        self.content = tk.Frame(self.root, bg=BG, padx=22, pady=18)
        self.content.pack(side="right", fill="both", expand=True)
        for name in ("Dashboard", "Appointments", "Services", "Billing", "Records"):
            tk.Button(side, text="  " + name, anchor="w",
                      command=lambda n=name: self.show_page(n), bg=DARK, fg="white",
                      activebackground=GOLD, relief="flat", font=("Segoe UI", 11),
                      padx=15, pady=12).pack(fill="x", padx=7, pady=2)
        btn(side, "LOG OUT", self.login_page, "#79565C").pack(fill="x", padx=13, pady=22)
        self.show_page("Dashboard")

    def show_page(self, name):
        self.clear(self.content)
        self.page = name
        label(self.content, name, 23, DARK, True).pack(anchor="w")
        tk.Frame(self.content, bg=GOLD, height=3, width=65).pack(anchor="w", pady=(5, 15))
        getattr(self, "page_" + name.lower())()

    def refresh(self):
        self.show_page(self.page)

    def page_dashboard(self):
        label(self.content, "Welcome to your beauty space!", 16, GOLD, True).pack(anchor="w")
        today = date.today().strftime("%d-%m-%Y")
        vals = [len(appointments),
                sum(a["date"] == today and a["status"] != "Cancelled" for a in appointments),
                sum(a["status"] == "Completed" for a in appointments),
                money(sum(a["price"] * 1.05 for a in appointments if a["billed"]))]
        row = tk.Frame(self.content, bg=BG)
        row.pack(fill="x", pady=18)
        for title, value in zip(("Total Appointments", "Today's Bookings", "Completed", "Total Revenue"), vals):
            card = tk.Frame(row, bg=WHITE, padx=10, pady=16,
                            highlightbackground=PINK, highlightthickness=1)
            card.pack(side="left", fill="both", expand=True, padx=4)
            label(card, title, 9, GOLD, True).pack(anchor="w")
            label(card, str(value), 15, DARK, True).pack(anchor="w", pady=7)
        label(self.content, "Recent Appointments", 14, DARK, True).pack(anchor="w")
        t = tree(self.content, ("id", "customer", "service", "date", "status"),
                 ("ID", "Customer", "Service", "Date", "Status"))
        for a in appointments[-5:][::-1]:
            t.insert("", "end", values=tuple(a[k] for k in ("id", "customer", "service", "date", "status")))

    def page_appointments(self):
        form = tk.Frame(self.content, bg=BG)
        form.pack(fill="x")
        self.vars = {k: tk.StringVar() for k in ("customer", "phone", "date", "time", "service")}
        self.vars["date"].set(date.today().strftime("%d-%m-%Y"))
        self.vars["time"].set("10:00 AM")
        fields = [("Customer Name", "customer", 14), ("Phone", "phone", 12),
                  ("Date DD-MM-YYYY", "date", 13), ("Time", "time", 10)]
        for title, key, width in fields:
            f = tk.Frame(form, bg=BG)
            f.pack(side="left", padx=(0, 7))
            label(f, title, 9, DARK, True).pack(anchor="w")
            tk.Entry(f, textvariable=self.vars[key], width=width).pack(pady=5, ipady=4)
        f = tk.Frame(self.content, bg=BG)
        f.pack(fill="x", pady=4)
        label(f, "Service", 10, DARK, True).pack(side="left", padx=(0, 8))
        self.service_box = ttk.Combobox(f, textvariable=self.vars["service"], state="readonly", width=18)
        self.service_box.pack(side="left")
        self.update_services()
        btn(f, "Add", self.add_appointment, GOLD).pack(side="left", padx=7)
        btn(f, "Edit Selected", self.edit_appointment).pack(side="left", padx=3)
        btn(f, "Cancel Selected", self.cancel_appointment, "#95616A").pack(side="left", padx=3)
        self.ap_tree = tree(self.content, ("id", "customer", "phone", "service", "date", "time", "status"),
                            ("ID", "Customer", "Phone", "Service", "Date", "Time", "Status"))
        self.ap_tree.bind("<<TreeviewSelect>>", self.select_appointment)
        self.fill_appointments()

    def update_services(self):
        if hasattr(self, "service_box"):
            names = [s["name"] for s in services]
            self.service_box["values"] = names
            if self.vars["service"].get() not in names:
                self.vars["service"].set(names[0] if names else "")

    def fill_appointments(self):
        self.ap_tree.delete(*self.ap_tree.get_children())
        for a in appointments:
            self.ap_tree.insert("", "end", iid=str(a["id"]),
                values=tuple(a[k] for k in ("id", "customer", "phone", "service", "date", "time", "status")))

    def select_appointment(self, event=None):
        if not self.ap_tree.selection():
            return
        a = next(x for x in appointments if str(x["id"]) == self.ap_tree.selection()[0])
        for k in self.vars:
            self.vars[k].set(a[k])

    def add_appointment(self):
        global next_id
        d = {k: v.get().strip() for k, v in self.vars.items()}
        s = next((x for x in services if x["name"] == d["service"]), None)
        if not all(d.values()) or not s:
            messagebox.showerror("Missing Details", "Complete all fields and select a service.")
            return
        try:
            datetime.strptime(d["date"], "%d-%m-%Y")
        except ValueError:
            messagebox.showerror("Invalid Date", "Use DD-MM-YYYY.")
            return
        appointments.append({"id": next_id, **d, "price": s["price"], "status": "Booked", "billed": False})
        next_id += 1
        self.refresh()

    def edit_appointment(self):
        if not self.ap_tree.selection():
            messagebox.showwarning("Select", "Select an appointment first.")
            return
        a = next(x for x in appointments if str(x["id"]) == self.ap_tree.selection()[0])
        s = next((x for x in services if x["name"] == self.vars["service"].get()), None)
        if a["billed"]:
            messagebox.showwarning("Billed", "A billed appointment cannot be edited.")
            return
        d = {k: v.get().strip() for k, v in self.vars.items()}
        if not all(d.values()) or not s:
            messagebox.showerror("Invalid Details", "Complete all fields.")
            return
        try:
            datetime.strptime(d["date"], "%d-%m-%Y")
        except ValueError:
            messagebox.showerror("Invalid Date", "Use DD-MM-YYYY.")
            return
        a.update(d, price=s["price"])
        self.refresh()

    def cancel_appointment(self):
        if not self.ap_tree.selection():
            messagebox.showwarning("Select", "Select an appointment first.")
            return
        a = next(x for x in appointments if str(x["id"]) == self.ap_tree.selection()[0])
        if a["billed"]:
            messagebox.showwarning("Billed", "A billed appointment cannot be cancelled.")
        elif messagebox.askyesno("Cancel", "Cancel this appointment?"):
            a["status"] = "Cancelled"
            self.refresh()

    def page_services(self):
        form = tk.Frame(self.content, bg=BG)
        form.pack(fill="x", pady=8)
        self.sn, self.sp = tk.StringVar(), tk.StringVar()
        for title, var in (("Service Name", self.sn), ("Price (Rs.)", self.sp)):
            f = tk.Frame(form, bg=BG)
            f.pack(side="left", padx=(0, 10))
            label(f, title, 10, DARK, True).pack(anchor="w")
            tk.Entry(f, textvariable=var, width=18).pack(pady=5, ipady=4)
        btn(form, "Add Service", self.add_service, GOLD).pack(side="left", padx=5)
        btn(form, "Delete Selected", self.delete_service, "#95616A").pack(side="left")
        self.stree = tree(self.content, ("name", "price"), ("Service", "Price"))
        self.stree.bind("<<TreeviewSelect>>", self.select_service)
        self.fill_services()

    def fill_services(self):
        self.stree.delete(*self.stree.get_children())
        for s in services:
            self.stree.insert("", "end", iid=s["name"], values=(s["name"], money(s["price"])))

    def select_service(self, event=None):
        if self.stree.selection():
            s = next(x for x in services if x["name"] == self.stree.selection()[0])
            self.sn.set(s["name"])
            self.sp.set(str(s["price"]))

    def add_service(self):
        name = self.sn.get().strip()
        try:
            price = float(self.sp.get())
            if not name or price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a name and positive price.")
            return
        if any(s["name"].lower() == name.lower() for s in services):
            messagebox.showerror("Duplicate", "Service already exists.")
            return
        services.append({"name": name, "price": price})
        self.fill_services()
        self.update_services()
        self.sn.set("")
        self.sp.set("")

    def delete_service(self):
        if not self.stree.selection():
            messagebox.showwarning("Select", "Select a service first.")
            return
        name = self.stree.selection()[0]
        if any(a["service"] == name and a["status"] != "Cancelled" for a in appointments):
            messagebox.showwarning("In Use", "This service belongs to an appointment.")
            return
        services[:] = [s for s in services if s["name"] != name]
        self.fill_services()
        self.update_services()

    def page_billing(self):
        label(self.content, "Select an appointment to prepare its bill.", 12).pack(anchor="w")
        self.bill_var = tk.StringVar()
        self.bill_box = ttk.Combobox(self.content, textvariable=self.bill_var, state="readonly", width=48)
        self.bill_box.pack(anchor="w", pady=10)
        self.bill_box.bind("<<ComboboxSelected>>", lambda e: self.show_bill())
        self.bill = tk.Text(self.content, height=14, bg=WHITE, fg=DARK, font=("Consolas", 11))
        self.bill.pack(fill="both", expand=True, pady=8)
        btn(self.content, "Complete Bill", self.complete_bill, GOLD).pack(anchor="e")
        self.update_bills()
        self.show_bill()

    def update_bills(self):
        choices = [f'{a["id"]} | {a["customer"]} | {a["service"]}'
                   for a in appointments if a["status"] != "Cancelled"]
        self.bill_box["values"] = choices
        if self.bill_var.get() not in choices:
            self.bill_var.set(choices[0] if choices else "")

    def chosen_bill(self):
        try:
            ident = int(self.bill_var.get().split("|")[0])
            return next(a for a in appointments if a["id"] == ident)
        except (ValueError, StopIteration, IndexError):
            return None

    def show_bill(self):
        a = self.chosen_bill()
        self.bill.config(state="normal")
        self.bill.delete("1.0", tk.END)
        if a:
            sub, gst = a["price"], a["price"] * .05
            lines = ["STYLO SALON", "=" * 38, f'Customer: {a["customer"]}',
                     f'Appointment ID: {a["id"]}', f'Date: {a["date"]}  Time: {a["time"]}',
                     "-" * 38, f'Service: {a["service"]}', f"Subtotal: {money(sub)}",
                     f"GST (5%): {money(gst)}", "-" * 38, f"FINAL TOTAL: {money(sub + gst)}",
                     f'Status: {"Paid" if a["billed"] else "Unpaid"}',
                     "Thank you for choosing STYLO!"]
            self.bill.insert(tk.END, "\n".join(lines))
        else:
            self.bill.insert(tk.END, "No appointment available for billing.")
        self.bill.config(state="disabled")

    def complete_bill(self):
        a = self.chosen_bill()
        if not a:
            messagebox.showwarning("No Appointment", "Select an appointment first.")
        elif a["billed"]:
            messagebox.showinfo("Already Paid", "This appointment is already billed.")
        elif a["status"] == "Cancelled":
            messagebox.showerror("Cancelled", "Cancelled appointments cannot be billed.")
        else:
            a["billed"], a["status"] = True, "Completed"
            messagebox.showinfo("Payment Complete", f'Total: {money(a["price"] * 1.05)}')
            self.refresh()

    def page_records(self):
        bar = tk.Frame(self.content, bg=BG)
        bar.pack(fill="x")
        self.search = tk.StringVar()
        self.filter = tk.StringVar(value="All")
        tk.Entry(bar, textvariable=self.search, width=25).pack(side="left", ipady=5)
        ttk.Combobox(bar, textvariable=self.filter, state="readonly",
                     values=["All", "Booked", "Completed", "Cancelled"], width=13).pack(side="left", padx=7)
        btn(bar, "Search / Filter", self.fill_records, GOLD).pack(side="left")
        self.rtree = tree(self.content, ("id", "customer", "phone", "service", "date", "time", "status"),
                          ("ID", "Customer", "Phone", "Service", "Date", "Time", "Status"))
        self.fill_records()

    def fill_records(self):
        if not hasattr(self, "rtree"):
            return
        self.rtree.delete(*self.rtree.get_children())
        q, status = self.search.get().lower().strip(), self.filter.get()
        for a in appointments:
            searchable = f'{a["customer"]} {a["phone"]} {a["service"]} {a["date"]}'.lower()
            if q in searchable and (status == "All" or a["status"] == status):
                self.rtree.insert("", "end", values=tuple(a[k] for k in
                    ("id", "customer", "phone", "service", "date", "time", "status")))


if __name__ == "__main__":
    root = tk.Tk()
    Stylo(root)
    root.mainloop()
