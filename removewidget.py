from news import MainUi


class RemoveWidget(MainUi):
    def autoremove(self):
        if self.status == 1:
            self.right_layout.removeWidget(self.right_lableme)
            self.right_lableme.deleteLater()
            self.right_layout.removeWidget(self.right_lablese)
            self.right_lablese.deleteLater()
            self.right_layout.removeWidget(self.right_pushbutton)
            self.right_pushbutton.deleteLater()
            self.right_layout.removeWidget(self.right_tableView1)
            self.right_tableView1.deleteLater()
        elif self.status == 2:
            self.right_layout.removeWidget(self.right_lableme2)
            self.right_lableme2.deleteLater()
            self.right_layout.removeWidget(self.right_lablese2)
            self.right_lablese2.deleteLater()
            self.right_layout.removeWidget(self.right_pushbutton2)
            self.right_pushbutton2.deleteLater()
            self.right_layout.removeWidget(self.right_tableView2)
            self.right_tableView2.deleteLater()
        elif self.status == 3:
            self.right_layout.removeWidget(self.right_tableView3)
            self.right_layout.removeWidget(self.right_lablese3)
            self.right_layout.removeWidget(self.right_pushbutton3)
            self.right_layout.removeWidget(self.right_lineedit)
            self.right_tableView3.deleteLater()
            self.right_lablese3.deleteLater()
            self.right_pushbutton3.deleteLater()
            self.right_lineedit.deleteLater()
        elif self.status == 4:
            self.right_layout.removeWidget(self.right_help)
            self.right_help.deleteLater()
        elif self.status == 5:
            self.right_layout.removeWidget(self.right_rec)
            self.right_rec.deleteLater()
